import pandas as pd

from apsuite.scheduling.unrelated.instances import UnrelatedSpec, generate_unrelated
from apsuite.scheduling.unrelated.lower_bounds import trivial_lb
from apsuite.scheduling.unrelated.algorithms import lp_rounding_with_info, greedy_baseline

def main():
    rows = []
    dists = ["lognormal_machines", "random_matrix", "bimodal_jobs"]
    grid = [(20, 4), (40, 5), (60, 6)]
    seeds = range(5)

    for dist in dists:
        for (n, m) in grid:
            for seed in seeds:
                inst = generate_unrelated(UnrelatedSpec(n=n, m=m, dist=dist, seed=seed))
                lb2 = trivial_lb(inst)

                # GREEDY baseline
                g = greedy_baseline(inst, order="minproc_desc")
                rows.append({
                    "dist": dist, "n": n, "m": m, "seed": seed,
                    "alg": g.alg,
                    "lb_trivial": lb2,
                    "T_lp": None,
                    "C": g.makespan,
                    "ratio_vs_lp": None,
                    "gap_vs_lp": None,
                    "ratio_vs_trivial_lb": g.makespan / lb2 if lb2 > 0 else None,
                    "lp_runtime_s": None,
                    "round_runtime_s": None,
                    "ls_runtime_s": None,
                    "runtime_s": g.info["runtime_s"],
                    "lp_success": None,
                    "lp_status": None,
                })

                # LP rounding (no LS)
                r0 = lp_rounding_with_info(inst, use_local_search=False)
                lpmeta = r0.info["lp"]
                rows.append({
                    "dist": dist, "n": n, "m": m, "seed": seed,
                    "alg": "LP_ROUND",
                    "lb_trivial": lb2,
                    "T_lp": r0.info["T_lp"],
                    "C": r0.makespan,
                    "ratio_vs_lp": r0.info["ratio_vs_lp"],
                    "gap_vs_lp": r0.info["gap_vs_lp"],
                    "ratio_vs_trivial_lb": r0.makespan / lb2 if lb2 > 0 else None,
                    "lp_runtime_s": lpmeta["runtime_s"],
                    "round_runtime_s": r0.info["round_runtime_s"],
                    "ls_runtime_s": None,
                    "runtime_s": r0.info["total_runtime_s"],
                    "lp_success": lpmeta["success"],
                    "lp_status": lpmeta["status"],
                })

                # LP rounding + LS
                r1 = lp_rounding_with_info(inst, use_local_search=True, ls_time_limit_s=0.01)
                lpmeta = r1.info["lp"]
                rows.append({
                    "dist": dist, "n": n, "m": m, "seed": seed,
                    "alg": "LP_ROUND+LS",
                    "lb_trivial": lb2,
                    "T_lp": r1.info["T_lp"],
                    "C": r1.makespan,
                    "ratio_vs_lp": r1.info["ratio_vs_lp"],
                    "gap_vs_lp": r1.info["gap_vs_lp"],
                    "ratio_vs_trivial_lb": r1.makespan / lb2 if lb2 > 0 else None,
                    "lp_runtime_s": lpmeta["runtime_s"],
                    "round_runtime_s": r1.info["round_runtime_s"],
                    "ls_runtime_s": (r1.info["ls"]["runtime_s"] if r1.info["ls"] else None),
                    "runtime_s": r1.info["total_runtime_s"],
                    "lp_success": lpmeta["success"],
                    "lp_status": lpmeta["status"],
                })

    df = pd.DataFrame(rows)
    out = "results/tables/sched_unrelated_lp.csv"
    df.to_csv(out, index=False)
    print("Wrote:", out)

    # Summaries
    print("\nMean ratio_vs_lp (LP algorithms only):")
    dflp = df[df["ratio_vs_lp"].notna()]
    print(dflp.groupby(["dist", "n", "m", "alg"])[["ratio_vs_lp", "runtime_s"]].mean().round(4))

    print("\nMean ratio_vs_trivial_lb (all algorithms):")
    print(df.groupby(["dist", "n", "m", "alg"])[["ratio_vs_trivial_lb", "runtime_s"]].mean().round(4))

if __name__ == "__main__":
    main()