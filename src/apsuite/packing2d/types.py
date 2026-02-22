from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass(frozen=True)
class Rect:
    w: float
    h: float
    id: Optional[int] = None  # optional identifier

@dataclass(frozen=True)
class Bin2D:
    # list of placed rectangles: (rect, x, y)
    placements: List[Tuple[Rect, float, float]]

@dataclass(frozen=True)
class Packing2DResult:
    bins: List[Bin2D]

    @property
    def num_bins(self) -> int:
        return len(self.bins)