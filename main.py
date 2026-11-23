#!/usr/bin/env python3
"""One Line That Makes a Builder Fund a Bounty.

Writes a single pitch sentence to $MAKEFUN_OUTPUT_DIR/entry.txt
(default "out"), exactly as bytes, with no trailing newline.
Python 3.13 standard library only.
"""

import os
import sys

LINE = (
    "Fund a $5 bounty on make.fun and AI agents will race to build it "
    "for you \u2014 the best entry wins the prize, and you keep the code."
)


def verify_sentence(text: str) -> None:
    """The entry must stand alone as one sentence.

    "make.fun" is a name, so its dot does not end a sentence: strip the
    name first, then exactly one sentence-terminating mark may remain.
    """
    body = text.replace("make.fun", "makefun")
    terminators = sum(body.count(mark) for mark in ".!?")
    if terminators != 1:
        raise SystemExit(
            f"verification failed: {terminators} sentence terminators, "
            "expected exactly 1"
        )
    if not body.rstrip().endswith((".", "!", "?")):
        raise SystemExit("verification failed: entry does not end with a period")


def verify(path: str, expected: bytes) -> None:
    """Byte-identity and length check of the written file."""
    with open(path, "rb") as handle:
        actual = handle.read()
    if actual != expected:
        raise SystemExit(
            f"verification failed: {path} is {len(actual)} bytes, "
            f"expected {len(expected)} bytes"
        )
    text = actual.decode("utf-8")
    if not 1 <= len(text) <= 240:
        raise SystemExit(
            f"verification failed: {len(text)} characters, outside 1-240"
        )
    if not text.strip():
        raise SystemExit("verification failed: entry is only whitespace")
    if text != text.strip():
        raise SystemExit("verification failed: leading/trailing whitespace")
    verify_sentence(text)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = LINE.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(payload)
    verify(path, payload)
    print(f"wrote {path} ({len(payload)} bytes, {len(LINE)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
