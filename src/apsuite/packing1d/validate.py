from __future__ import annotations
from typing import Iterable

def validate_items(items: Iterable[float], capacity: float = 1.0) -> list[float]:
    items = list(items)
    if capacity <= 0:
        raise ValueError("capacity must be > 0")
    if len(items) == 0:
        return []
    for x in items:
        if not isinstance(x, (int, float)):
            raise TypeError(f"item size must be numeric, got {type(x)}")
        if x <= 0:
            raise ValueError(f"item size must be > 0, got {x}")
        if x > capacity:
            raise ValueError(f"item size {x} exceeds capacity {capacity}")
    return [float(x) for x in items]