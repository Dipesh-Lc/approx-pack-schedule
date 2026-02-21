from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from apsuite.common.types import PackingResult

@dataclass(frozen=True)
class PackingMetrics:
    num_bins: int
    lower_bound: int
    approx_ratio_vs_lb: Optional[float]  # None if LB=0
    gap_vs_lb: Optional[float]           # (bins-LB)/LB, None if LB=0

def packing_metrics(result: PackingResult, lower_bound: int) -> PackingMetrics:
    b = result.num_bins
    lb = int(lower_bound)
    if lb <= 0:
        return PackingMetrics(num_bins=b, lower_bound=lb,
                             approx_ratio_vs_lb=None, gap_vs_lb=None)
    return PackingMetrics(
        num_bins=b,
        lower_bound=lb,
        approx_ratio_vs_lb=b / lb,
        gap_vs_lb=(b - lb) / lb,
    )