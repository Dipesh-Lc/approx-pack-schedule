import numpy as np
from apsuite.scheduling.unrelated.types import UnrelatedInstance
from apsuite.scheduling.unrelated.lp import solve_lp_makespan_info

def test_lp_info_returns_metadata():
    p = np.array([[2, 3, 4],
                  [3, 2, 5]], dtype=float)
    inst = UnrelatedInstance(p=p)
    T, X, info = solve_lp_makespan_info(inst)
    assert X.shape == (2, 3)
    assert T >= 0.0
    assert info.success is True
    assert info.runtime_s >= 0.0