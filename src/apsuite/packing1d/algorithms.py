from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

from apsuite.common.types import PackingResult
from apsuite.packing1d.validate import validate_items


def first_fit(items: List[float], capacity: float = 1.0) -> PackingResult:
    """First-Fit bin packing.
    Place each item into the first bin where it fits; open a new bin otherwise.
    """
    items = validate_items(items, capacity)

    bins: List[List[float]] = []
    remaining: List[float] = []  # remaining capacity per bin

    for x in items:
        placed = False
        for b in range(len(bins)):
            if remaining[b] >= x:
                bins[b].append(x)
                remaining[b] -= x
                placed = True
                break
        if not placed:
            bins.append([x])
            remaining.append(capacity - x)

    return PackingResult(bins=bins)


def best_fit(items: List[float], capacity: float = 1.0) -> PackingResult:
    """Best-Fit bin packing.
    Place each item into the bin that will have the least remaining capacity after placement.
    Open a new bin if no bin can fit the item.
    """
    items = validate_items(items, capacity)

    bins: List[List[float]] = []
    remaining: List[float] = []

    for x in items:
        best_bin = None
        best_rem_after = None  # smaller is better

        for b in range(len(bins)):
            if remaining[b] >= x:
                rem_after = remaining[b] - x
                if best_rem_after is None or rem_after < best_rem_after:
                    best_rem_after = rem_after
                    best_bin = b

        if best_bin is None:
            bins.append([x])
            remaining.append(capacity - x)
        else:
            bins[best_bin].append(x)
            remaining[best_bin] -= x

    return PackingResult(bins=bins)    


def first_fit_decreasing(items: List[float], capacity: float = 1.0) -> PackingResult:
    items = validate_items(items, capacity)
    items_sorted = sorted(items, reverse=True)
    return first_fit(items_sorted, capacity=capacity)

def best_fit_decreasing(items: List[float], capacity: float = 1.0) -> PackingResult:
    items = validate_items(items, capacity)
    items_sorted = sorted(items, reverse=True)
    return best_fit(items_sorted, capacity=capacity)