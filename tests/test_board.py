import pytest

from battleship_ai.board import Board, ShotResult
from battleship_ai.ship import Ship


def test_ship_positions_are_horizontal():
    ship = Ship(x=2, y=3, size=4)

    assert ship.positions == [(2, 3), (3, 3), (4, 3), (5, 3)]


def test_place_valid_ship():
    board = Board(width=10, height=10)
    ship = Ship(x=1, y=1, size=3)

    board.place_ship(ship)

    assert board.ships == [ship]


def test_reject_ship_outside_board():
    board = Board(width=10, height=10)
    ship = Ship(x=9, y=1, size=3)

    with pytest.raises(ValueError, match="Invalid ship placement"):
        board.place_ship(ship)


def test_reject_overlapping_ship():
    board = Board(width=10, height=10)
    board.place_ship(Ship(x=1, y=1, size=3))

    with pytest.raises(ValueError, match="Invalid ship placement"):
        board.place_ship(Ship(x=3, y=1, size=3))


def test_miss():
    board = Board(width=10, height=10)
    board.place_ship(Ship(x=1, y=1, size=3))

    assert board.receive_shot(5, 5) == ShotResult.MISS


def test_hit():
    board = Board(width=10, height=10)
    board.place_ship(Ship(x=1, y=1, size=3))

    assert board.receive_shot(2, 1) == ShotResult.HIT


def test_sunk():
    board = Board(width=10, height=10)
    board.place_ship(Ship(x=1, y=1, size=2))

    assert board.receive_shot(1, 1) == ShotResult.HIT
    assert board.receive_shot(2, 1) == ShotResult.SUNK


def test_repeated_shot():
    board = Board(width=10, height=10)
    board.place_ship(Ship(x=1, y=1, size=2))

    assert board.receive_shot(5, 5) == ShotResult.MISS
    assert board.receive_shot(5, 5) == ShotResult.REPEATED


def test_all_sunk():
    board = Board(width=10, height=10)
    board.place_ship(Ship(x=1, y=1, size=1))

    assert board.all_sunk is False

    board.receive_shot(1, 1)

    assert board.all_sunk is True
