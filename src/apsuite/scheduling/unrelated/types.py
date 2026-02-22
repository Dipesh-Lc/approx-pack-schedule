from __future__ import annotations
from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass(frozen=True)
class UnrelatedInstance:
    # p[i, j] = processing time of job j on machine i
    p: np.ndarray  # shape (m, n)

    @property
    def m(self) -> int:
        return int(self.p.shape[0])

    @property
    def n(self) -> int:
        return int(self.p.shape[1])

@dataclass(frozen=True)
class Assignment:
    # assign[j] = machine index i
    assign: List[int]

    def makespan(self, inst: UnrelatedInstance) -> float:
        m, n = inst.m, inst.n
        loads = [0.0] * m
        for j in range(n):
            i = self.assign[j]
            loads[i] += float(inst.p[i, j])
        return max(loads)