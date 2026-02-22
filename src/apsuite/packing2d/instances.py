from __future__ import annotations
from dataclasses import dataclass
from typing import List
import numpy as np

from apsuite.packing2d.types import Rect

@dataclass(frozen=True)
class Instance2DSpec:
    name: str
    n: int
    dist: str
    seed: int
    W: float
    H: float

def generate_rectangles(spec: Instance2DSpec) -> List[Rect]:
    rng = np.random.default_rng(spec.seed)
    n = spec.n
    W, H = spec.W, spec.H

    if spec.dist == "uniform":
        # random rectangles with widths/heights in (0,1) scaled to bin size
        w = rng.uniform(0.05, 0.8, n) * W
        h = rng.uniform(0.05, 0.8, n) * H

    elif spec.dist == "bimodal":
        # mix of "flat wide" and "tall narrow" rectangles
        n1 = n // 2
        n2 = n - n1
        w1 = rng.uniform(0.4, 0.9, n1) * W
        h1 = rng.uniform(0.05, 0.3, n1) * H
        w2 = rng.uniform(0.05, 0.3, n2) * W
        h2 = rng.uniform(0.4, 0.9, n2) * H
        w = np.concatenate([w1, w2])
        h = np.concatenate([h1, h2])
        idx = rng.permutation(n)
        w, h = w[idx], h[idx]

    elif spec.dist == "heavy_tail":
        # many small rectangles, few larger ones
        a = rng.pareto(a=2.0, size=n) + 1.0
        w = (1.0 / a) * 0.95 * W
        b = rng.pareto(a=2.0, size=n) + 1.0
        h = (1.0 / b) * 0.95 * H
        w = np.clip(w, 0.02 * W, 0.95 * W)
        h = np.clip(h, 0.02 * H, 0.95 * H)

    else:
        raise ValueError(f"Unknown dist: {spec.dist}")

    rects = [Rect(float(w[i]), float(h[i]), id=i) for i in range(n)]
    return rects