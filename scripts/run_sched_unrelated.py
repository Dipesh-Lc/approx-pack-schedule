import numpy as np

from apsuite.scheduling.unrelated.types import UnrelatedInstance
from apsuite.scheduling.unrelated.lower_bounds import trivial_lb
from apsuite.scheduling.unrelated.algorithms import (
    lp_rounding, lp_rounding_with_info, greedy_baseline
)

def main():
    p = np.array([
        [10,  2,  8,  6,  7,  3],
        [ 4,  9,  3,  7,  2, 10],
        [ 6,  5,  9,  2,  8,  4],
    ], dtype=float)

    inst = UnrelatedInstance(p=p)
    lb_triv = trivial_lb(inst)

    # Baselines
    g = greedy_baseline(inst, order="minproc_desc")
    lp_plain = lp_rounding_with_info(inst, use_local_search=False)
    lp_ls = lp_rounding_with_info(inst, use_local_search=True, ls_time_limit_s=0.01)

    # Backwards compatible output (optional)
    T_star, C_round, _ = lp_rounding(inst)

    print("Processing times p[i,j] (m x n):")
    print(p)
    print()
    print(f"Trivial LB: {lb_triv:.4f}")
    print(f"LP optimum T*: {lp_plain.info['T_lp']:.4f}")
    print()

    print(f"{g.alg}: makespan={g.makespan:.4f}, ratio_vs_trivialLB={g.makespan/lb_triv:.4f}")
    print(f"{lp_plain.alg}: makespan={lp_plain.makespan:.4f}, ratio_vs_LP={lp_plain.info['ratio_vs_lp']:.4f}, gap_vs_LP={lp_plain.info['gap_vs_lp']:.4f}")
    print(f"{lp_ls.alg}: makespan={lp_ls.makespan:.4f}, ratio_vs_LP={lp_ls.info['ratio_vs_lp']:.4f}, gap_vs_LP={lp_ls.info['gap_vs_lp']:.4f}")
    print()
    print("LP solver info:", lp_plain.info["lp"])
    print()
    print("Back-compat lp_rounding():")
    print(f"  T*={T_star:.4f}, C={C_round:.4f}, ratio={C_round/T_star:.4f}")

if __name__ == "__main__":
    main()