#!/usr/bin/env python3
"""
Very simple Risk-as-Code gate for a repo.

Goal:
- FAIL if any changed .py file writes plaintext to disk.
- PASS if file-writing is preceded by an obvious encryption step.

How it works (simple heuristics, not perfect):
1) Detect file writes (open(..., "w"/"a"/"x") or binary "wb"/"ab"/"xb").
2) If there is a file write, require at least one "encryption signal" in the file:
   - imports cryptography / Fernet
   - calls .encrypt(...)
   - uses Fernet(...)

Usage ideas:
- Local: python risk_gate.py path/to/script.py
- CI:    python risk_gate.py $(git diff --name-only origin/main...HEAD | grep '\.py$')
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable
# Test to see if we can trigger risk gate) ---

# --- Simple patterns (intentionally basic) ---

# "Writes to disk" signals
OPEN_WRITE_RE = re.compile(
    r"""open\s*\(\s*[^)]*,\s*["'].*([wax]|[wax]b|b[axw]).*["']\s*\)""",
    re.IGNORECASE,
)
# Also catch common direct writes outside open() contexts (very basic)
WRITE_CALL_RE = re.compile(r"""\.(write|writelines)\s*\(""", re.IGNORECASE)

# "Encryption present" signals (choose what your demo uses)
ENCRYPT_IMPORT_RE = re.compile(r"""^\s*(from\s+cryptography|import\s+cryptography)\b""", re.MULTILINE)
FERNET_RE = re.compile(r"""\bFernet\b""")
ENCRYPT_CALL_RE = re.compile(r"""\.encrypt\s*\(""")  # e.g., cipher.encrypt(...)

# Optional: allow a "safe wrapper" as an alternative signal
SAFE_WRAPPER_RE = re.compile(r"""\bsecure_save\b|\bSecureStorage\.save\b""")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # If it's not UTF-8, treat as suspicious for this simple gate
        return ""


def file_writes_to_disk(code: str) -> bool:
    return bool(OPEN_WRITE_RE.search(code) or WRITE_CALL_RE.search(code))


def file_has_encryption_signal(code: str) -> bool:
    # For your demo: require cryptography/Fernet + an encrypt call
    has_crypto = bool(ENCRYPT_IMPORT_RE.search(code) or FERNET_RE.search(code))
    has_encrypt_call = bool(ENCRYPT_CALL_RE.search(code))
    has_safe_wrapper = bool(SAFE_WRAPPER_RE.search(code))

    # Pass if either:
    # - explicit encryption signals, OR
    # - approved wrapper
    return (has_crypto and has_encrypt_call) or has_safe_wrapper


def check_paths(paths: Iterable[Path]) -> int:
    failures: list[str] = []

    for p in paths:
        if not p.exists() or p.suffix != ".py":
            continue

        code = read_text(p)
        if not code:
            failures.append(f"{p}: could not read as UTF-8 (treating as FAIL for demo).")
            continue

        if file_writes_to_disk(code) and not file_has_encryption_signal(code):
            failures.append(
                f"{p}: writes to disk but no encryption signal found. "
                f"(Expected cryptography/Fernet + .encrypt(...) or a safe wrapper.)"
            )

    if failures:
        print("RISK GATE: FAIL")
        for msg in failures:
            print(f" - {msg}")
        return 1

    print("RISK GATE: PASS")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python risk_gate.py <file1.py> [file2.py ...]")
        return 2

    paths = [Path(a) for a in argv[1:]]
    return check_paths(paths)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
