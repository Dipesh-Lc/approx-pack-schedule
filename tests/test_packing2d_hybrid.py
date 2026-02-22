from apsuite.packing2d.types import Rect
from apsuite.packing2d.algorithms import shelf, guillotine, hybrid_shelf_guillotine

def test_2d_hybrid_never_worse_than_components():
    rects = [
        Rect(6, 2), Rect(4, 2), Rect(5, 1),
        Rect(2, 6), Rect(2, 4), Rect(1, 5),
        Rect(3, 3), Rect(3, 2),
    ]
    W, H = 10, 10
    r_s = shelf(rects, W=W, H=H)
    r_g = guillotine(rects, W=W, H=H)
    r_h = hybrid_shelf_guillotine(rects, W=W, H=H)

    assert r_h.num_bins <= r_s.num_bins
    assert r_h.num_bins <= r_g.num_bins