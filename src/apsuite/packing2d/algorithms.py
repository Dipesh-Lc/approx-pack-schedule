from __future__ import annotations
from typing import List
from apsuite.packing2d.types import Rect, Packing2DResult
from apsuite.packing2d.shelf import shelf_pack
from apsuite.packing2d.guillotine import guillotine_pack

def shelf(rects: List[Rect], W: float, H: float) -> Packing2DResult:
    return shelf_pack(rects, W=W, H=H, decreasing_height=True)

def guillotine(rects: List[Rect], W: float, H: float) -> Packing2DResult:
    return guillotine_pack(rects, W=W, H=H, order="decreasing_area", score="best_area_fit")

def best_of_two(a: Packing2DResult, b: Packing2DResult) -> Packing2DResult:
    # Deterministic tie-breaker: prefer 'a' on ties
    return b if b.num_bins < a.num_bins else a


def hybrid_shelf_guillotine(rects: List[Rect], W: float, H: float) -> Packing2DResult:
    """
    Portfolio heuristic: run both Shelf and Guillotine and keep the better packing (fewer bins).
    """
    r_shelf = shelf(rects, W=W, H=H)
    r_gui = guillotine(rects, W=W, H=H)
    return best_of_two(r_shelf, r_gui)