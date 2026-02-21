from apsuite.packing1d.algorithms import (
    first_fit, best_fit, first_fit_decreasing, best_fit_decreasing
)
from apsuite.packing1d.lower_bounds import volume_lower_bound
from apsuite.common.metrics import packing_metrics

if __name__ == "__main__":
    items = [0.5, 0.7, 0.2, 0.4, 0.8, 0.1]
    lb = volume_lower_bound(items)

    print("LB(volume):", lb)
    for alg in [first_fit, best_fit, first_fit_decreasing, best_fit_decreasing]:
        res = alg(items)
        m = packing_metrics(res, lb)
        print(f"{alg.__name__}: bins={m.num_bins}, ratio_vs_lb={m.approx_ratio_vs_lb:.3f}, gap={m.gap_vs_lb:.3f}")