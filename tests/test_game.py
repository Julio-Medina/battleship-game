from battleship_ai.board import ShotResult
from battleship_ai.game import Game


def test_game_places_default_ships():
    game = Game(seed=1)

    game.place_default_ships()

    assert len(game.player_board.ships) == 4
    assert len(game.ai_board.ships) == 4


def test_player_can_hit_ai_ship():
    game = Game(seed=1)
    game.place_default_ships()

    result = game.player_shoots(1, 2)

    assert result == ShotResult.HIT


def test_player_can_miss_ai_ship():
    game = Game(seed=1)
    game.place_default_ships()

    result = game.player_shoots(10, 10)

    assert result == ShotResult.MISS


def test_ai_can_take_a_turn():
    game = Game(seed=1)
    game.place_default_ships()

    shot, result = game.ai_shoots()

    assert isinstance(shot, tuple)
    assert len(shot) == 2
    assert result in {ShotResult.MISS, ShotResult.HIT, ShotResult.SUNK}


def test_player_wins_after_sinking_all_ai_ships():
    game = Game(seed=1)
    game.place_default_ships()

    for ship in game.ai_board.ships:
        for x, y in ship.positions:
            game.player_shoots(x, y)

    assert game.player_won is True


def test_ai_wins_after_sinking_all_player_ships_directly():
    game = Game(seed=1)
    game.place_default_ships()

    for ship in game.player_board.ships:
        for x, y in ship.positions:
            game.player_board.receive_shot(x, y)

    assert game.ai_won is True
