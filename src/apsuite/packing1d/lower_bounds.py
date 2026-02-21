from __future__ import annotations
import math
from typing import Sequence

from apsuite.packing1d.validate import validate_items

def volume_lower_bound(items: Sequence[float], capacity: float = 1.0) -> int:
    """Simple lower bound: ceil(sum(items)/capacity)."""
    items = validate_items(items, capacity)
    if not items:
        return 0
    return int(math.ceil(sum(items) / capacity))

def half_item_lower_bound(items, capacity: float = 1.0) -> int:
    items = validate_items(items, capacity)
    if not items:
        return 0
    return sum(1 for x in items if x > capacity / 2)

def combined_lower_bound(items, capacity: float = 1.0) -> int:
    return max(volume_lower_bound(items, capacity), half_item_lower_bound(items, capacity))