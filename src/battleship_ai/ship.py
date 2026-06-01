from dataclasses import dataclass, field
from typing import List, Set, Tuple


Position = Tuple[int, int]


@dataclass
class Ship:
    x: int
    y: int
    size: int
    hits: Set[Position] = field(default_factory=set)

    @property
    def positions(self) -> List[Position]:
        return [(self.x + offset, self.y) for offset in range(self.size)]

    def occupies(self, x: int, y: int) -> bool:
        return (x, y) in self.positions

    def hit(self, x: int, y: int) -> bool:
        if not self.occupies(x, y):
            return False

        self.hits.add((x, y))
        return True

    @property
    def is_sunk(self) -> bool:
        return len(self.hits) == self.size
