from apsuite.packing2d.types import Rect
from apsuite.packing2d.guillotine import guillotine_pack

def test_guillotine_pack_simple_fit_one_bin():
    rects = [Rect(2,1), Rect(2,1), Rect(2,1)]
    res = guillotine_pack(rects, W=4, H=2)
    assert res.num_bins == 1

def test_guillotine_pack_multiple_bins():
    rects = [Rect(4,2), Rect(4,2)]
    res = guillotine_pack(rects, W=4, H=2)
    assert res.num_bins == 2

def test_guillotine_never_places_outside_bin():
    rects = [Rect(3,1), Rect(1,1), Rect(2,1)]
    W, H = 4, 2
    res = guillotine_pack(rects, W=W, H=H)
    for b in res.bins:
        for r, x, y in b.placements:
            assert x >= -1e-12 and y >= -1e-12
            assert x + r.w <= W + 1e-12
            assert y + r.h <= H + 1e-12