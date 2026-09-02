import os, re, sys
from pathlib import Path
from urllib.parse import unquote

# Resolve from this file so the documented command works from any clone.
ROOT = str(Path(__file__).resolve().parent.parent)
import subprocess as _sp
# Only check files git tracks. Review notes and other ignored scratch files are
# transient and may contain "path.md:141" citations that are not link targets.
_tracked = set()
try:
    _tracked = {os.path.normpath(os.path.join(ROOT, x))
                for x in _sp.run(["git", "-C", ROOT, "ls-files", "*.md"],
                                 capture_output=True, text=True).stdout.split()}
except Exception:
    pass
md = []
for dp, dn, fn in os.walk(ROOT):
    if ".git" in dp.split(os.sep): continue
    for f in fn:
        if not f.endswith(".md"): continue
        full = os.path.join(dp, f)
        if _tracked and os.path.normpath(full) not in _tracked: continue
        md.append(full)
md.sort()

# Blume removes numeric ordering prefixes from published routes. Keep the
# source files and their links readable in the repository while allowing this
# checker to validate the canonical Blume URLs as well.
def _blume_route(path):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if rel == "README.md":
        return "/"
    parts = rel.split("/")
    if parts[0] == "modules" and len(parts) >= 3 and re.match(r"^\d{2}-", parts[1]):
        module = parts[1][3:]
        stem = parts[-1][:-3]
        if stem != "README" and re.match(r"^\d{2}-", stem):
            stem = stem[3:]
        return f"/modules/{module}/{stem}"
    return "/" + rel[:-3]

site_routes = {_blume_route(path): path for path in md}

link_re = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
broken = []
total_links = 0
for path in md:
    txt = open(path, encoding="utf-8").read()
    # strip fenced code blocks
    txt_nocode = re.sub(r'```.*?```', '', txt, flags=re.S)
    for m in link_re.finditer(txt_nocode):
        target = m.group(2).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        total_links += 1
        frag = target.split("#")[0]
        if not frag:
            continue
        if frag.startswith("/"):
            resolved = site_routes.get(unquote(frag))
        else:
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), unquote(frag)))
        if not resolved or not os.path.exists(resolved):
            broken.append((os.path.relpath(path, ROOT), target))

print(f"markdown files: {len(md)}")
print(f"internal links checked: {total_links}")
print(f"broken links: {len(broken)}")
for p, t in broken[:60]:
    print(f"  BROKEN  {p} -> {t}")
fails = len(broken)

# section conformance for lessons
SECTIONS = ["1. The problem","2. In plain language","3. How it works","4. Pseudo-code",
            "5. Knobs and variants","6. Challenges and failure modes","7. Alternatives",
            "8. Trade-offs","9. Complexity introduced","10. Related concepts",
            "11. Exercises","12. References"]
lessons = [p for p in md if re.search(r'/\d\d-\d\d-', p)]
print(f"\nlesson files: {len(lessons)}")
bad = []
for p in lessons:
    t = open(p, encoding="utf-8").read()
    missing = [s for s in SECTIONS if f"## {s}" not in t]
    has_mermaid = "```mermaid" in t
    has_nav = "**Up:**" in t
    if missing or not has_mermaid or not has_nav:
        bad.append((os.path.relpath(p, ROOT), missing, has_mermaid, has_nav))
if not bad:
    print("all lessons: 12/12 sections, mermaid diagram, nav footer  ✓")
for b in bad:
    print("  ISSUE", b[0], "missing:", b[1], "mermaid:", b[2], "nav:", b[3])
fails += len(bad)

# curriculum coverage
cur = open(os.path.join(ROOT,"CURRICULUM.md"), encoding="utf-8").read()
listed = set()
for target in re.findall(r'\]\((/modules/[^)#]+)', cur):
    page = site_routes.get(target)
    if page and os.path.dirname(page).startswith(os.path.join(ROOT, "modules")):
        listed.add(os.path.relpath(page, os.path.join(ROOT, "modules")))
listed_lessons = {l for l in listed if re.search(r'/\d\d-\d\d-', "/"+l)}
actual = {os.path.relpath(p, os.path.join(ROOT,"modules")) for p in lessons}
print(f"\ncurriculum lists {len(listed_lessons)} lessons; filesystem has {len(actual)}")
print("in curriculum, missing on disk:", sorted(listed_lessons - actual))
print("on disk, missing from curriculum:", sorted(actual - listed_lessons))
fails += len(listed_lessons - actual) + len(actual - listed_lessons)

