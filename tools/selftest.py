"""Prove the documentation checks can fail.

Run before trusting a clean `verify.py` run:

    python3 tools/selftest.py && python3 tools/verify.py

Every case here is a defect that actually shipped and was missed, or the exact
shape a check claims to catch. If a case stops failing, the check has rotted.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dspl_lint import fences, code_blocks, preceding_prose, ANTI  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + ("" if ok else f"  <- {detail}"))
    if not ok:
        failures.append(name)


print("=== fence parser ===")

# The defect that invalidated every code check: a mermaid block before the code.
SRC = """intro prose

```mermaid
graph TD
  A --> B
```

more prose that must never be mistaken for code

```
await payments.charge(cmd)
```

trailing prose
"""
blocks = code_blocks(SRC)
check("mermaid block is skipped, not mis-paired",
      blocks == ["await payments.charge(cmd)"],
      f"got {blocks!r}")

check("prose between fences is never captured",
      all("prose" not in b for b in code_blocks(SRC)))

# Two mermaid blocks in a row shifted the old regex by two.
SRC2 = "```mermaid\na\n```\n\n```mermaid\nb\n```\n\n```\nreal = code\n```\n"
check("consecutive mermaid blocks stay aligned",
      code_blocks(SRC2) == ["real = code"], f"got {code_blocks(SRC2)!r}")

check("info string is preserved",
      [i for i, _b, _n in fences("```python\nx\n```\n")] == ["python"])

check("unterminated fence does not hang or swallow the file",
      code_blocks("```\nx = 1\n") == ["x = 1"])

lines = SRC.splitlines()
_info, _body, start = fences(SRC)[0]
check("start_line indexes the first body line (0-based)",
      lines[start] == "await payments.charge(cmd)", f"got {lines[start]!r}")
_win = [l for l in preceding_prose(lines, start).splitlines() if l.strip()]
check("the window above a fence stops just before that fence's own opener",
      _win[-1] == "more prose that must never be mistaken for code",
      f"got {_win[-1]!r}")

print("\n=== anti-example detection ===")

DOC = """**Before — the naive version.**

```
await payments.charge(cmd)
```
"""
_i, _b, st = fences(DOC)[0]
check("'**Before —**' above the fence is visible to the checker",
      bool(ANTI.search(preceding_prose(DOC.splitlines(), st))))

check("a TRAP marker deep inside a long block is still found",
      bool(ANTI.search("x = 1\n" * 200 + "# TRAP: this is wrong")))

print("\n=== rule shapes ===")

# ubiquitous-language drift: one noun, two creation verbs
SYN = ('Issue', 'Generate', 'Create', 'Make', 'Produce')
def drift(blocks_):
    names = {}
    for b in blocks_:
        for verb, noun in re.findall(r'\b([A-Z][a-z]+)([A-Z][A-Za-z]+)\b', b):
            if verb in SYN:
                names.setdefault(noun, set()).add(verb)
    return {n for n, v in names.items() if len(v) > 1}

check("drift fires on GenerateLabel vs IssueLabel",
      drift(["outbox.append(GenerateLabel(x))", "emit IssueLabel(y)"]) == {"Label"})
check("drift stays silent on one verb per noun",
      drift(["IssueLabel(x)", "IssueRefund(y)", "VoidLabel(z)"]) == set())

# dual-write: durable write followed by an unguarded external effect
DUR = re.compile(r'\b\w*(orders|store|db|processes)\w*\.(put|save|insert|update)\(')
EXT = re.compile(r'\b(bus|topic|queue|events|email)\w*\.(publish|send)\(')
OBX = re.compile(r'\b(outbox|jobs|inbox)\w*\.(append|put|enqueue)\(')
check("dual-write pattern is recognised",
      bool(DUR.search("orders.put(o)")) and bool(EXT.search("bus.publish(e)")))
check("an outbox append is not counted as an external effect",
      not (EXT.search("outbox.append(e)") and not OBX.search("outbox.append(e)")))

# unbounded remote call
CALL = re.compile(r'await\s+(payments|inventory)\w*\.(\w+)\(')
check("unbounded remote call is recognised",
      bool(CALL.search("  x = await payments.charge(cmd)")))
check("a Result combinator is not a remote call",
      not re.search(r'(?<![.\w])(reviews)\w*\.(?!unwrap\w*\()(\w+)\(',
                    "reviews.unwrap_or(None)"))

print()
if failures:
    print(f"SELFTEST: {len(failures)} FAILED -> {failures}")
    sys.exit(1)
print("SELFTEST: all checks can fail when they should. verify.py results are meaningful.")
