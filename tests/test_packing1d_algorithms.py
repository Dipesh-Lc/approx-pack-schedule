from apsuite.packing1d.algorithms import (
    first_fit,
    best_fit,
    first_fit_decreasing,
    best_fit_decreasing,
)

def test_all_algorithms_respect_capacity():
    items = [0.51, 0.49, 0.7, 0.3, 0.3, 0.2]
    for alg in [first_fit, best_fit, first_fit_decreasing, best_fit_decreasing]:
        res = alg(items, capacity=1.0)
        assert all(load <= 1.0 + 1e-12 for load in res.loads)

def test_decreasing_not_worse_on_simple_case():
    # Not a theorem, but a reasonable sanity check for this case
    items = [0.4, 0.4, 0.4, 0.6, 0.6]
    ff = first_fit(items).num_bins
    ffd = first_fit_decreasing(items).num_bins
    assert ffd <= ff