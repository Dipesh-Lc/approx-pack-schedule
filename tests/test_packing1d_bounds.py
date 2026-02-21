from apsuite.packing1d.lower_bounds import volume_lower_bound

def test_volume_lb_basic():
    items = [0.5, 0.7, 0.2, 0.4]
    assert volume_lower_bound(items) == 2  # sum=1.8 -> ceil=2

def test_volume_lb_empty():
    assert volume_lower_bound([]) == 0