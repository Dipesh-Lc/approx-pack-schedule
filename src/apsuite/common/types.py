from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class PackingResult:
    # bins[b] is the list of item sizes in bin b (in insertion order)
    bins: List[List[float]]

    @property
    def num_bins(self) -> int:
        return len(self.bins)

    @property
    def loads(self) -> List[float]:
        return [sum(b) for b in self.bins]