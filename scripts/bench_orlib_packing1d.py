import time
import pandas as pd

from apsuite.packing1d.algorithms import (
    first_fit, best_fit, first_fit_decreasing, best_fit_decreasing
)
from apsuite.packing1d.lower_bounds import volume_lower_bound  # keep consistent for now
from apsuite.common.metrics import packing_metrics
from apsuite.packing1d.orlib_parser import load_orlib_dir
from apsuite.packing1d.algorithms import ffd_local_improve
from apsuite.packing1d.algorithms import hybrid_ffd_bf

ALGS = {
    "FF": first_fit,
    "BF": best_fit,
    "FFD": first_fit_decreasing,
    "BFD": best_fit_decreasing,
    "FFD+LS": ffd_local_improve,
    "HYB(FFD,BF)": hybrid_ffd_bf,
}

def classify_instance(name: str) -> str:
    name = name.lower()
    if name.startswith("u"):
        return "uniform"
    if name.startswith("t"):
        return "triplets"
    return "other"

def main():
    instances = load_orlib_dir("data/raw/orlib_1d", normalize_capacity=True)

    rows = []
    for inst in instances:
        items = inst.items
        lb = volume_lower_bound(items, capacity=1.0)

        for alg_name, alg in ALGS.items():
            t0 = time.perf_counter()
            res = alg(items, capacity=1.0)
            dt = time.perf_counter() - t0

            met = packing_metrics(res, lb)

            # Compare to best-known (from file header)
            ratio_vs_best = res.num_bins / inst.best_known_bins if inst.best_known_bins > 0 else None
            inst_class = classify_instance(inst.name)
            relative_gap = (
                (res.num_bins - inst.best_known_bins) / inst.best_known_bins
                if inst.best_known_bins > 0 else None
            )            
            rows.append({
                "instance": inst.name,
                "alg": alg_name,
                "n": len(items),
                "capacity": inst.capacity,
                "best_known_bins": inst.best_known_bins,
                "bins": res.num_bins,
                "ratio_vs_best": ratio_vs_best,
                "lb_volume": lb,
                "ratio_vs_lb": met.approx_ratio_vs_lb,
                "gap_vs_lb": met.gap_vs_lb,
                "runtime_s": dt,
                "class": inst_class,
                "source": inst.source,
                "gap_vs_best": relative_gap,
            })

    df = pd.DataFrame(rows)
    out = "results/tables/orlib_packing1d.csv"
    df.to_csv(out, index=False)
    print("Wrote:", out)

    # Simple summary table
    print("\nMean performance across ALL instances:")
    print(df.groupby("alg")[["ratio_vs_best", "runtime_s", "bins"]].mean().round(4))

    print("\nMean ratio_vs_best by class:")
    print(df.groupby(["class", "alg"])["ratio_vs_best"].mean().round(4))

    print("\nMean ratio_vs_best by source file:")
    print(df.groupby(["source", "alg"])["ratio_vs_best"].mean().round(4))

    print("\nMean gap_vs_best by class:")
    print(df.groupby(["class", "alg"])["gap_vs_best"].mean().round(4))
if __name__ == "__main__":
    main()