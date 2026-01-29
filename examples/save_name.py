#!/usr/bin/env python3
"""Prompt the user for names and append them to a file until they enter 'q'."""
from __future__ import annotations

FILENAME = "name.txt"


def main() -> None:
    print("Enter names (or 'q' to quit). Names are appended to name.txt.")
    while True:
        name = input("Enter your name: ").strip()
        if name.lower() == "q":
            print("Done.")
            break
        if not name:
            continue
        with open(FILENAME, "a", encoding="utf-8") as f:
            f.write(name + "\n")
        print(f"Saved '{name}' to {FILENAME}")


if __name__ == "__main__":
    main()
