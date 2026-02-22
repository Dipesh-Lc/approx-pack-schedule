from __future__ import annotations
from typing import List
from apsuite.packing2d.types import Rect, Bin2D, Packing2DResult
from apsuite.packing2d.validate import validate_rects

def shelf_pack(rects: List[Rect], W: float, H: float, decreasing_height: bool = True) -> Packing2DResult:
    rects = validate_rects(rects, W, H)
    items = rects[:]
    if decreasing_height:
        items.sort(key=lambda r: r.h, reverse=True)

    bins: List[Bin2D] = []
    cur_bin: List[tuple] = []
    x = 0.0
    y = 0.0
    shelf_h = 0.0

    def new_bin():
        nonlocal cur_bin, x, y, shelf_h
        if cur_bin:
            bins.append(Bin2D(placements=cur_bin))
        cur_bin = []
        x = 0.0
        y = 0.0
        shelf_h = 0.0

    new_bin()  # initialize empty bin state

    for r in items:
        # Start new shelf if doesn't fit in current row
        if x + r.w > W:
            y += shelf_h
            x = 0.0
            shelf_h = 0.0

        # If doesn't fit vertically, open new bin
        if y + r.h > H:
            new_bin()

        # Place rectangle
        cur_bin.append((r, x, y))
        x += r.w
        shelf_h = max(shelf_h, r.h)

    # push last bin
    if cur_bin:
        bins.append(Bin2D(placements=cur_bin))

    return Packing2DResult(bins=bins)