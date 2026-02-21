from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import numpy as np

@dataclass(frozen=True)
class InstanceSpec:
    name: str
    n: int
    dist: str
    seed: int

def generate_instance(spec: InstanceSpec) -> List[float]:
    rng = np.random.default_rng(spec.seed)

    if spec.dist == "uniform":
        x = rng.random(spec.n)
    elif spec.dist == "bimodal":
        # half small, half large
        small = rng.uniform(0.05, 0.3, spec.n // 2)
        large = rng.uniform(0.6, 0.95, spec.n - spec.n // 2)
        x = np.concatenate([small, large])
        rng.shuffle(x)
    elif spec.dist == "heavy_tail":
        # Pareto-like then clipped to (0,1)
        y = (rng.pareto(a=2.0, size=spec.n) + 1.0)
        x = 1.0 / y
        x = np.clip(x, 0.01, 0.99)
    else:
        raise ValueError(f"Unknown dist: {spec.dist}")

    # Avoid tiny numerical weirdness; keep in (0,1)
    x = np.clip(x, 1e-6, 1 - 1e-6)
    return x.astype(float).tolist()