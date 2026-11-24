"""Famous Last Words at 1 Percent -- make.fun entry.

One line, spoken by a phone at one percent battery: its famous last
words before the screen goes dark. Original, funny, and on-topic --
a farewell to the charger and a confession about the low-battery
warning it ignored for hours.

The program writes the line to <MAKEFUN_OUTPUT_DIR>/entry.txt
(default /output/entry.txt, the file the sealed gate checks:
UTF-8 text, 1 to 200 characters, not only whitespace) and also
prints the exact same line to stdout.

Pure Python 3 standard library only; deterministic; no network.
SPDX-License-Identifier: MIT
"""

import os

# The last words themselves: one line, one sentence.
LINE = (
    "Tell my charger I loved it; I died doing what I loved -- "
    "ignoring the low-battery warning for three whole hours."
)

MAX_CHARS = 200


def output_path():
    """Resolve the entry file location from the environment."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(directory, "entry.txt")


def validate(line):
    """Check that the line is a single well-formed last-words line."""
    if not isinstance(line, str):
        raise ValueError("last words must be text")
    if not line or line != line.strip():
        raise ValueError("last words must be a single non-blank line")
    if "\n" in line or "\r" in line:
        raise ValueError("last words must not contain a line break")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "last words are %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    if line.count(".") != 1 or not line.endswith("."):
        raise ValueError("last words must be exactly one sentence")
    return line


def store(line):
    """Write the line to entry.txt and print the exact same line."""
    path = output_path()
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")
    print(line)


def main():
    """Validate first, so only well-formed last words are ever stored."""
    store(validate(LINE))


if __name__ == "__main__":
    main()
