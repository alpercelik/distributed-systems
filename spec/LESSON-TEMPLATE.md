---
title: "Lesson Template"
---

Every lesson in `modules/` has exactly these sections, in this order. Consistency is the
point: once you have read three lessons you know where to look for the trade-off table
without reading the prose.

Copy this file to start a new lesson.

---

```markdown
# NN-MM · Pattern Name

> One sentence. What this pattern does, and the single thing it buys you.

| | |
|---|---|
| **Module** | [NN — Module Name](README.md) |
| **Prerequisites** | [link](path) , [link](path) |
| **Also known as** | alternative names in the literature |
| **Category** | Resilience / Scalability / Consistency / Integration / Structure / Operations |

---

## 1. The problem

The concrete failure or limitation that exists *before* the pattern. Written as a
situation, not a definition. Include the observable symptom — what an engineer actually
sees in a dashboard or a postmortem.

## 2. In plain language

An analogy from outside software, three to six sentences. It must be *load-bearing*: the
analogy has to explain the mechanism, not just the vibe. Then one sentence naming exactly
where the analogy breaks down, because every analogy does.

## 3. How it works

The mechanism, technically and precisely. Names the moving parts, the states, the
guarantees, and what is assumed of the environment. Contains at least one Mermaid diagram.

## 4. Pseudo-code

DSPL only ([spec](../../spec/PSEUDOCODE-SPEC.md)). Structured as:

- **Before** — the naive version, when the contrast teaches something.
- **The pattern** — the implementation itself.
- **In use** — how a service calls it, in the ShopFlow domain.

Every network call shows its timeout. Every trap is marked `# TRAP:`.

## 5. Knobs and variants

The parameters you have to choose, with the consequence of choosing wrong in each
direction. A table where possible.

## 6. Challenges and failure modes

What goes wrong *with the pattern in place*. This section is the difference between
knowing a pattern and having operated one. Include: the interaction with other patterns,
the failure that only appears under load, and the failure that only appears during
recovery.

## 7. Alternatives

Other ways to solve the problem in §1, and when each is the better answer — including
"do nothing", which is often correct.

## 8. Trade-offs

| Advantage | Disadvantage |
|---|---|
| ... | ... |

## 9. Complexity introduced

Explicit accounting of the cost of adoption, along four axes:

- **Operational** — new things to monitor, tune, page on.
- **Cognitive** — what a new engineer must understand to change this code safely.
- **Failure surface** — new ways the system can break that did not exist before.
- **Testing** — what is now hard to test, and how to test it anyway.

## 10. Related concepts

- **Builds on:** prerequisites
- **Composes with:** patterns commonly deployed alongside
- **Conflicts with / tension:** patterns that pull in the opposite direction
- **Contrast with:** patterns often confused with this one

All entries are links.

## 11. Exercises

Three, escalating:
1. **Trace it** — walk the pseudo-code through a specific failure by hand.
2. **Extend it** — add a capability or handle a new case.
3. **Break it** — find the input or timing that defeats the implementation shown.

## 12. References

Books, papers, and canonical write-ups. Author and title, not bare URLs.

---

**Previous:** [link] · **Next:** [link] · **Up:** [Module README](README.md)
```

---

## Rules for writing lessons

1. **The analogy must be mechanical.** "A circuit breaker is like an electrical circuit
   breaker" is not an analogy, it is an etymology. Explain *why* tripping the circuit
   protects the house.
2. **Show the bug before the fix.** Most patterns are only convincing next to the code
   they replace.
3. **Every pattern has a cost.** A lesson with an empty §9 is a lesson that has not been
   understood.
4. **Never introduce a term twice.** If a concept has a lesson, link to it; do not
   re-explain it.
5. **Code obeys the spec.** No language-specific syntax, no library names inside code
   blocks. Vendor names belong in prose and in §12.
