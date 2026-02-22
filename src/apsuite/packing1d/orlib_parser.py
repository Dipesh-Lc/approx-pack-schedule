from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

@dataclass(frozen=True)
class OrlibBPPInstance:
    name: str
    source: str              # e.g. "binpack1.txt"
    capacity: float
    best_known_bins: int
    items: List[float]

def _nonempty_lines(path: Path) -> Iterable[str]:
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if s:
            yield s

def load_orlib_file(path: str | Path, normalize_capacity: bool = True) -> List[OrlibBPPInstance]:
    """
    OR-Library 1D bin packing format:
      P
      for each problem:
        identifier
        capacity n best_known
        n item sizes (one per line in the original files, but we parse token-wise)
    Format described on OR-Library page. :contentReference[oaicite:1]{index=1}
    """
    path = Path(path)
    lines = list(_nonempty_lines(path))
    if not lines:
        raise ValueError(f"Empty file: {path}")

    # First line: number of problems
    try:
        P = int(lines[0].split()[0])
    except Exception as e:
        raise ValueError(f"Cannot parse number of problems in {path}: {lines[0]!r}") from e

    idx = 1
    instances: List[OrlibBPPInstance] = []

    
    for _ in range(P):
        if idx >= len(lines):
            raise ValueError(f"Unexpected EOF while reading instance id in {path}")
        name = lines[idx].split()[0]
        idx += 1

        if idx >= len(lines):
            raise ValueError(f"Unexpected EOF while reading header for {name} in {path}")
        header_tokens = lines[idx].split()
        idx += 1
        if len(header_tokens) < 3:
            raise ValueError(f"Bad header line for {name} in {path}: {header_tokens}")
        
        source = path.name
        cap = float(header_tokens[0])
        n = int(header_tokens[1])
        best = int(header_tokens[2])

        # Read item sizes token-wise until we collect n items
        items: List[float] = []
        while len(items) < n:
            if idx >= len(lines):
                raise ValueError(f"Unexpected EOF while reading items for {name} in {path} "
                                 f"(got {len(items)} of {n})")
            for tok in lines[idx].split():
                if len(items) < n:
                    items.append(float(tok))
            idx += 1

        if normalize_capacity:
            items = [x / cap for x in items]
            cap_out = 1.0
        else:
            cap_out = cap

        instances.append(
            OrlibBPPInstance(
                name=name,
                source=source,
                capacity=cap_out,
                best_known_bins=best,
                items=items,
            )
        )

    return instances

def load_orlib_dir(dirpath: str | Path, normalize_capacity: bool = True) -> List[OrlibBPPInstance]:
    dirpath = Path(dirpath)
    paths = sorted(dirpath.glob("binpack*.txt"))
    if not paths:
        raise FileNotFoundError(f"No binpack*.txt found in {dirpath}")
    all_instances: List[OrlibBPPInstance] = []
    for p in paths:
        all_instances.extend(load_orlib_file(p, normalize_capacity=normalize_capacity))
    return all_instances