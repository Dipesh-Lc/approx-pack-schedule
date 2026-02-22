import time
import pandas as pd

from apsuite.scheduling.identical.instances import IdenticalSchedSpec, generate_jobs
from apsuite.scheduling.identical.algorithms import list_scheduling, lpt
from apsuite.scheduling.identical.lower_bounds import lb_makespan_identical

ALGS = {"LIST": list_scheduling, "LPT": lpt}

def main():
    rows = []
    for dist in ["uniform", "bimodal", "heavy_tail"]:
        for (n, m) in [(50, 5), (200, 10), (800, 20)]:
            for seed in range(5):
                spec = IdenticalSchedSpec(n=n, m=m, dist=dist, seed=seed)
                p = generate_jobs(spec)
                lb = lb_makespan_identical(p, m=m)

                for alg_name, alg in ALGS.items():
                    t0 = time.perf_counter()
                    sched = alg(p, m=m)
                    dt = time.perf_counter() - t0
                    C = sched.makespan
                    ratio = C / lb if lb > 0 else None

                    rows.append({
                        "dist": dist,
                        "n": n,
                        "m": m,
                        "seed": seed,
                        "alg": alg_name,
                        "makespan": C,
                        "lb": lb,
                        "ratio": ratio,
                        "runtime_s": dt,
                    })

    df = pd.DataFrame(rows)
    out = "results/tables/sched_identical.csv"
    df.to_csv(out, index=False)
    print("Wrote:", out)
    print(df.groupby(["dist", "n", "m", "alg"])[["ratio", "runtime_s"]].mean().round(4))

if __name__ == "__main__":
    main()