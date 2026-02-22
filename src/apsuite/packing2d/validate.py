from __future__ import annotations
from typing import Iterable, List
from apsuite.packing2d.types import Rect

def validate_rects(rects: Iterable[Rect], W: float, H: float) -> List[Rect]:
    if W <= 0 or H <= 0:
        raise ValueError("Bin dimensions must be > 0")
    rects = list(rects)
    for r in rects:
        if r.w <= 0 or r.h <= 0:
            raise ValueError(f"Rectangle must have positive size: {r}")
        if r.w > W or r.h > H:
            raise ValueError(f"Rectangle {r} does not fit in bin ({W}, {H})")
    return rects