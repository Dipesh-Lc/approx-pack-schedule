from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from apsuite.scheduling.unrelated.types import UnrelatedInstance

@dataclass(frozen=True)
class UnrelatedSpec:
    n: int
    m: int
    dist: str
    seed: int

def generate_unrelated(spec: UnrelatedSpec) -> UnrelatedInstance:
    rng = np.random.default_rng(spec.seed)
    m, n = spec.m, spec.n

    if spec.dist == "lognormal_machines":
        # machine speeds: each machine i has speed s_i > 0
        speeds = rng.lognormal(mean=0.0, sigma=0.6, size=m)  # heterogeneous speeds
        base = rng.uniform(1.0, 100.0, size=n)
        # p[i,j] = base[j] / speed[i] * noise
        noise = rng.uniform(0.8, 1.2, size=(m, n))
        p = (base[None, :] / speeds[:, None]) * noise

    elif spec.dist == "random_matrix":
        # fully unrelated: each p_ij independent
        p = rng.uniform(1.0, 100.0, size=(m, n))

    elif spec.dist == "bimodal_jobs":
        base = rng.choice([10.0, 80.0], size=n, p=[0.6, 0.4])
        speeds = rng.uniform(0.5, 2.0, size=m)
        noise = rng.uniform(0.9, 1.1, size=(m, n))
        p = (base[None, :] / speeds[:, None]) * noise

    else:
        raise ValueError(f"Unknown dist: {spec.dist}")

    return UnrelatedInstance(p=p.astype(float))