#!/usr/bin/env python3
"""Decrypt and print an encrypted file."""
from __future__ import annotations
import sys
from cryptography.fernet import Fernet


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: decrypt_file.py <encrypted_file> <key_file>")
        sys.exit(1)

    encrypted_file = sys.argv[1]
    key_file = sys.argv[2]

    with open(key_file, "rb") as kf:
        key = kf.read()

    cipher = Fernet(key)

    with open(encrypted_file, "rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # skip empty lines
            decrypted = cipher.decrypt(line)
            print(decrypted.decode("utf-8"), flush=True)


if __name__ == "__main__":
    main()
