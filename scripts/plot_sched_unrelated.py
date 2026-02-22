import pandas as pd
import matplotlib.pyplot as plt

CSV = "results/tables/sched_unrelated_lp.csv"
OUTDIR = "results/figures"

LP_ALGS = ["LP_ROUND", "LP_ROUND+LS"]  # keep focused
ALL_ALGS = None  # will infer from data

def main():
    df = pd.read_csv(CSV)

    # --- 1) Ratio vs LP (LP algs only) ---
    dflp = df[df["alg"].isin(LP_ALGS)].dropna(subset=["ratio_vs_lp"])
    for dist, dfd in dflp.groupby("dist"):
        plt.figure()
        summary = (
            dfd.groupby(["n", "alg"])["ratio_vs_lp"]
            .mean()
            .reset_index()
            .pivot(index="n", columns="alg", values="ratio_vs_lp")
            .sort_index()
        )
        for alg in summary.columns:
            plt.plot(summary.index, summary[alg], marker="o", label=alg)

        plt.xlabel("n (number of jobs)")
        plt.ylabel("Mean C / T_lp")
        plt.title(f"Unrelated Machines: Ratio vs LP bound ({dist})")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        out = f"{OUTDIR}/sched_unrelated_ratio_vs_lp_{dist}.png"
        plt.savefig(out, dpi=200)
        plt.close()
        print("Wrote:", out)

    # --- 2) Ratio vs trivial LB (all algs) ---
    dft = df.dropna(subset=["ratio_vs_trivial_lb"])
    for dist, dfd in dft.groupby("dist"):
        plt.figure()
        summary = (
            dfd.groupby(["n", "alg"])["ratio_vs_trivial_lb"]
            .mean()
            .reset_index()
            .pivot(index="n", columns="alg", values="ratio_vs_trivial_lb")
            .sort_index()
        )
        for alg in summary.columns:
            plt.plot(summary.index, summary[alg], marker="o", label=alg)

        plt.xlabel("n (number of jobs)")
        plt.ylabel("Mean C / LB_trivial")
        plt.title(f"Unrelated Machines: Ratio vs trivial LB ({dist})")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        out = f"{OUTDIR}/sched_unrelated_ratio_vs_trivialLB_{dist}.png"
        plt.savefig(out, dpi=200)
        plt.close()
        print("Wrote:", out)

    # --- 3) Runtime scaling (all algs) ---
    for dist, dfd in df.dropna(subset=["runtime_s"]).groupby("dist"):
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
        plt.title(f"Unrelated Machines: Runtime scaling ({dist})")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        out = f"{OUTDIR}/sched_unrelated_runtime_{dist}.png"
        plt.savefig(out, dpi=200)
        plt.close()
        print("Wrote:", out)

    # --- 4) Histogram: ratio_vs_lp (LP algs only) ---
    plt.figure()
    for alg, dfa in dflp.groupby("alg"):
        plt.hist(dfa["ratio_vs_lp"], bins=40, alpha=0.5, label=alg)

    plt.xlabel("C / T_lp")
    plt.ylabel("Count")
    plt.title("Unrelated Machines: Ratio vs LP bound (LP algorithms)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    out = f"{OUTDIR}/sched_unrelated_ratio_vs_lp_hist.png"
    plt.savefig(out, dpi=200)
    plt.close()
    print("Wrote:", out)


if __name__ == "__main__":
    main()