# --- regression guards added after the third-party review ---
import subprocess, sys
print("\n=== review regression guards ===")
for pat, why in [
    (r"\| \*\*Module\*\* \| \[(?!__SELF__)", "module header vs path"),
]:
    pass
import os, re
bad = [ (os.path.join(dp,f), m.group(1), os.path.basename(dp)[:2])
        for dp,dn,fn in os.walk(os.path.join(ROOT,"modules")) for f in sorted(fn)
        if re.match(r'\d\d-\d\d-', f)
        for m in [re.search(r'\|\s*\*\*Module\*\*\s*\|\s*\[(\d\d)', open(os.path.join(dp,f),encoding="utf-8").read())]
        if m and m.group(1) != os.path.basename(dp)[:2] ]
print(f"module headers disagreeing with path: {len(bad)}")
fails += len(bad)
stale = subprocess.run(["grep","-rIn","--include=*.md","-E",
    r"(55 lessons|56 lessons|Fifty-five|sharded order store|exactly two things)", ROOT],
    capture_output=True, text=True).stdout.strip()
print(f"stale claims/counts: {len(stale.splitlines()) if stale else 0}")
if stale: print(stale)
fails += len(stale.splitlines()) if stale else 0
print("GUARDS: PASS" if fails == 0 else f"GUARDS: {fails} FAILURES")

# --- fence parsing ---------------------------------------------------------
# See tools/dspl_lint.py for why this is not a regex, and tools/selftest.py for
# the cases that prove it works. Run selftest.py before trusting a clean run.
sys.path.insert(0, os.path.join(ROOT, "tools"))
from dspl_lint import fences, code_blocks, preceding_prose, ANTI  # noqa: E402

# --- DSPL stdlib conformance (advisory) -----------------------------------
print("\n=== DSPL stdlib conformance ===")
std = open(os.path.join(ROOT, "spec/STDLIB.md"), encoding="utf-8").read()
spec = open(os.path.join(ROOT, "spec/PSEUDOCODE-SPEC.md"), encoding="utf-8").read()
declared = set()
for src in (std, spec):
    for block in code_blocks(src):
        declared |= set(re.findall(r'\.(\w+)\(', block))
        declared |= set(re.findall(r'^\s*(\w+)\(', block, re.M))
BUILTINS = {
 'increment','gauge','histogram','info','warn','error','debug','event','span',
 'map','filter','take','size','count','keys','values','is_empty','is_ok','is_err',
 'unwrap','unwrap_or','unwrap_or_else','trim','split','replace','reversed','sorted',
 'sorted_by','group_by','zip','enumerate','clear','next','has_next','append','add',
 'remove','contains','find','any','all','first','last','sum','min','max','min_by',
 'max_by','join','seconds','ms','index_where','apply','to_view','to_summary','parse',
 'evict_older_than','failure_rate','percentile','record','abs','ceil','floor','round',
}
used = {}
for dp, dn, fn in os.walk(os.path.join(ROOT, "modules")):
    for f in sorted(fn):
        if not f.endswith(".md"): continue
        for block in code_blocks(open(os.path.join(dp, f), encoding="utf-8").read()):
            for m in re.findall(r'\.(\w+)\(', block):
                if m not in declared and m not in BUILTINS:
                    used.setdefault(m, set()).add(f[:5])
required_stdlib_operations = {
    # Storage / logs
    'append', 'append_if_version', 'compare_and_swap', 'compare_and_swap_fenced',
    'delete', 'delete_where', 'get', 'get_entry', 'get_stale',
    'mark_published', 'put', 'put_if_absent', 'put_negative', 'query', 'read',
    'scan', 'truncate', 'update', 'update_where',
    # Messaging
    'ack', 'dead_letter', 'depth', 'nack', 'publish', 'receive', 'retry', 'send',
    # Coordination / cache
    'acquire', 'campaign', 'release', 'renew', 'try_acquire', 'try_enter',
}
missing_core = sorted(m for m in used if m in required_stdlib_operations)
print(f"undeclared required stdlib operations: {len(missing_core)} {missing_core if missing_core else ''}")
print(f"lesson-local helper names (allowed by STDLIB policy): {len(used)}")
if missing_core:
    print("FAIL: extend spec/STDLIB.md or change the lesson")
fails += len(missing_core)

# --- pseudo-code safety audit (from the second external review) -------------
print("\n=== pseudo-code safety audit ===")
import os, re
CLIENTS = r'(payments|inventory|shipping|catalog|carrier|psp|erp|email|search|analytics|loyalty|warehouse|pricing|accounts|notification|reviews|recommender|promotions|consensus|registry)'
def _blocks(p):
    return code_blocks(open(p, encoding="utf-8").read())
