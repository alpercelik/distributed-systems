"""Shared primitives for the documentation checks.

This module exists because of a real defect. The fenced-code extractor was
originally a one-line regex:

    re.findall(r'```(?!mermaid)\\w*\\n(.*?)```', src, re.S)

The `(?!mermaid)` lookahead makes the scan refuse to *open* at a ```mermaid
fence — so it opens at that block's CLOSING fence instead, and every subsequent
pairing is off by one. The "code" it returned was prose. Every check built on it
reported a clean bill of health while reading the wrong half of the file.

The lesson generalises: a check that cannot fail is worse than no check, because
it is mistaken for evidence. Anything imported here is exercised by
tools/selftest.py against inputs with known defects.
"""

import re

FENCE_OPEN = re.compile(r'\s*```+(\S*)')
FENCE_CLOSE = re.compile(r'\s*```+\s*$')

# Markers that make a block or line a deliberate anti-example.
ANTI = re.compile(r'TRAP|WRONG|✗|anti-example|Before —')


def fences(src, skip=("mermaid",)):
    """Return [(info, body, start_line)] for every fenced block.

    Fences are paired by walking lines and tracking open/close state, never by
    regex alternation. `start_line` is 1-based and points at the opening fence's
    following line, so `src.splitlines()[start_line - 1]` is the body's first line.
    """
    out, lines, i = [], src.splitlines(), 0
    while i < len(lines):
        m = FENCE_OPEN.match(lines[i])
        if not m:
            i += 1
            continue
        info, start, j = m.group(1), i, i + 1
        while j < len(lines) and not FENCE_CLOSE.match(lines[j]):
            j += 1
        if info not in skip:
            out.append((info, "\n".join(lines[start + 1:j]), start + 1))
        i = j + 1
    return out


def code_blocks(src):
    return [b for _info, b, _n in fences(src)]


def preceding_prose(src_lines, start_line, n=7):
    """The prose immediately above a fence.

    The '**Before — ...**' header that marks an anti-example lives here, not in
    the block, so any check that judges intent must read it.
    """
    return "\n".join(src_lines[max(0, start_line - n):start_line - 1])
