from apsuite.packing2d.types import Rect
from apsuite.packing2d.lower_bounds import area_lower_bound
from apsuite.packing2d.shelf import shelf_pack

def test_area_lower_bound_simple():
    rects = [Rect(1,1), Rect(1,1)]
    assert area_lower_bound(rects, W=2, H=1) == 1  # total area=2, bin area=2

def test_shelf_pack_produces_valid_bin_count():
    rects = [Rect(2,1), Rect(2,1), Rect(2,1)]
    res = shelf_pack(rects, W=4, H=2)
    assert res.num_bins == 1  # should fit (two on first shelf, one below)

def test_shelf_pack_multiple_bins():
    rects = [Rect(4,2), Rect(4,2)]
    res = shelf_pack(rects, W=4, H=2)
    assert res.num_bins == 2