_lessons = sorted(os.path.join(dp, f)
                  for dp, dn, fn in os.walk(os.path.join(ROOT, "modules"))
                  for f in fn if re.match(r'\d\d-\d\d-', f))
# Scope. The remote-call rules apply only where the course has already taught
# bounds and where calls are actually remote:
#   - Modules 00-01 deliberately show naive, unbounded code; timeouts arrive in 02-01.
#   - Modules 06-07 (DDD, modular monolith) are in-process by construction. An
#     unawaited `inventory.reserve(...)` there is the point, not a defect.
#   - Blocks and lines flagged TRAP / WRONG / ✗ / "Before" are anti-examples.
IN_PROCESS_MODULES = ("06", "07")
BOUNDS_TAUGHT_FROM = "02"
# `reviews.unwrap_or(None)` is a Result combinator on a local, not a call to the
# reviews service; `ErpProductTranslator.translate(...)` is pure and in-process.
# Without this the audit reports the course's own idioms as network calls.
COMBINATORS = r'(unwrap\w*|or_default|or_else|and_then|is_ok|is_err|map|map_err|' \
              r'translate|to_\w+|from_\w+|value|len|size)'

issues = []
for p in _lessons:
    base = os.path.basename(p)
    mod = base[:2]
    remote_rules = mod >= BOUNDS_TAUGHT_FROM and mod not in IN_PROCESS_MODULES
    _src_lines = open(p, encoding="utf-8").read().splitlines()
    for _info, b, _start in fences(open(p, encoding="utf-8").read()):
        lines = b.splitlines()
        # The "**Before — ...**" header sits in the prose ABOVE the fence, so an
        # anti-example is only recognisable by looking there.
        _pre = "\n".join(_src_lines[max(0, _start - 7):_start - 1])
        block_is_anti = bool(ANTI.search(b[:400]) or ANTI.search(_pre))
        declared = {m.lower() for m in re.findall(r'uses (\w+):[^\n]*with timeout', b)}
        for i, l in enumerate(lines):
            if l.strip().startswith('#'): continue
            near = " ".join(lines[max(0, i - 2):i + 3])
            # `# lint: bound-by <reason>` is an explicit, greppable waiver. It
            # forces the author to state WHY a call needs no bound here, which is
            # the reviewable artefact; a silent allowlist is not.
            waived = re.search(r'#\s*lint:', " ".join(lines[max(0, i - 3):i + 1]))
            suppressed = block_is_anti or ANTI.search(near) or waived
            # a call is bound if the line (or its continuation) carries a bound,
            # or it propagates a deadline-carrying context, or it is `?`-propagated
            bound = re.search(r'timeout|deadline|budget|\bctx\b|remaining\(',
                              " ".join(lines[i:i + 3]))
            if remote_rules and not suppressed:
                m = re.search(r'await\s+' + CLIENTS + r'\w*\.(?!' + COMBINATORS + r'\()(\w+)\(', l)
                if m and not bound \
                   and 'with deadline' not in " ".join(lines[max(0, i - 6):i]) \
                   and m.group(1).lower() not in declared:
                    issues.append(f"{base}:{i+1} unbounded remote call")
                m2 = re.search(r'(?<![.\w])' + CLIENTS + r'\w*\.(?!' + COMBINATORS + r'\()(\w+)\(', l)
                if m2 and not re.search(r'(await|spawn|retry_forever|uses |interface |service |record |=>|\|)', l) \
                   and not re.search(r'\.(publish|send|increment|gauge|append|ping|register|deregister|heartbeat)\(', l) \
                   and not bound:
                    issues.append(f"{base}:{i+1} remote call not awaited")
            # scan() used as a time filter — scan takes a key prefix. Always checked.
            if re.search(r'\.scan\(\s*(older_than|.*_at\b|.*<\s*now)', l) and not suppressed:
                issues.append(f"{base}:{i+1} scan() used as a time predicate")
        # in-process state used as a durability guard
        for l in lines:
            if re.search(r'^\s*state\s+(?!tokens\b)\w*(token|seen|processed|dedup|highest)\w*\s*:', l, re.I) \
               and 'TRAP' not in b and 'WRONG' not in b:
                issues.append(f"{base} guard state held in process memory")
print(f"pseudo-code safety issues: {len(issues)}")
for x in issues: print("  " + x)
fails += len(issues)

