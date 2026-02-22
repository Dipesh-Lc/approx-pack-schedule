from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from apsuite.packing2d.types import Rect, Bin2D, Packing2DResult
from apsuite.packing2d.validate import validate_rects


@dataclass
class FreeRect:
    x: float
    y: float
    w: float
    h: float


def _fits(r: Rect, fr: FreeRect) -> bool:
    return r.w <= fr.w and r.h <= fr.h


def _split_guillotine(fr: FreeRect, r: Rect) -> List[FreeRect]:
    """
    Place r at (fr.x, fr.y). Split remaining space into:
      - right piece: (x + r.w, y, fr.w - r.w, r.h)
      - top piece:   (x, y + r.h, fr.w, fr.h - r.h)
    Both are guillotine-legal. Some variants use different split rules; this is simple and consistent.
    """
    out: List[FreeRect] = []
    # Right remainder (beside the placed rect, same height as rect)
    rw = fr.w - r.w
    if rw > 1e-12:
        out.append(FreeRect(fr.x + r.w, fr.y, rw, r.h))

    # Top remainder (above the placed rect, full original width)
    th = fr.h - r.h
    if th > 1e-12:
        out.append(FreeRect(fr.x, fr.y + r.h, fr.w, th))

    return out


def _prune_free_rects(free_rects: List[FreeRect]) -> List[FreeRect]:
    """
    Remove free rectangles fully contained in another.
    Keeps the list smaller and avoids redundant fits.
    """
    pruned: List[FreeRect] = []
    for i, a in enumerate(free_rects):
        contained = False
        for j, b in enumerate(free_rects):
            if i == j:
                continue
            if (a.x >= b.x - 1e-12 and a.y >= b.y - 1e-12
                and a.x + a.w <= b.x + b.w + 1e-12
                and a.y + a.h <= b.y + b.h + 1e-12):
                contained = True
                break
        if not contained:
            pruned.append(a)
    return pruned


def guillotine_pack(
    rects: List[Rect],
    W: float,
    H: float,
    order: str = "decreasing_area",
    score: str = "best_area_fit",
) -> Packing2DResult:
    """
    Simple guillotine heuristic (no rotation).
    order:
      - 'input'
      - 'decreasing_area'
      - 'decreasing_maxside'
    score (select free rectangle):
      - 'best_area_fit': minimizes leftover area (fr.w*fr.h - r.w*r.h)
      - 'best_short_side': minimizes min(fr.w-r.w, fr.h-r.h)
    """
    rects = validate_rects(rects, W, H)
    items = rects[:]

    if order == "decreasing_area":
        items.sort(key=lambda r: r.w * r.h, reverse=True)
    elif order == "decreasing_maxside":
        items.sort(key=lambda r: max(r.w, r.h), reverse=True)
    elif order == "input":
        pass
    else:
        raise ValueError(f"Unknown order: {order}")

    bins: List[Bin2D] = []

    # For each bin we track placements and free rectangles
    placements: List[Tuple[Rect, float, float]] = []
    free_rects: List[FreeRect] = [FreeRect(0.0, 0.0, W, H)]

    def close_bin_and_open_new():
        nonlocal placements, free_rects
        if placements:
            bins.append(Bin2D(placements=placements))
        placements = []
        free_rects = [FreeRect(0.0, 0.0, W, H)]

    for r in items:
        best_idx: Optional[int] = None
        best_score: Optional[float] = None

        for i, fr in enumerate(free_rects):
            if not _fits(r, fr):
                continue

            if score == "best_area_fit":
                s = (fr.w * fr.h) - (r.w * r.h)
            elif score == "best_short_side":
                s = min(fr.w - r.w, fr.h - r.h)
            else:
                raise ValueError(f"Unknown score: {score}")

            if best_score is None or s < best_score:
                best_score = s
                best_idx = i

        if best_idx is None:
            # No fit in current bin → open a new bin
            close_bin_and_open_new()
            # After opening, it must fit in the fresh bin
            fr0 = free_rects[0]
            placements.append((r, fr0.x, fr0.y))
            free_rects = _split_guillotine(fr0, r)
            free_rects = _prune_free_rects(free_rects)
            continue

        # Place in chosen free rectangle
        fr = free_rects.pop(best_idx)
        placements.append((r, fr.x, fr.y))
        free_rects.extend(_split_guillotine(fr, r))
        free_rects = _prune_free_rects(free_rects)

    # Finalize last bin
    if placements:
        bins.append(Bin2D(placements=placements))

    return Packing2DResult(bins=bins)