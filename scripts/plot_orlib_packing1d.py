import pandas as pd
import matplotlib.pyplot as plt

CSV = "results/tables/orlib_packing1d.csv"
OUT = "results/figures/orlib_ratio_vs_best_boxplot.png"

def main():
    df = pd.read_csv(CSV).dropna(subset=["ratio_vs_best"])
    plt.figure()
    # boxplot by algorithm
    algs = sorted(df["alg"].unique())
    data = [df[df["alg"] == a]["ratio_vs_best"].values for a in algs]
    plt.boxplot(data, tick_labels=algs, showmeans=True)
    plt.ylabel("bins / best_known_bins")
    plt.title("OR-Library 1D Bin Packing: Quality vs Best-Known")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT, dpi=200)
    plt.close()
    print("Wrote:", OUT)

if __name__ == "__main__":
    main()