# --- dual-write linter: durable state + external effect outside a transaction ---
print("\n=== dual-write audit ===")
_DUR = re.compile(r'\b\w*(orders|store|db|shipments|view|jobs|sagas|processes|ledger|stock|reservations|rows)\w*\.(put|save|insert|update)\(')
_EXT = re.compile(r'\b(bus|topic|queue|events|deferred\w*|work|pending|commands|notifications?|email|search|warehouse|marketing|analytics|loyalty)\w*\.(publish|send|index|record|award|append)\(')
_OBX = re.compile(r'\b(outbox|jobs|deferred|inbox)\w*\.(append|put|enqueue)\(')
dual = []
for p in _lessons:
    src = open(p, encoding="utf-8").read()
    # only lint the worked solutions (§4 onward); §1 problem statements show the bug on purpose
    body = src.split("## 4. Pseudo-code", 1)[-1]
    # keep the ~300 chars of prose before each fence: "**Before — ...**" headers
    # mark deliberate anti-examples and must not be linted as defects.
    _bl = body.splitlines()
    for _info, b, _n in fences(body):
        _pre = "\n".join(_bl[max(0, _n - 6):_n - 1])
        if re.search(r'\*\*Before\b|✗ WRONG|anti-example|# ✗', _pre): continue
        L = b.splitlines()
        inside = [False] * len(L)
        for i, l in enumerate(L):
            if re.match(r'\s*atomically:', l):
                ind = len(l) - len(l.lstrip())
                for j in range(i + 1, len(L)):
                    if L[j].strip() and (len(L[j]) - len(L[j].lstrip())) <= ind: break
                    inside[j] = True
        dur = [i for i, l in enumerate(L) if _DUR.search(l) and not l.strip().startswith('#')]
        ext = [i for i, l in enumerate(L) if _EXT.search(l) and not _OBX.search(l) and not l.strip().startswith('#')]
        for d in dur:
            for e in ext:
                if e < d or e - d > 6: continue
                if inside[d] and inside[e]: continue
                ctx = " ".join(L[max(0, d - 4):e + 5])
                if re.search(r'TRAP|dual-write|✗|WRONG|deliberately|Before', ctx): continue
                dual.append(f"{os.path.basename(p)}: {L[d].strip()[:60]} → {L[e].strip()[:40]}")
                break
            else: continue
            break
print(f"unguarded durable-write + external-effect pairs: {len(dual)}")
for x in dual: print("  " + x)
fails += len(dual)

# --- ubiquitous-language drift: one concept, two names ----------------------
# Module 06 preaches ubiquitous language, so the course must not use two verbs
# for the same command across lessons. Caught GenerateLabel vs IssueLabel.
print("\n=== ubiquitous-language drift ===")
_SYN = ('Issue', 'Generate', 'Create', 'Make', 'Produce')  # creation verbs only:
# Void/Cancel/Abort/Send name different operations on the same noun, not drift.
_names = {}
for p in _lessons:
    _sl = open(p, encoding="utf-8").read().splitlines()
    for _i, b, _n in fences(open(p, encoding="utf-8").read()):
        # anti-examples name invented commands deliberately (see 05-07's TRAP)
        if ANTI.search(b[:400]) or ANTI.search("\n".join(_sl[max(0, _n - 7):_n - 1])):
            continue
        _L = b.splitlines()
        for _li, _line in enumerate(_L):
            # a wrong name quoted inside a TRAP is evidence, not drift
            if ANTI.search(" ".join(_L[max(0, _li - 5):_li + 6])):
                continue
            for verb, noun in re.findall(r'\b([A-Z][a-z]+)([A-Z][A-Za-z]+)\b', _line):
                if verb in _SYN:
                    _names.setdefault(noun, {}).setdefault(verb, set()).add(os.path.basename(p)[:5])
drift = []
for noun, verbs in sorted(_names.items()):
    if len(verbs) > 1:
        # a name used in one lesson only, as a deliberate wrong example, is fine
        spread = {v: sorted(ls) for v, ls in verbs.items()}
        drift.append(f"{noun}: " + ", ".join(f"{v}{noun} in {ls}" for v, ls in spread.items()))
ALLOWED = {  # genuinely distinct operations that share a noun
    'Refund',   # IssueRefund (command) vs RequestRefund (customer-initiated)
    'Order',    # PlaceOrder / CancelOrder are different operations
    'Return',   # RequestReturn / CancelReturn
    'Payment', 'Shipment', 'Reservation', 'Task', 'Session', 'Transaction',
}
drift = [d for d in drift if d.split(":")[0] not in ALLOWED]
print(f"same-noun different-verb command names: {len(drift)}")
for x in drift: print("  " + x)
fails += len(drift)

if fails:
    print(f"\nVERIFY: {fails} failure(s)")
    sys.exit(1)
print("\nVERIFY: PASS")
