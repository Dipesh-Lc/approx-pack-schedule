from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class UnrelatedSchedule:
    assignment: list[int]   # length n, job -> machine
    loads: np.ndarray       # shape (m,)
    makespan: float

def greedy_minload(
    p: np.ndarray,
    *,
    order: str = "minproc_desc",
) -> UnrelatedSchedule:
    """
    Greedy for unrelated machines: assign each job to machine minimizing
    current_load[i] + p[i,j].

    p: shape (m, n)
    order:
      - 'as_is'
      - 'minproc_desc' : sort jobs by decreasing min_i p[i,j]
      - 'maxproc_desc' : sort jobs by decreasing max_i p[i,j]
    """
    p = np.asarray(p, dtype=float)
    m, n = p.shape
    loads = np.zeros(m, dtype=float)
    assignment = [-1] * n

    jobs = np.arange(n)
    if order == "minproc_desc":
        jobs = jobs[np.argsort(np.min(p, axis=0))[::-1]]
    elif order == "maxproc_desc":
        jobs = jobs[np.argsort(np.max(p, axis=0))[::-1]]
    elif order != "as_is":
        raise ValueError(f"Unknown order: {order}")

    for j in jobs:
        i = int(np.argmin(loads + p[:, j]))
        assignment[j] = i
        loads[i] += p[i, j]

    return UnrelatedSchedule(
        assignment=assignment,
        loads=loads,
        makespan=float(loads.max(initial=0.0)),
    )