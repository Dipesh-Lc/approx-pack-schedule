import pandas as pd
import matplotlib.pyplot as plt

CSV = "results/tables/sched_identical.csv"
OUTDIR = "results/figures"

def main():
    df = pd.read_csv(CSV).dropna(subset=["ratio", "runtime_s"])

    # 1) Ratio vs LB by n (separate figure for each dist, lines per algorithm)
    for dist, dfd in df.groupby("dist"):
        plt.figure()
        summary = (
            dfd.groupby(["n", "alg"])["ratio"]
            .mean()
            .reset_index()
            .pivot(index="n", columns="alg", values="ratio")
            .sort_index()
        )
        for alg in summary.columns:
            plt.plot(summary.index, summary[alg], marker="o", label=alg)

        plt.xlabel("n (number of jobs)")
        plt.ylabel("Mean C_alg / LB")
        plt.title(f"Identical Machines Scheduling: Ratio vs LB ({dist})")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        out = f"{OUTDIR}/sched_identical_ratio_{dist}.png"
        plt.savefig(out, dpi=200)
        plt.close()
        print("Wrote:", out)

    # 2) Runtime scaling
    for dist, dfd in df.groupby("dist"):
        plt.figure()
        summary = (
            dfd.groupby(["n", "alg"])["runtime_s"]
            .mean()
            .reset_index()
            .pivot(index="n", columns="alg", values="runtime_s")
            .sort_index()
        )
        for alg in summary.columns:
            plt.plot(summary.index, summary[alg], marker="o", label=alg)

        plt.xlabel("n (number of jobs)")
        plt.ylabel("Mean runtime (s)")
        plt.title(f"Identical Machines Scheduling: Runtime scaling ({dist})")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        out = f"{OUTDIR}/sched_identical_runtime_{dist}.png"
        plt.savefig(out, dpi=200)
        plt.close()
        print("Wrote:", out)

    # 3) Histogram of ratios (pooled)
    plt.figure()
    for alg, dfa in df.groupby("alg"):
        plt.hist(dfa["ratio"], bins=40, alpha=0.5, label=alg)

    plt.xlabel("C_alg / LB")
    plt.ylabel("Count")
    plt.title("Identical Machines Scheduling: Ratio vs LB (all instances)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    out = f"{OUTDIR}/sched_identical_ratio_hist_all.png"
    plt.savefig(out, dpi=200)
    plt.close()
    print("Wrote:", out)

if __name__ == "__main__":
    main()