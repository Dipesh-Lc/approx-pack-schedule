import numpy as np
from apsuite.scheduling.unrelated.rounding import (
    round_by_argmax_with_load_tiebreak,
    makespan_from_assignment,
    local_improve_single_moves,
)

def test_rounding_returns_valid_assignment():
    p = np.array([[3,2,7],[4,1,3]], dtype=float)
    x = np.array([[0.2,0.9,0.1],[0.8,0.1,0.9]], dtype=float)  # shape (2,3)
    a = round_by_argmax_with_load_tiebreak(x, p)
    assert len(a) == p.shape[1]
    assert all(0 <= i < p.shape[0] for i in a)

def test_local_search_never_worsens_makespan_simple():
    p = np.array([[10,1],[1,10]], dtype=float)
    a0 = [0,0]  # terrible assignment
    C0 = makespan_from_assignment(p, a0)
    a1 = local_improve_single_moves(a0, p, time_limit_s=0.01)
    C1 = makespan_from_assignment(p, a1)
    assert C1 <= C0 + 1e-12