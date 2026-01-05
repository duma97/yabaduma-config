#!/usr/bin/env python3

import subprocess
import sys

VALID_DIRECTIONS = {"west", "east", "north", "south"}


def swap_window(direction: str) -> bool:
    result = subprocess.run(
        ["yabai", "-m", "window", "--swap", direction],
        capture_output=True,
    )
    return result.returncode == 0


def toggle_split() -> None:
    subprocess.run(["yabai", "-m", "window", "--toggle", "split"], capture_output=True)


def main():
    if len(sys.argv) < 2:
        print("Usage: smart-swap.py <west|east|north|south>", file=sys.stderr)
        sys.exit(1)

    direction = sys.argv[1]

    if direction not in VALID_DIRECTIONS:
        print("Usage: smart-swap.py <west|east|north|south>", file=sys.stderr)
        sys.exit(1)

    if not swap_window(direction):
        toggle_split()
        swap_window(direction)


if __name__ == "__main__":
    main()
