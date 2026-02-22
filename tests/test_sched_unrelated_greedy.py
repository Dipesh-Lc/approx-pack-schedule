import numpy as np
from apsuite.scheduling.unrelated.greedy import greedy_minload

def test_greedy_minload_basic_shapes():
    p = np.array([
        [3, 2, 7],
        [4, 1, 3],
    ], dtype=float)  # m=2,n=3

    sched = greedy_minload(p, order="as_is")
    assert len(sched.assignment) == 3
    assert sched.loads.shape == (2,)
    assert sched.makespan == max(sched.loads)

def test_greedy_respects_processing_times():
    p = np.array([
        [10, 1],
        [1, 10],
    ], dtype=float)

    sched = greedy_minload(p, order="as_is")
    # Each job should go to its fast machine
    assert sched.assignment[0] == 1
    assert sched.assignment[1] == 0
    assert sched.makespan == 1.0