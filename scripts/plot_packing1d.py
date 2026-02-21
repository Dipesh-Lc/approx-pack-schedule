import pandas as pd
import matplotlib.pyplot as plt

CSV = "results/tables/packing1d_baseline.csv"
OUTDIR = "results/figures"

def main():
    df = pd.read_csv(CSV)

    # Safety: drop None
    df = df.dropna(subset=["ratio_vs_lb", "gap_vs_lb", "runtime_s"])

    # ---- Plot 1: Mean ratio vs LB by n (lines per algorithm), per distribution
    for dist, dfd in df.groupby("dist"):
        plt.figure()
        summary = (
            dfd.groupby(["n", "alg"])["ratio_vs_lb"]
            .mean()
            .reset_index()
            .pivot(index="n", columns="alg", values="ratio_vs_lb")
            .sort_index()
        )
        for alg in summary.columns:
            plt.plot(summary.index, summary[alg], marker="o", label=alg)

        plt.xlabel("n (number of items)")
        plt.ylabel("Mean bins / LB(volume)")
        plt.title(f"1D Bin Packing: Mean ratio vs volume LB ({dist})")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        out = f"{OUTDIR}/packing1d_ratio_vs_lb_{dist}.png"
        plt.savefig(out, dpi=200)
        plt.close()
        print("Wrote:", out)

    # ---- Plot 2: Runtime scaling (log scale y often helps)
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

        plt.xlabel("n (number of items)")
        plt.ylabel("Mean runtime (s)")
        plt.title(f"1D Bin Packing: Runtime scaling ({dist})")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        out = f"{OUTDIR}/packing1d_runtime_{dist}.png"
        plt.savefig(out, dpi=200)
        plt.close()
        print("Wrote:", out)

    # ---- Plot 3: Gap histogram pooled (best for “distributional view”)
    plt.figure()
    for alg, dfa in df.groupby("alg"):
        plt.hist(dfa["gap_vs_lb"], bins=40, alpha=0.5, label=alg)
    plt.xlabel("(bins - LB)/LB")
    plt.ylabel("Count")
    plt.title("1D Bin Packing: Gap vs volume LB (all instances)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    out = f"{OUTDIR}/packing1d_gap_hist_all.png"
    plt.savefig(out, dpi=200)
    plt.close()
    print("Wrote:", out)

if __name__ == "__main__":
    main()