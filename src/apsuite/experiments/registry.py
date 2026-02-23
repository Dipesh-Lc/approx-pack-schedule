from __future__ import annotations

from typing import Callable
import time
# -------------------------
# Packing 1D
# -------------------------
from apsuite.packing1d.instances import InstanceSpec, generate_instance
from apsuite.packing1d.lower_bounds import volume_lower_bound
from apsuite.packing1d import algorithms as p1d_algs

# -------------------------
# Packing 2D
# -------------------------
from apsuite.packing2d.instances import Instance2DSpec, generate_rectangles
from apsuite.packing2d.lower_bounds import area_lower_bound
from apsuite.packing2d.algorithms import shelf, guillotine, hybrid_shelf_guillotine

# -------------------------
# Scheduling: identical
# -------------------------
from apsuite.scheduling.identical.instances import IdenticalSchedSpec, generate_jobs
from apsuite.scheduling.identical.algorithms import list_scheduling, lpt
from apsuite.scheduling.identical.lower_bounds import lb_makespan_identical

# -------------------------
# Scheduling: unrelated
# -------------------------
from apsuite.scheduling.unrelated.instances import UnrelatedSpec, generate_unrelated
from apsuite.scheduling.unrelated.lower_bounds import trivial_lb
from apsuite.scheduling.unrelated.algorithms import (
    lp_rounding_with_info,
    greedy_baseline,
)


def _get_params(cfg: dict) -> dict:
    return cfg.get("params", {}) or {}


# ============================================================
# Packing 1D
# ============================================================

def run_packing1d(cfg: dict) -> list[dict]:
    rows: list[dict] = []
    grid = cfg["grid"]
    repetitions = int(cfg.get("repetitions", 1))
    base_seed = int(cfg.get("seed", 0))

    params = _get_params(cfg)
    capacity = float(params.get("capacity", 1.0))

    ALG_MAP: dict[str, Callable] = {
        "FF": p1d_algs.first_fit,
        "BF": p1d_algs.best_fit,
        "FFD": p1d_algs.first_fit_decreasing,
        "BFD": p1d_algs.best_fit_decreasing,
    }

    for dist in grid["dist"]:
        for n in grid["n"]:
            n = int(n)
            for rep in range(repetitions):
                seed = base_seed + rep

                spec = InstanceSpec(
                    name="synthetic",
                    n=n,
                    dist=dist,
                    seed=seed,
                )
                items = generate_instance(spec)
                lb = volume_lower_bound(items, capacity=capacity)

                for alg_name, alg in ALG_MAP.items():
                    t0 = time.perf_counter()
                    result = alg(items, capacity=capacity)
                    dt = time.perf_counter() - t0

                    rows.append({
                        "task": "packing1d",
                        "dist": dist,
                        "n": n,
                        "rep": rep,
                        "seed": seed,
                        "alg": alg_name,
                        "objective": result.num_bins,
                        "lb_trivial": lb,
                        "lp_T": None,
                        "ratio_vs_trivial_lb": result.num_bins / lb if lb > 0 else None,
                        "ratio_vs_lp": None,
                        "gap_vs_lp": None,
                        "runtime_s": dt,
                    })

    return rows


# ============================================================
# Packing 2D
# ============================================================

def run_packing2d(cfg: dict) -> list[dict]:
    rows: list[dict] = []
    grid = cfg["grid"]
    repetitions = int(cfg.get("repetitions", 1))
    base_seed = int(cfg.get("seed", 0))

    params = _get_params(cfg)
    W = float(params.get("W", 1.0))
    H = float(params.get("H", 1.0))

    ALG_MAP: dict[str, Callable] = {
        "SHELF": shelf,
        "GUILLOTINE": guillotine,
        "HYB(SHELF,GUIL)": hybrid_shelf_guillotine,
    }

    for dist in grid["dist"]:
        for n in grid["n"]:
            n = int(n)
            for rep in range(repetitions):
                seed = base_seed + rep

                spec = Instance2DSpec(
                    name="synthetic",
                    n=n,
                    dist=dist,
                    seed=seed,
                    W=W,
                    H=H,
                )

                rects = generate_rectangles(spec)
                lb = area_lower_bound(rects, W=W, H=H)

                for alg_name, alg in ALG_MAP.items():
                    t0 = time.perf_counter()
                    result = alg(rects, W=W, H=H)
                    dt = time.perf_counter() - t0
                    rows.append({
                        "task": "packing2d",
                        "dist": dist,
                        "n": n,
                        "rep": rep,
                        "seed": seed,
                        "alg": alg_name,
                        "objective": result.num_bins,
                        "lb_trivial": lb,
                        "lp_T": None,
                        "ratio_vs_trivial_lb": result.num_bins / lb if lb > 0 else None,
                        "ratio_vs_lp": None,
                        "gap_vs_lp": None,
                        "runtime_s": dt,
                    })

    return rows


# ============================================================
# Scheduling: Identical Machines
# ============================================================

