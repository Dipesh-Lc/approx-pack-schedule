from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Tuple

import numpy as np
from scipy.optimize import linprog

from apsuite.scheduling.unrelated.types import UnrelatedInstance


@dataclass(frozen=True)
class LPInfo:
    success: bool
    status: int
    message: str
    nit: int | None
    method: str
    runtime_s: float


def solve_lp_makespan(inst: UnrelatedInstance) -> Tuple[float, np.ndarray]:
    """
    Backwards-compatible API.
    Returns (T*, X) where X has shape (m,n).
    """
    T, X, _ = solve_lp_makespan_info(inst)
    return T, X


def solve_lp_makespan_info(inst: UnrelatedInstance, *, method: str = "highs") -> Tuple[float, np.ndarray, LPInfo]:
    """
    Solve LP relaxation for unrelated machines makespan.
    Returns (T*, X, info) where X has shape (m,n).
    """
    m, n = inst.m, inst.n
    p = np.asarray(inst.p, dtype=float)

    # Variable vector: [x_00, x_01, ..., x_(m-1,n-1), T]
    num_x = m * n
    T_idx = num_x
    dim = num_x + 1

    c = np.zeros(dim, dtype=float)
    c[T_idx] = 1.0  # minimize T

    # Equality constraints: for each job j, sum_i x_ij = 1
    A_eq = np.zeros((n, dim), dtype=float)
    b_eq = np.ones(n, dtype=float)
    for j in range(n):
        for i in range(m):
            A_eq[j, i * n + j] = 1.0

    # Inequalities: for each machine i, sum_j p_ij x_ij - T <= 0
    A_ub = np.zeros((m, dim), dtype=float)
    b_ub = np.zeros(m, dtype=float)
    for i in range(m):
        A_ub[i, i * n:(i + 1) * n] = p[i, :]
        A_ub[i, T_idx] = -1.0

    # Bounds: x_ij >= 0, T >= 0
    # (No need for upper bound 1; equality constraints imply x_ij <= 1 in feasible solutions.)
    bounds = [(0.0, None)] * num_x + [(0.0, None)]

    t0 = time.perf_counter()
    res = linprog(
        c=c,
        A_ub=A_ub, b_ub=b_ub,
        A_eq=A_eq, b_eq=b_eq,
        bounds=bounds,
        method=method,
    )
    t1 = time.perf_counter()

    info = LPInfo(
        success=bool(res.success),
        status=int(getattr(res, "status", -1)),
        message=str(getattr(res, "message", "")),
        nit=getattr(res, "nit", None),
        method=method,
        runtime_s=float(t1 - t0),
    )

    if not res.success or res.x is None:
        raise RuntimeError(f"LP failed: {info}")

    sol = np.asarray(res.x, dtype=float)
    T_star = float(sol[T_idx])
    X = sol[:num_x].reshape(m, n)

    # numerical cleanup
    X = np.maximum(X, 0.0)

    return T_star, X, info