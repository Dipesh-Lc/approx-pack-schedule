import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

FIGDIR_NAME = "figures"

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def plot_hist(df, value_col, title, outpath, by="alg", bins=40):
    plt.figure()
    for key, d in df.groupby(by):
        plt.hist(d[value_col].dropna(), bins=bins, alpha=0.5, label=str(key))
    plt.xlabel(value_col)
    plt.ylabel("count")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

def plot_scaling(df, x="n", y="ratio", title="", outpath="", group_cols=("dist","alg")):
    plt.figure()
    for keys, d in df.groupby(list(group_cols)):
        keys = keys if isinstance(keys, tuple) else (keys,)
        label = ",".join([str(k) for k in keys])
        s = d.groupby(x)[y].mean().sort_index()
        plt.plot(s.index, s.values, marker="o", label=label)

    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

def plot_runtime(df, x="n", title="", outpath="", group_cols=("dist","alg")):
    plt.figure()
    for keys, d in df.groupby(list(group_cols)):
        keys = keys if isinstance(keys, tuple) else (keys,)
        label = ",".join([str(k) for k in keys])
        s = d.groupby(x)["runtime_s"].mean().sort_index()
        plt.plot(s.index, s.values, marker="o", label=label)

    plt.xlabel(x)
    plt.ylabel("runtime_s (mean)")
    plt.title(title)
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp_dir", required=True, help="e.g., results/experiments/packing1d_scale")
    args = ap.parse_args()

    csv_path = os.path.join(args.exp_dir, "results.csv")
    df = pd.read_csv(csv_path)

    fig_dir = os.path.join(args.exp_dir, FIGDIR_NAME)
    ensure_dir(fig_dir)

    task = df["task"].iloc[0]
    print("Task:", task)

    # unify "ratio" column
    if task in ("packing1d", "packing2d", "sched_identical"):
        # ratio vs trivial LB is the meaningful one here
        df["ratio"] = df["ratio_vs_trivial_lb"]
        ratio_name = "ratio_vs_trivial_lb"
        group_cols = ("dist", "alg")
        xcol = "n"
    elif task == "sched_unrelated":
        # Use ratio_vs_lp for LP algs; otherwise ratio_vs_trivial_lb for greedy
        df_lp = df[df["ratio_vs_lp"].notna()].copy()
        df_lp["ratio"] = df_lp["ratio_vs_lp"]
        ratio_name = "ratio_vs_lp"
        group_cols = ("dist", "alg")
        xcol = "n"
    else:
        raise ValueError(f"Unknown task: {task}")

    # 1) scaling curves (ratio vs n)
    if task != "sched_unrelated":
        plot_scaling(
            df.dropna(subset=["ratio"]),
            x=xcol,
            y="ratio",
            title=f"{task}: mean {ratio_name} vs n",
            outpath=os.path.join(fig_dir, f"{task}_ratio_vs_n.png"),
            group_cols=group_cols,
        )
        plot_runtime(
            df,
            x=xcol,
            title=f"{task}: mean runtime vs n",
            outpath=os.path.join(fig_dir, f"{task}_runtime_vs_n.png"),
            group_cols=group_cols,
        )
        plot_hist(
            df.dropna(subset=["ratio"]),
            value_col="ratio",
            title=f"{task}: histogram of {ratio_name}",
            outpath=os.path.join(fig_dir, f"{task}_ratio_hist.png"),
            by="alg",
        )
    else:
        # unrelated: plot LP-only ratio curves + runtime for all
        plot_scaling(
            df_lp.dropna(subset=["ratio"]),
            x=xcol,
            y="ratio",
            title=f"{task}: mean ratio_vs_lp vs n (LP algs)",
            outpath=os.path.join(fig_dir, f"{task}_ratio_vs_n_lp.png"),
            group_cols=("dist", "alg"),
        )
        plot_runtime(
            df,
            x=xcol,
            title=f"{task}: mean runtime vs n",
            outpath=os.path.join(fig_dir, f"{task}_runtime_vs_n.png"),
            group_cols=("dist", "alg"),
        )
        plot_hist(
            df_lp.dropna(subset=["ratio"]),
            value_col="ratio",
            title=f"{task}: histogram of ratio_vs_lp (LP algs)",
            outpath=os.path.join(fig_dir, f"{task}_ratio_hist_lp.png"),
            by="alg",
        )

    print("Wrote figures to:", fig_dir)

if __name__ == "__main__":
    main()