from typing import Tuple

from battleship_ai.board import ShotResult
from battleship_ai.game import Game


def format_result(result: ShotResult) -> str:
    if result == ShotResult.HIT:
        return "hit"
    if result == ShotResult.SUNK:
        return "sunk"
    if result == ShotResult.MISS:
        return "miss"
    if result == ShotResult.REPEATED:
        return "repeated shot"
    return str(result)


def parse_shot(raw: str) -> Tuple[int, int]:
    parts = raw.strip().replace(" ", "").split(",")

    if len(parts) != 2:
        raise ValueError("Use the format x,y. Example: 4,7")

    x, y = int(parts[0]), int(parts[1])
    return x, y


def main() -> None:
    game = Game(seed=None)
    game.place_default_ships()

    print("Battleship Heuristic AI")
    print("Enter shots as x,y. Example: 4,7")
    print("Type q to quit.\n")

    while not game.player_won and not game.ai_won:
        raw = input("Your shot: ").strip()

        if raw.lower() in {"q", "quit", "exit"}:
            print("Goodbye.")
            return

        try:
            x, y = parse_shot(raw)
            player_result = game.player_shoots(x, y)
        except ValueError as exc:
            print(f"Invalid input: {exc}")
            continue

        print(f"You fired at ({x}, {y}): {format_result(player_result)}")

        if game.player_won:
            print("You sank all enemy ships. You win!")
            return

        ai_position, ai_result = game.ai_shoots()
        print(f"AI fired at {ai_position}: {format_result(ai_result)}")

        if game.ai_won:
            print("The AI sank all your ships. You lose.")
            return

        print()

    print("Game over.")


if __name__ == "__main__":
    main()
