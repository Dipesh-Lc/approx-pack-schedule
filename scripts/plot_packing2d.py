import pandas as pd
import matplotlib.pyplot as plt

CSV = "results/tables/packing2d_baseline.csv"
OUTDIR = "results/figures"

def main():
    df = pd.read_csv(CSV).dropna(subset=["ratio_vs_lb", "gap_vs_lb", "runtime_s"])

    # Ratio vs LB plots by dist
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

        plt.xlabel("n (number of rectangles)")
        plt.ylabel("Mean bins / LB(area)")
        plt.title(f"2D Bin Packing: Mean ratio vs area LB ({dist})")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        out = f"{OUTDIR}/packing2d_ratio_vs_lb_{dist}.png"
        plt.savefig(out, dpi=200)
        plt.close()
        print("Wrote:", out)

    # Runtime scaling
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

        plt.xlabel("n (number of rectangles)")
        plt.ylabel("Mean runtime (s)")
        plt.title(f"2D Bin Packing: Runtime scaling ({dist})")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        out = f"{OUTDIR}/packing2d_runtime_{dist}.png"
        plt.savefig(out, dpi=200)
        plt.close()
        print("Wrote:", out)

    # Gap histogram
    plt.figure()
    for alg, dfa in df.groupby("alg"):
        plt.hist(dfa["gap_vs_lb"], bins=40, alpha=0.5, label=alg)
    plt.xlabel("(bins - LB)/LB")
    plt.ylabel("Count")
    plt.title("2D Bin Packing: Gap vs area LB (all instances)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    out = f"{OUTDIR}/packing2d_gap_hist_all.png"
    plt.savefig(out, dpi=200)
    plt.close()
    print("Wrote:", out)

if __name__ == "__main__":
    main()