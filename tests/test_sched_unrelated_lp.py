import numpy as np
from apsuite.scheduling.unrelated.types import UnrelatedInstance
from apsuite.scheduling.unrelated.lp import solve_lp_makespan
from apsuite.scheduling.unrelated.algorithms import lp_rounding

def test_lp_solution_shapes():
    p = np.array([[2, 3, 4],
                  [3, 2, 5]], dtype=float)  # m=2, n=3
    inst = UnrelatedInstance(p=p)
    T, X = solve_lp_makespan(inst)
    assert X.shape == (2, 3)
    assert T >= 0.0

def test_lp_rounding_makespan_ge_T():
    p = np.array([[2, 3, 4],
                  [3, 2, 5]], dtype=float)
    inst = UnrelatedInstance(p=p)
    T_star, C, _ = lp_rounding(inst)
    assert C + 1e-12 >= T_star  # integral schedule can't beat relaxation