"""The Robot Apology.

Writes a two-line robot confession to /output/entry.txt.

Line one owns one specific mistake. Line two names the lesson that
follows from that exact mistake and what will change.

The text is validated before it is written: exactly two lines, 1 to
400 characters in total, not only whitespace, no control characters,
and each line ending as a sentence. If validation fails the program
exits non-zero and writes nothing. After writing, the file is read
back and must match the validated text exactly.
"""

import sys
from pathlib import Path

APOLOGY = (
    "Sorry, I set your alarm for 6 p.m. instead of 6 a.m., so you slept "
    "until noon and missed your sister's graduation ceremony.\n"
    "I learned that a.m. and p.m. change the whole day, not just the "
    "hour, so I will say 'six in the morning' back to you and wait "
    "for a yes before I set any alarm again."
)

OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARS = 400


def validate_apology(text: str) -> list[str]:
    """Return a list of problems with the apology; empty means valid."""
    problems: list[str] = []
    if not isinstance(text, str):
        return ["apology is not text"]
    if not text.strip():
        problems.append("apology is empty or only whitespace")
    if len(text) < 1 or len(text) > MAX_CHARS:
        problems.append(
            f"apology is {len(text)} characters, outside 1 to {MAX_CHARS}"
        )
    lines = text.split("\n")
    if len(lines) != 2:
        problems.append(f"apology must be exactly two lines, got {len(lines)}")
    for line in lines:
        if not line.strip():
            problems.append("a line is empty or only whitespace")
        if not line.rstrip().endswith("."):
            problems.append("each line must end with a full stop")
    bad_controls = [c for c in text if ord(c) < 32 and c != "\n"]
    if bad_controls:
        problems.append(f"apology contains control characters: {bad_controls!r}")
    return problems


def main() -> int:
    problems = validate_apology(APOLOGY)
    if problems:
        for problem in problems:
            print(f"invalid apology: {problem}", file=sys.stderr)
        return 1
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(APOLOGY, encoding="utf-8")
    written_back = OUTPUT_PATH.read_text(encoding="utf-8")
    if written_back != APOLOGY:
        print("invalid apology: written file does not match", file=sys.stderr)
        return 1
    if validate_apology(written_back):
        print("invalid apology: read-back text failed validation", file=sys.stderr)
        return 1
    print(f"characters: {len(written_back)}")
    print(APOLOGY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
