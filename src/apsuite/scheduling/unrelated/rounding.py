from __future__ import annotations

import time
import numpy as np


def makespan_from_assignment(p: np.ndarray, assignment: list[int]) -> float:
    p = np.asarray(p, dtype=float)
    m, n = p.shape
    loads = np.zeros(m, dtype=float)
    for j, i in enumerate(assignment):
        loads[i] += p[i, j]
    return float(loads.max(initial=0.0))


def round_by_argmax_with_load_tiebreak(x: np.ndarray, p: np.ndarray) -> list[int]:
    """
    Deterministic rounding:
      choose machine i with largest x[i,j]
      tie-break: choose machine minimizing current_load[i] + p[i,j]
    """
    x = np.asarray(x, dtype=float)
    p = np.asarray(p, dtype=float)
    m, n = p.shape
    if x.shape != (m, n):
        raise ValueError(f"x must have shape {(m, n)}")

    loads = np.zeros(m, dtype=float)
    assignment = [-1] * n

    for j in range(n):
        col = x[:, j]
        best = float(np.max(col))
        cand = np.where(np.isclose(col, best, rtol=0.0, atol=1e-12))[0]
        if cand.size == 1:
            i = int(cand[0])
        else:
            i = int(cand[np.argmin(loads[cand] + p[cand, j])])

        assignment[j] = i
        loads[i] += p[i, j]

    return assignment


def local_improve_single_moves(
    assignment: list[int],
    p: np.ndarray,
    *,
    max_passes: int = 2,
    time_limit_s: float = 0.01,
) -> list[int]:
    """
    Tiny time-bounded local improvement:
      move a job off the critical machine if it reduces makespan.
    """
    p = np.asarray(p, dtype=float)
    m, n = p.shape
    if len(assignment) != n:
        raise ValueError("assignment length must equal number of jobs")

    a = assignment.copy()
    start = time.perf_counter()

    # compute initial loads
    loads = np.zeros(m, dtype=float)
    for j, i in enumerate(a):
        loads[i] += p[i, j]

    for _ in range(max_passes):
        if time.perf_counter() - start > time_limit_s:
            break

        improved = False
        crit = int(np.argmax(loads))
        C0 = float(loads.max(initial=0.0))

        jobs_on_crit = [j for j in range(n) if a[j] == crit]

        for j in jobs_on_crit:
            if time.perf_counter() - start > time_limit_s:
                break

            best_i = crit
            best_C = C0

            for i in range(m):
                if i == crit:
                    continue

                new_load_crit = loads[crit] - p[crit, j]
                new_load_i = loads[i] + p[i, j]

                other_max = 0.0
                for k in range(m):
                    if k == crit or k == i:
                        continue
                    if loads[k] > other_max:
                        other_max = float(loads[k])

                new_C = max(float(new_load_crit), float(new_load_i), other_max)

                if new_C + 1e-12 < best_C:
                    best_C = new_C
                    best_i = i

            if best_i != crit:
                old_i = a[j]
                a[j] = best_i
                loads[old_i] -= p[old_i, j]
                loads[best_i] += p[best_i, j]
                improved = True

        if not improved:
            break

    return a