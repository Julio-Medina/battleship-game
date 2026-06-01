from typing import Optional, Tuple

from battleship_ai.ai import HeuristicAI
from battleship_ai.board import Board, ShotResult
from battleship_ai.ship import Ship


Position = Tuple[int, int]


class Game:
    def __init__(self, width: int = 10, height: int = 10, seed: Optional[int] = None):
        self.player_board = Board(width, height)
        self.ai_board = Board(width, height)
        self.ai = HeuristicAI(width, height, seed=seed)

    def place_default_ships(self) -> None:
        self.player_board.place_ship(Ship(1, 1, 4))
        self.player_board.place_ship(Ship(3, 3, 3))
        self.player_board.place_ship(Ship(6, 5, 4))
        self.player_board.place_ship(Ship(2, 8, 4))

        self.ai_board.place_ship(Ship(1, 2, 4))
        self.ai_board.place_ship(Ship(4, 4, 3))
        self.ai_board.place_ship(Ship(2, 6, 4))
        self.ai_board.place_ship(Ship(6, 9, 4))

    def player_shoots(self, x: int, y: int) -> ShotResult:
        return self.ai_board.receive_shot(x, y)

    def ai_shoots(self) -> Tuple[Position, ShotResult]:
        shot = self.ai.next_shot()
        result = self.player_board.receive_shot(*shot)
        self.ai.record_result(shot, result)
        return shot, result

    @property
    def player_won(self) -> bool:
        return self.ai_board.all_sunk

    @property
    def ai_won(self) -> bool:
        return self.player_board.all_sunk
