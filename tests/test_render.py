from battleship_ai.board import Board
from battleship_ai.render import render_board
from battleship_ai.ship import Ship


def test_render_empty_board():
    board = Board(width=3, height=2)

    rendered = render_board(board)

    assert rendered == "   1 2 3\n 1 . . .\n 2 . . ."


def test_render_reveals_ships_when_enabled():
    board = Board(width=3, height=2)
    board.place_ship(Ship(1, 1, 2))

    rendered = render_board(board, reveal_ships=True)

    assert rendered == "   1 2 3\n 1 S S .\n 2 . . ."


def test_render_hides_ships_when_disabled():
    board = Board(width=3, height=2)
    board.place_ship(Ship(1, 1, 2))

    rendered = render_board(board, reveal_ships=False)

    assert rendered == "   1 2 3\n 1 . . .\n 2 . . ."


def test_render_shows_miss():
    board = Board(width=3, height=2)
    board.receive_shot(3, 2)

    rendered = render_board(board)

    assert rendered == "   1 2 3\n 1 . . .\n 2 . . o"


def test_render_shows_hit():
    board = Board(width=3, height=2)
    board.place_ship(Ship(1, 1, 2))
    board.receive_shot(1, 1)

    rendered = render_board(board, reveal_ships=True)

    assert rendered == "   1 2 3\n 1 X S .\n 2 . . ."
