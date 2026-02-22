from apsuite.packing1d.algorithms import first_fit_decreasing
from apsuite.packing1d.local_search import local_improve_eliminate_bins

def test_local_improvement_never_violates_capacity():
    items = [0.51, 0.49, 0.7, 0.3, 0.3, 0.2, 0.2]
    res = first_fit_decreasing(items)
    improved = local_improve_eliminate_bins(res, capacity=1.0)
    assert all(sum(b) <= 1.0 + 1e-12 for b in improved.bins)

def test_local_improvement_does_not_increase_bins():
    items = [0.6, 0.6, 0.4, 0.4, 0.2, 0.2]
    res = first_fit_decreasing(items)
    improved = local_improve_eliminate_bins(res, capacity=1.0)
    assert improved.num_bins <= res.num_bins