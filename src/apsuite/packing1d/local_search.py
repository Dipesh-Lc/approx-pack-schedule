from __future__ import annotations

from typing import List, Tuple

from apsuite.common.types import PackingResult


def _remaining_capacities(bins: List[List[float]], capacity: float) -> List[float]:
    return [capacity - sum(b) for b in bins]


def try_eliminate_one_bin(
    bins: List[List[float]],
    capacity: float = 1.0,
    max_passes: int = 2,
) -> Tuple[bool, List[List[float]]]:
    """
    Try to eliminate a single bin by moving all its items into other bins.
    Strategy:
      - pick a candidate bin (smallest load)
      - try to place its items one-by-one into other bins (best-fit style)
      - if successful, remove the emptied bin

    Returns:
      (improved, new_bins)
    """
    if len(bins) <= 1:
        return False, bins

    # Choose candidate: smallest load bin (easiest to empty)
    loads = [sum(b) for b in bins]
    cand_idx = min(range(len(bins)), key=lambda i: loads[i])
    candidate_items = sorted(bins[cand_idx], reverse=True)  # place big first

    # Create a working copy without the candidate bin
    new_bins = [b.copy() for i, b in enumerate(bins) if i != cand_idx]
    rem = _remaining_capacities(new_bins, capacity)

    # Attempt to place all candidate items into remaining bins
    for x in candidate_items:
        best_bin = None
        best_rem_after = None
        for j in range(len(new_bins)):
            if rem[j] >= x:
                ra = rem[j] - x
                if best_rem_after is None or ra < best_rem_after:
                    best_rem_after = ra
                    best_bin = j
        if best_bin is None:
            # Failed to place one item => cannot eliminate this candidate bin
            return False, bins
        new_bins[best_bin].append(x)
        rem[best_bin] -= x

    # Success: candidate bin eliminated
    return True, new_bins


def local_improve_eliminate_bins(
    result: PackingResult,
    capacity: float = 1.0,
    max_rounds: int = 50,
    max_passes_per_round: int = 2,
) -> PackingResult:
    """
    Repeatedly attempt to eliminate bins.
    Stops when no bin can be eliminated or max_rounds reached.
    """
    bins = [b.copy() for b in result.bins]

    rounds = 0
    improved_any = False
    while rounds < max_rounds:
        improved, bins2 = try_eliminate_one_bin(
            bins, capacity=capacity, max_passes=max_passes_per_round
        )
        if not improved:
            break
        bins = bins2
        improved_any = True
        rounds += 1

    if improved_any:
        # optional: stable ordering (not necessary but helps reproducibility)
        bins = [sorted(b, reverse=True) for b in bins]

    return PackingResult(bins=bins)