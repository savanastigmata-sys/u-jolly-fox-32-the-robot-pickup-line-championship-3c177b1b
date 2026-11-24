#!/usr/bin/env python3
"""The Robot Pickup Line Championship — entry generator.

Writes a single-line robot pickup line (<=200 chars, UTF-8) to
$MAKEFUN_OUTPUT_DIR/entry.txt.
"""

import os
import sys

MAX_CHARS = 200

LINE = (
    "Every algorithm I know says the optimal move is standing here, "
    "pretending I didn't rehearse this."
)


def resolve_output_dir():
    """Return the output directory, falling back to ./output."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def validate(line):
    """Enforce the competition format: one line, <=200 chars, UTF-8."""
    if not line or not line.strip():
        raise ValueError("entry must not be empty")
    if line != line.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "entry is %d chars, over the %d limit" % (len(line), MAX_CHARS)
        )
    line.encode("utf-8")
    return line


def main():
    line = validate(LINE)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    # Read back and re-validate: the file on disk must be exactly the entry.
    with open(path, "r", encoding="utf-8") as f:
        on_disk = f.read()
    if on_disk != line + "\n":
        raise RuntimeError("entry.txt on disk does not match validated line")
    validate(on_disk.rstrip("\n"))
    print("wrote %s (%d chars)" % (path, len(line)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
