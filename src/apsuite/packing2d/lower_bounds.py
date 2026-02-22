from __future__ import annotations
import math
from typing import Sequence
from apsuite.packing2d.types import Rect
from apsuite.packing2d.validate import validate_rects

def area_lower_bound(rects: Sequence[Rect], W: float, H: float) -> int:
    rects = validate_rects(rects, W, H)
    if not rects:
        return 0
    total_area = sum(r.w * r.h for r in rects)
    return int(math.ceil(total_area / (W * H)))