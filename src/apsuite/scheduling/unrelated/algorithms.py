from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import numpy as np

from apsuite.scheduling.unrelated.types import UnrelatedInstance, Assignment
from apsuite.scheduling.unrelated.lp import solve_lp_makespan, solve_lp_makespan_info
from apsuite.scheduling.unrelated.rounding import (
    round_by_argmax_with_load_tiebreak,
    local_improve_single_moves,
    makespan_from_assignment,
)
from apsuite.scheduling.unrelated.greedy import greedy_minload


@dataclass(frozen=True)
class AlgoResult:
    alg: str
    makespan: float
    assignment: list[int]
    info: dict[str, Any]


def lp_rounding(inst: UnrelatedInstance) -> tuple[float, float, Assignment]:
    """
    Backwards-compatible function used by your existing scripts/tests.
    Returns (T_star, C_round, Assignment)
    """
    T_star, X = solve_lp_makespan(inst)
    a = round_by_argmax_with_load_tiebreak(X, inst.p)
    C = makespan_from_assignment(inst.p, a)
    return T_star, C, Assignment(assign=a)


def lp_rounding_with_info(inst: UnrelatedInstance, *, use_local_search: bool, ls_time_limit_s: float = 0.01) -> AlgoResult:
    """
    Enhanced Phase-4 runner for experiments:
      LP -> rounding -> optional local search
    """
    T_star, X, lp_info = solve_lp_makespan_info(inst)

    t0 = time.perf_counter()
    a0 = round_by_argmax_with_load_tiebreak(X, inst.p)
    C0 = makespan_from_assignment(inst.p, a0)
    t1 = time.perf_counter()

    a = a0
    C = C0
    ls_info = None
    if use_local_search:
        t2 = time.perf_counter()
        a1 = local_improve_single_moves(a0, inst.p, time_limit_s=ls_time_limit_s)
        C1 = makespan_from_assignment(inst.p, a1)
        t3 = time.perf_counter()
        ls_info = {"runtime_s": float(t3 - t2), "time_limit_s": ls_time_limit_s}
        a, C = a1, C1

    info = {
        "T_lp": T_star,
        "ratio_vs_lp": float(C / T_star) if T_star > 0 else None,
        "gap_vs_lp": float((C - T_star) / T_star) if T_star > 0 else None,
        "lp": lp_info.__dict__,
        "round_runtime_s": float(t1 - t0),
        "ls": ls_info,
        "total_runtime_s": float(lp_info.runtime_s + (t1 - t0) + ((ls_info["runtime_s"]) if ls_info else 0.0)),
    }
    return AlgoResult(alg=("LP+LS" if use_local_search else "LP"), makespan=C, assignment=a, info=info)


def greedy_baseline(inst: UnrelatedInstance, *, order: str = "minproc_desc") -> AlgoResult:
    t0 = time.perf_counter()
    sched = greedy_minload(inst.p, order=order)
    t1 = time.perf_counter()
    info = {"runtime_s": float(t1 - t0), "order": order}
    return AlgoResult(alg=f"GREEDY({order})", makespan=sched.makespan, assignment=sched.assignment, info=info)