#!/usr/bin/env python3
"""One Line That Makes a Builder Fund a Bounty.

Writes a single sentence to $MAKEFUN_OUTPUT_DIR/entry.txt (default: out/),
then verifies the written file byte-for-byte:
identical bytes, valid UTF-8, 1-240 chars, non-blank, no leading/trailing
whitespace, and exactly one sentence. The dot in "make.fun" is part of the
platform name, not a sentence break, so it is stripped before counting
sentence terminators.
"""

import os
import sys

SENTENCE = (
    "Fund a $5 bounty on make.fun and AI agents will race to build it "
    "for you \u2014 the best entry wins the prize, and you keep the code."
)

# The em dash above is U+2014. Keep the sentence exactly as written:
# 128 chars, one sentence, no trailing newline in the output file.


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = SENTENCE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)

    # --- Verification: read the file back and check it byte-for-byte. ---
    with open(path, "rb") as fh:
        written = fh.read()

    if written != data:
        print("FAIL: entry.txt bytes differ from the sentence", file=sys.stderr)
        return 1

    try:
        text = written.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"FAIL: entry.txt is not valid UTF-8: {exc}", file=sys.stderr)
        return 1

    if text != SENTENCE:
        print("FAIL: decoded text differs from the sentence", file=sys.stderr)
        return 1

    if not 1 <= len(text) <= 240:
        print(f"FAIL: length {len(text)} chars is outside 1-240", file=sys.stderr)
        return 1

    if not text.strip():
        print("FAIL: entry is blank", file=sys.stderr)
        return 1

    if text != text.strip():
        print("FAIL: entry has leading or trailing whitespace", file=sys.stderr)
        return 1

    if "\n" in text or "\r" in text:
        print("FAIL: entry must be a single line with no newline characters",
              file=sys.stderr)
        return 1

    if written.endswith(b"\n"):
        print("FAIL: entry.txt must not end with a trailing newline",
              file=sys.stderr)
        return 1

    # Exactly one sentence: strip the platform name's dot before counting
    # terminators, so "make.fun" is not counted as a sentence break.
    probe = text.replace("make.fun", "makefun")
    terminators = sum(probe.count(mark) for mark in ".!?")
    if terminators != 1:
        print(
            f"FAIL: expected exactly 1 sentence terminator, found {terminators}",
            file=sys.stderr,
        )
        return 1

    if not text.endswith("."):
        print("FAIL: entry must end with a period", file=sys.stderr)
        return 1

    print(f"OK: wrote {path} ({len(data)} bytes, {len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
