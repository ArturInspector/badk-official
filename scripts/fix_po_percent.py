#!/usr/bin/env python3
"""
Run after `makemessages` to fix false-positive python-format flags.

When a blocktranslate string contains a literal `%` (e.g. "95%"), Django's
makemessages marks it `#, python-format` and doubles the percent to `%%`.
At runtime Django looks up the original string with single `%`, the key
doesn't match the catalog, and the translation silently falls back to the
source language.

This script finds those false positives — entries where `#, python-format`
exists but the msgid has no real format specifiers (%s, %d, %(name)s, etc.)
— removes the flag and restores `%%` → `%` in both msgid and msgstr.

Usage:
    python scripts/fix_po_percent.py
    python scripts/fix_po_percent.py --check   # exit 1 if any fixes needed
"""

import argparse
import re
import sys
from pathlib import Path

# Real python format specifiers: %s, %d, %f, %(name)s, etc.
# %% is an escaped literal percent, not a specifier.
_REAL_FORMAT = re.compile(r"%(?!\%)[\w(]")

# Matches a full .po entry block (comment lines + msgid + msgstr)
_ENTRY = re.compile(
    r"((?:#[^\n]*\n)*)"   # comment block
    r'(msgid\s+".*?"(?:\n".*?")*\n)'  # msgid (possibly multi-line)
    r'(msgstr\s+".*?"(?:\n".*?")*\n)',  # msgstr (possibly multi-line)
    re.DOTALL,
)


def _collect_string(raw: str) -> str:
    """Join multiline .po string value into a single string."""
    return "".join(re.findall(r'"(.*?)"', raw))


def fix_file(path: Path, check: bool) -> bool:
    """Return True if any fixes were applied (or needed, in check mode)."""
    text = path.read_text(encoding="utf-8")
    fixed = False
    result = []
    pos = 0

    for m in _ENTRY.finditer(text):
        result.append(text[pos : m.start()])
        comments, msgid_block, msgstr_block = m.group(1), m.group(2), m.group(3)

        has_flag = "#, python-format" in comments
        if has_flag:
            raw_id = _collect_string(msgid_block)
            # After replacing %% with %, are there real format specifiers left?
            after_unescape = raw_id.replace("%%", "")
            if not _REAL_FORMAT.search(after_unescape):
                # False positive — fix it
                fixed = True
                if not check:
                    comments = re.sub(r"#, python-format\n", "", comments)
                    # Also remove trailing comma if it was the only flag
                    msgid_block = msgid_block.replace("%%", "%")
                    msgstr_block = msgstr_block.replace("%%", "%")

        result.append(comments + msgid_block + msgstr_block)
        pos = m.end()

    result.append(text[pos:])

    if fixed and not check:
        path.write_text("".join(result), encoding="utf-8")
        print(f"Fixed: {path}")
    elif fixed and check:
        print(f"Needs fix: {path}")

    return fixed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with code 1 if any files need fixing (don't modify)",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    po_files = sorted(root.glob("locale/*/LC_MESSAGES/django.po"))

    any_fixed = any(fix_file(p, args.check) for p in po_files)

    if args.check and any_fixed:
        print("Run `python scripts/fix_po_percent.py` to fix.")
        sys.exit(1)


if __name__ == "__main__":
    main()
