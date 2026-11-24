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

# The last words, kept as two clauses in the source so each half
# reads on its own; build_last_words() joins them into the single
# sentence that is submitted.
_LAST_WORDS_CLAUSES = (
    "Tell my charger I loved it; I died doing what I loved --",
    "ignoring the low-battery warning for three whole hours.",
)

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_OUTPUT_DIR = "/output"
ENTRY_FILENAME = "entry.txt"


def build_last_words():
    """Assemble the entry line from its clauses, one space apart."""
    return " ".join(_LAST_WORDS_CLAUSES)


def check_single_line(line):
    """Reject anything that is not one plain, non-blank line."""
    if not isinstance(line, str):
        raise ValueError("last words must be text")
    if not line or line != line.strip():
        raise ValueError("last words must be a single non-blank line")
    if "\n" in line or "\r" in line or "\t" in line:
        raise ValueError("last words must not contain a line break or tab")
    if "  " in line:
        raise ValueError("last words must not contain double spaces")
    if not line.isprintable():
        raise ValueError("last words must contain only printable characters")
    return line


def check_length(line):
    """Enforce the sealed gate's 1-200 character window."""
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        raise ValueError(
            "last words are %d characters, outside the %d-%d window"
            % (len(line), MIN_CHARS, MAX_CHARS)
        )
    return line


def check_single_sentence(line):
    """The entry is exactly one sentence, ending in a full stop."""
    if line.count(".") != 1 or not line.endswith("."):
        raise ValueError("last words must be exactly one sentence")
    return line


def validate(line):
    """Run every check in order; return the line unchanged if it passes."""
    check_single_line(line)
    check_length(line)
    check_single_sentence(line)
    return line


def resolve_output_path():
    """Resolve the entry file location from the environment."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    return os.path.join(directory, ENTRY_FILENAME)


def write_entry(line, path):
    """Write the line (plus trailing newline) to entry.txt."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")
    return path


def main():
    """Build, validate, then store and print the same last-words line."""
    line = validate(build_last_words())
    write_entry(line, resolve_output_path())
    print(line)


if __name__ == "__main__":
    main()
