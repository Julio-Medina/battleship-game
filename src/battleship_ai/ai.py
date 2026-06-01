import random
from typing import List, Optional, Set, Tuple

from battleship_ai.board import ShotResult


Position = Tuple[int, int]


class HeuristicAI:
    """
    Rule-based Battleship AI.

    Strategy:
    - If there is no active target, shoot randomly.
    - After a hit, store that position as a target.
    - Try neighboring cells around known hits.
    - Avoid repeated shots.
    """

    def __init__(self, width: int = 10, height: int = 10, seed: Optional[int] = None):
        if width <= 0 or height <= 0:
            raise ValueError("Board dimensions must be positive.")

        self.width = width
        self.height = height
        self.shots_taken: Set[Position] = set()
        self.hits_not_sunk: List[Position] = []
        self.random = random.Random(seed)

    def next_shot(self) -> Position:
        candidates = self._target_candidates()

        if candidates:
            shot = candidates[0]
        else:
            shot = self._random_untried_position()

        self.shots_taken.add(shot)
        return shot

    def record_result(self, position: Position, result: ShotResult) -> None:
        if result == ShotResult.HIT:
            if position not in self.hits_not_sunk:
                self.hits_not_sunk.append(position)

        elif result == ShotResult.SUNK:
            self.hits_not_sunk.clear()

    def _target_candidates(self) -> List[Position]:
        candidates: List[Position] = []

        for x, y in self.hits_not_sunk:
            neighbors = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            ]

            for candidate in neighbors:
                if self._is_available(candidate):
                    candidates.append(candidate)

        return candidates

    def _random_untried_position(self) -> Position:
        available = [
            (x, y)
            for y in range(1, self.height + 1)
            for x in range(1, self.width + 1)
            if (x, y) not in self.shots_taken
        ]

        if not available:
            raise RuntimeError("No available shots remain.")

        return self.random.choice(available)

    def _is_available(self, position: Position) -> bool:
        x, y = position

        return (
            1 <= x <= self.width
            and 1 <= y <= self.height
            and position not in self.shots_taken
        )