def run_sched_identical(cfg: dict) -> list[dict]:
    rows: list[dict] = []
    grid = cfg["grid"]
    repetitions = int(cfg.get("repetitions", 1))
    base_seed = int(cfg.get("seed", 0))

    for dist in grid["dist"]:
        for n in grid["n"]:
            n = int(n)
            for m in grid["m"]:
                m = int(m)
                for rep in range(repetitions):
                    seed = base_seed + rep

                    spec = IdenticalSchedSpec(
                        n=n,
                        m=m,
                        dist=dist,
                        seed=seed,
                    )
                    jobs = generate_jobs(spec)
                    lb = lb_makespan_identical(jobs, m=m)

                    for alg_name, alg in {
                        "LIST": list_scheduling,
                        "LPT": lpt,
                    }.items():
                        t0 = time.perf_counter()
                        result = alg(jobs, m=m)
                        dt = time.perf_counter() - t0

                        rows.append({
                            "task": "sched_identical",
                            "dist": dist,
                            "n": n,
                            "m": m,
                            "rep": rep,
                            "seed": seed,
                            "alg": alg_name,
                            "objective": result.makespan,
                            "lb_trivial": lb,
                            "lp_T": None,
                            "ratio_vs_trivial_lb": result.makespan / lb if lb > 0 else None,
                            "ratio_vs_lp": None,
                            "gap_vs_lp": None,
                            "runtime_s": dt,
                        })

    return rows


# ============================================================
# Scheduling: Unrelated Machines
# ============================================================

def run_sched_unrelated(cfg: dict) -> list[dict]:
    rows: list[dict] = []
    grid = cfg["grid"]
    repetitions = int(cfg.get("repetitions", 1))
    base_seed = int(cfg.get("seed", 0))

    params = _get_params(cfg)
    ls_time_limit_s = float(params.get("ls_time_limit_s", 0.01))

    for dist in grid["dist"]:
        for n in grid["n"]:
            n = int(n)
            for m in grid["m"]:
                m = int(m)
                for rep in range(repetitions):
                    seed = base_seed + rep

                    inst = generate_unrelated(
                        UnrelatedSpec(n=n, m=m, dist=dist, seed=seed)
                    )

                    lb = trivial_lb(inst)

                    # ---------------- GREEDY ----------------
                    g = greedy_baseline(inst)
                    rows.append({
                        "task": "sched_unrelated",
                        "dist": dist,
                        "n": n,
                        "m": m,
                        "rep": rep,
                        "seed": seed,
                        "alg": g.alg,
                        "objective": g.makespan,
                        "lb_trivial": lb,
                        "lp_T": None,
                        "ratio_vs_trivial_lb": g.makespan / lb if lb > 0 else None,
                        "ratio_vs_lp": None,
                        "gap_vs_lp": None,
                        "runtime_s": g.info["runtime_s"],
                    })

                    # ---------------- LP_ROUND ----------------
                    r0 = lp_rounding_with_info(
                        inst,
                        use_local_search=False,
                    )
                    lp_T0 = r0.info.get("lp_T", r0.info.get("T_lp"))

                    rows.append({
                        "task": "sched_unrelated",
                        "dist": dist,
                        "n": n,
                        "m": m,
                        "rep": rep,
                        "seed": seed,
                        "alg": "LP_ROUND",
                        "objective": r0.makespan,
                        "lb_trivial": lb,
                        "lp_T": lp_T0,
                        "ratio_vs_trivial_lb": r0.makespan / lb if lb > 0 else None,
                        "ratio_vs_lp": r0.info["ratio_vs_lp"],
                        "gap_vs_lp": r0.info["gap_vs_lp"],
                        "runtime_s": r0.info["total_runtime_s"],
                    })

                    # ---------------- LP_ROUND+LS ----------------
                    r1 = lp_rounding_with_info(
                        inst,
                        use_local_search=True,
                        ls_time_limit_s=ls_time_limit_s,
                    )
                    lp_T1 = r1.info.get("lp_T", r1.info.get("T_lp"))

                    rows.append({
                        "task": "sched_unrelated",
                        "dist": dist,
                        "n": n,
                        "m": m,
                        "rep": rep,
                        "seed": seed,
                        "alg": "LP_ROUND+LS",
                        "objective": r1.makespan,
                        "lb_trivial": lb,
                        "lp_T": lp_T1,
                        "ratio_vs_trivial_lb": r1.makespan / lb if lb > 0 else None,
                        "ratio_vs_lp": r1.info["ratio_vs_lp"],
                        "gap_vs_lp": r1.info["gap_vs_lp"],
                        "runtime_s": r1.info["total_runtime_s"],
                    })

    return rows


# ============================================================
# Registry
# ============================================================

REGISTRY: dict[str, Callable[[dict], list[dict]]] = {
    "packing1d": run_packing1d,
    "packing2d": run_packing2d,
    "sched_identical": run_sched_identical,
    "sched_unrelated": run_sched_unrelated,
}