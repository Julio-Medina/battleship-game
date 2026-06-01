from enum import Enum
from typing import List, Set, Tuple

from battleship_ai.ship import Ship


Position = Tuple[int, int]


class ShotResult(str, Enum):
    MISS = "miss"
    HIT = "hit"
    SUNK = "sunk"
    REPEATED = "repeated"


class Board:
    def __init__(self, width: int = 10, height: int = 10):
        if width <= 0 or height <= 0:
            raise ValueError("Board dimensions must be positive.")

        self.width = width
        self.height = height
        self.ships: List[Ship] = []
        self.shots: Set[Position] = set()

    def in_bounds(self, x: int, y: int) -> bool:
        return 1 <= x <= self.width and 1 <= y <= self.height

    def can_place_ship(self, ship: Ship) -> bool:
        if ship.size <= 0:
            return False

        for x, y in ship.positions:
            if not self.in_bounds(x, y):
                return False

            if any(existing.occupies(x, y) for existing in self.ships):
                return False

        return True

    def place_ship(self, ship: Ship) -> None:
        if not self.can_place_ship(ship):
            raise ValueError("Invalid ship placement.")

        self.ships.append(ship)

    def receive_shot(self, x: int, y: int) -> ShotResult:
        if not self.in_bounds(x, y):
            raise ValueError("Shot is outside the board.")

        if (x, y) in self.shots:
            return ShotResult.REPEATED

        self.shots.add((x, y))

        for ship in self.ships:
            if ship.hit(x, y):
                return ShotResult.SUNK if ship.is_sunk else ShotResult.HIT

        return ShotResult.MISS

    @property
    def all_sunk(self) -> bool:
        return bool(self.ships) and all(ship.is_sunk for ship in self.ships)
