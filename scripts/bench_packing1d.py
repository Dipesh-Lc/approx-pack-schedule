import time
import pandas as pd

from apsuite.packing1d.algorithms import (
    first_fit, best_fit, first_fit_decreasing, best_fit_decreasing
)
from apsuite.packing1d.instances import InstanceSpec, generate_instance
from apsuite.common.metrics import packing_metrics
from apsuite.packing1d.lower_bounds import combined_lower_bound

ALGS = {
    "FF": first_fit,
    "BF": best_fit,
    "FFD": first_fit_decreasing,
    "BFD": best_fit_decreasing,
}

def run_one(n: int, dist: str, seed: int):
    spec = InstanceSpec(name=f"{dist}_n{n}_s{seed}", n=n, dist=dist, seed=seed)
    items = generate_instance(spec)
    lb = combined_lower_bound(items)

    rows = []
    for name, alg in ALGS.items():
        t0 = time.perf_counter()
        res = alg(items)
        dt = time.perf_counter() - t0
        met = packing_metrics(res, lb)

        rows.append({
            "instance": spec.name,
            "n": n,
            "dist": dist,
            "seed": seed,
            "alg": name,
            "bins": met.num_bins,
            "lb_volume": met.lower_bound,
            "ratio_vs_lb": met.approx_ratio_vs_lb,
            "gap_vs_lb": met.gap_vs_lb,
            "runtime_s": dt,
        })
    return rows

if __name__ == "__main__":
    all_rows = []
    for dist in ["uniform", "bimodal", "heavy_tail"]:
        for n in [100, 500, 2000]:
            for seed in [0, 1, 2, 3, 4]:
                all_rows.extend(run_one(n=n, dist=dist, seed=seed))

    df = pd.DataFrame(all_rows)
    out = "results/tables/packing1d_baseline.csv"
    df.to_csv(out, index=False)
    print("Wrote:", out)
    print(df.groupby(["dist", "n", "alg"])["bins"].mean().round(2))