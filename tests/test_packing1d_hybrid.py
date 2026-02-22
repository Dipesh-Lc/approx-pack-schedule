from apsuite.packing1d.algorithms import (
    first_fit_decreasing,
    best_fit,
    hybrid_ffd_bf,
)

def test_hybrid_never_worse_than_components():
    items = [0.8, 0.2, 0.7, 0.3, 0.6, 0.4, 0.55, 0.45]
    r_ffd = first_fit_decreasing(items)
    r_bf = best_fit(items)
    r_h = hybrid_ffd_bf(items)
    assert r_h.num_bins <= r_ffd.num_bins
    assert r_h.num_bins <= r_bf.num_bins

def test_hybrid_respects_capacity():
    items = [0.51, 0.49, 0.7, 0.3, 0.3, 0.2, 0.2]
    r_h = hybrid_ffd_bf(items)
    assert all(sum(b) <= 1.0 + 1e-12 for b in r_h.bins)