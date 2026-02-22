import time
import pandas as pd

from apsuite.packing2d.instances import Instance2DSpec, generate_rectangles
from apsuite.packing2d.lower_bounds import area_lower_bound
from apsuite.packing2d.algorithms import shelf, guillotine, hybrid_shelf_guillotine

ALGS = {
    "SHELF": shelf,
    "GUILLOTINE": guillotine,
    "HYB(SHELF,GUIL)": hybrid_shelf_guillotine,
}

def run_one(n: int, dist: str, seed: int, W: float, H: float):
    spec = Instance2DSpec(
        name=f"{dist}_n{n}_s{seed}_W{W}_H{H}",
        n=n, dist=dist, seed=seed, W=W, H=H
    )
    rects = generate_rectangles(spec)
    lb = area_lower_bound(rects, W=W, H=H)

    rows = []
    for alg_name, alg in ALGS.items():
        t0 = time.perf_counter()
        res = alg(rects, W=W, H=H)
        dt = time.perf_counter() - t0
        bins = res.num_bins
        ratio = (bins / lb) if lb > 0 else None
        gap = ((bins - lb) / lb) if lb > 0 else None

        rows.append({
            "instance": spec.name,
            "n": n,
            "dist": dist,
            "seed": seed,
            "W": W,
            "H": H,
            "alg": alg_name,
            "bins": bins,
            "lb_area": lb,
            "ratio_vs_lb": ratio,
            "gap_vs_lb": gap,
            "runtime_s": dt,
        })
    return rows

if __name__ == "__main__":
    W, H = 10.0, 10.0  # fixed bin size for now
    all_rows = []
    for dist in ["uniform", "bimodal", "heavy_tail"]:
        for n in [50, 200, 800]:
            for seed in [0, 1, 2, 3, 4]:
                all_rows.extend(run_one(n=n, dist=dist, seed=seed, W=W, H=H))

    df = pd.DataFrame(all_rows)
    out = "results/tables/packing2d_baseline.csv"
    df.to_csv(out, index=False)
    print("Wrote:", out)

    summary = df.groupby(["dist", "n", "alg"])[["bins", "ratio_vs_lb", "runtime_s"]].mean().round(4)
    print(summary)