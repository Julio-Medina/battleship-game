import pytest

from battleship_ai.cli import parse_shot


def test_parse_shot_accepts_comma_format():
    assert parse_shot("4,7") == (4, 7)


def test_parse_shot_accepts_spaces():
    assert parse_shot(" 4, 7 ") == (4, 7)


def test_parse_shot_rejects_invalid_format():
    with pytest.raises(ValueError, match="Use the format"):
        parse_shot("4")


def test_parse_shot_rejects_non_integer_values():
    with pytest.raises(ValueError):
        parse_shot("x,y")
