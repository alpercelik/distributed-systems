# Documentation checks

```
python3 tools/selftest.py && python3 tools/verify.py
```

Run in that order. `selftest.py` proves the checks can fail; `verify.py` runs them.
A clean `verify.py` alone means nothing if the parser underneath it is broken —
that happened, twice, and both times the false all-clear was more damaging than
having no check at all.

## What verify.py checks

| Check | Catches |
|---|---|
| Internal links | Links to files that do not exist. Git-tracked files only, so untracked review notes are ignored. |
| Lesson conformance | A lesson missing any of the 12 sections, its diagram, or its nav footer. |
| Curriculum coverage | A lesson on disk but not in [CURRICULUM.md](../CURRICULUM.md), or the reverse. |
| Regression guards | Metadata headers disagreeing with the file's own path; stale lesson counts and claims. |
| DSPL stdlib conformance | Core store/cache operations used in lessons but never declared in [STDLIB.md](../spec/STDLIB.md). |
| Pseudo-code safety | Unbounded or un-awaited remote calls, `scan()` used as a time predicate, durability guards held in process memory. |
| Dual-write audit | A durable write followed by an external effect outside a transaction. |
| Ubiquitous-language drift | One noun with two creation verbs — `GenerateLabel` in one lesson, `IssueLabel` in another. |

## The review rule for new lessons

Every example that **changes durable state and causes an external effect** must
show one of these three, explicitly:

1. **A transaction plus an outbox** — the state change and the intent to publish
   commit together; a separate publisher drains the outbox.
2. **An idempotent provider call** — a client-supplied key makes a retry safe, so
   the ordering of the two writes stops mattering.
3. **An accepted loss or duplicate, named in a comment** — sometimes the right
   answer, never the silent one.

Prose saying "we use an outbox here" does not count. The adjacent pseudo-code has
to show the atomic hand-off. Every review round of this course found the same
defect class: correct narration above code that quietly drops the guarantee.

## Scope, and what these checks cannot do

The remote-call rules apply from Module 02 (where bounds are taught) and skip
Modules 06–07, which are in-process by construction. Anti-examples are exempt —
they are recognised by `TRAP`, `WRONG`, `✗`, `anti-example`, or a
`**Before — ...**` header above the fence.

To waive a rule deliberately, state why:

```
# lint: bound-by adapter — the callee bounds its own outbound calls.
```

These are shape checks, not meaning checks. They cannot tell you that a
concurrency argument is wrong, that a guarantee is overstated, or that a state
machine contradicts its own diagram. Those need a reader.
