from battleship_ai.board import Board
from battleship_ai.ship import Ship


def render_board(board: Board, reveal_ships: bool = False) -> str:
    lines = []

    header = "   " + " ".join(str(x) for x in range(1, board.width + 1))
    lines.append(header)

    ship_positions = _ship_positions(board)

    for y in range(1, board.height + 1):
        cells = []

        for x in range(1, board.width + 1):
            position = (x, y)

            if position in board.shots and position in ship_positions:
                cells.append("X")
            elif position in board.shots:
                cells.append("o")
            elif reveal_ships and position in ship_positions:
                cells.append("S")
            else:
                cells.append(".")

        lines.append(f"{y:2} " + " ".join(cells))

    return "\n".join(lines)


def _ship_positions(board: Board) -> set:
    positions = set()

    for ship in board.ships:
        positions.update(ship.positions)

    return positions
