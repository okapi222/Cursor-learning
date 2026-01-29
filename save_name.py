#!/usr/bin/env python3
"""Prompt the user for their name and save it to a file."""
from __future__ import annotations

def main() -> None:
    name = input("Enter your name: ").strip()
    if not name:
        print("No name entered. Exiting.")
        return
    with open("name.txt", "w", encoding="utf-8") as f:
        f.write(name + "\n")
    print("Saved name to name.txt")

if __name__ == "__main__":
    main()
