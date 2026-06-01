# Battleship Heuristic AI

A classic Battleship game implemented in Python, originally developed as a university programming project and now being modernized into a clean, testable portfolio project.

## Original Version

The original implementation is preserved in:

legacy/battle_ship_game.py

The legacy version was written in Python 2 style and includes:

- Terminal-based Battleship gameplay
- Human vs human mode
- Human vs computer mode
- LAN/socket communication
- Ship placement through a text file
- A rule-based heuristic bot that mimics simple reasoning after successful hits

## Project Goal

The goal of this repository is to modernize the original game into a clean Python 3 project while preserving the original behavior and documenting the refactoring process.

## Planned Structure

The project will eventually separate:

- Board logic
- Ship logic
- Game flow
- AI strategy
- Network/socket communication
- Command-line interaction

## Roadmap

- [x] Preserve the original implementation
- [ ] Port syntax to Python 3
- [ ] Extract board and ship classes
- [ ] Extract heuristic AI logic
- [ ] Add unit tests
- [ ] Add a clean terminal game mode
- [ ] Reintroduce socket multiplayer support

## AI Strategy

The computer player does not use machine learning. It uses classical rule-based heuristics.

At a high level:

1. Shoot randomly when there is no known target.
2. After a successful hit, remember the position.
3. Try nearby positions in a direction.
4. Avoid repeated shots.
5. Continue until the ship is sunk or the search direction fails.

This makes the bot a simple example of classical AI based on rules, state, and local search.

## Status

This repository is currently in the preservation and refactoring stage.

## Running the Modern Version

The modernized version lives inside the src/battleship_ai/ package.

Run the terminal game with:

    PYTHONPATH=src python3 -m battleship_ai.cli

Enter shots using this format:

    x,y

Example:

    4,7

To quit the game, type:

    q

## Running the Tests

Install pytest if needed:

    python3 -m pip install pytest

Run the test suite:

    pytest -q

## Current Architecture

The modern code is organized as follows:

    src/battleship_ai/
    ├── ship.py      # Ship model and hit tracking
    ├── board.py     # Board state, ship placement, and shot resolution
    ├── ai.py        # Rule-based heuristic AI
    ├── game.py      # Game coordinator between player and AI boards
    └── cli.py       # Playable terminal interface

## Development Branch

Active modernization work is happening on:

    refactor/python3-core

The main branch preserves the stable repository history while the refactor is developed incrementally.

