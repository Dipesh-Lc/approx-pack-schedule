from __future__ import annotations
import numpy as np
from apsuite.scheduling.unrelated.types import UnrelatedInstance

def trivial_lb(inst: UnrelatedInstance) -> float:
    """
    Two simple lower bounds (valid for any assignment):
    1) max_j min_i p_ij  (each job must be processed somewhere)
    2) (sum_j min_i p_ij) / m  (load average using cheapest machine per job)
    """
    p = inst.p
    m, n = p.shape
    mins = p.min(axis=0)  # min over machines for each job
    return float(max(mins.max(), mins.sum() / m))