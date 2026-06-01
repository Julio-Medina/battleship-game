import pytest

from battleship_ai.ai import HeuristicAI
from battleship_ai.board import ShotResult


def test_ai_returns_position_inside_board():
    ai = HeuristicAI(width=10, height=10, seed=1)

    x, y = ai.next_shot()

    assert 1 <= x <= 10
    assert 1 <= y <= 10


def test_ai_does_not_repeat_shots():
    ai = HeuristicAI(width=3, height=3, seed=1)

    shots = [ai.next_shot() for _ in range(9)]

    assert len(shots) == 9
    assert len(set(shots)) == 9


def test_ai_raises_when_no_shots_remain():
    ai = HeuristicAI(width=1, height=1, seed=1)

    ai.next_shot()

    with pytest.raises(RuntimeError, match="No available shots remain"):
        ai.next_shot()


def test_ai_targets_neighbor_after_hit():
    ai = HeuristicAI(width=10, height=10, seed=1)

    hit_position = (5, 5)
    ai.shots_taken.add(hit_position)
    ai.record_result(hit_position, ShotResult.HIT)

    next_position = ai.next_shot()

    assert next_position in {
        (4, 5),
        (6, 5),
        (5, 4),
        (5, 6),
    }


def test_ai_clears_target_after_sunk():
    ai = HeuristicAI(width=10, height=10, seed=1)

    hit_position = (5, 5)
    ai.record_result(hit_position, ShotResult.HIT)

    assert ai.hits_not_sunk == [hit_position]

    ai.record_result(hit_position, ShotResult.SUNK)

    assert ai.hits_not_sunk == []


def test_ai_ignores_duplicate_hit_records():
    ai = HeuristicAI(width=10, height=10, seed=1)

    ai.record_result((5, 5), ShotResult.HIT)
    ai.record_result((5, 5), ShotResult.HIT)

    assert ai.hits_not_sunk == [(5, 5)]


def test_ai_rejects_invalid_board_size():
    with pytest.raises(ValueError, match="Board dimensions must be positive"):
        HeuristicAI(width=0, height=10)


def test_ai_target_candidates_skip_out_of_bounds_positions():
    ai = HeuristicAI(width=3, height=3, seed=1)

    ai.shots_taken.add((1, 1))
    ai.record_result((1, 1), ShotResult.HIT)

    candidates = ai._target_candidates()

    assert set(candidates) == {(2, 1), (1, 2)}


def test_ai_target_candidates_skip_already_used_positions():
    ai = HeuristicAI(width=3, height=3, seed=1)

    ai.shots_taken.update({(2, 2), (1, 2), (2, 1)})
    ai.record_result((2, 2), ShotResult.HIT)

    candidates = ai._target_candidates()

    assert set(candidates) == {(3, 2), (2, 3)}
