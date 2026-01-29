#!/usr/bin/env python3
"""Prompt the user for names and append them to an encrypted file."""
from __future__ import annotations
from cryptography.fernet import Fernet

FILENAME = "name.enc"
KEY_FILE = "key.key"


def load_or_create_key() -> bytes:
    try:
        with open(KEY_FILE, "rb") as f:
            return f.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key
#test 3

def main() -> None:
    key = load_or_create_key()
    cipher = Fernet(key)

    print("Enter names (or 'q' to quit). Names are saved encrypted.")
    while True:
        name = input("Enter your name: ").strip()
        if name.lower() == "q":
            print("Done.")
            break
        if not name:
            continue

        encrypted = cipher.encrypt(name.encode("utf-8"))

        with open(FILENAME, "ab") as f:
            f.write(encrypted + b"\n")

        print("Saved encrypted name.")


if __name__ == "__main__":
    main()