---
title: "Foundations"
---

> Every pattern in the next nine modules is a response to something in this one. Skip it
> and you will memorise solutions to problems you have not felt.

## What you will be able to do

- Explain why an organisation splits a system, and what it pays for the privilege.
- Name the assumption that a given outage violated.
- Reason about "did my request succeed?" when the honest answer is *unknowable*.
- Do a capacity estimate on a whiteboard and be within an order of magnitude.
- Say precisely what "eventually consistent" means, and what a user will observe.

## Lessons

| # | Lesson | Why it matters |
|---|---|---|
| 00-01 | [Why distributed systems](/modules/foundations/01-why-distributed-systems) | The bill that arrives with the benefits |
| 00-02 | [The fallacies of distributed computing](/modules/foundations/02-fallacies-of-distributed-computing) | Eight false assumptions, eight classes of outage |
| 00-03 | [Failure models and partial failure](/modules/foundations/03-failure-models-and-partial-failure) | The single hardest fact about distribution |
| 00-04 | [Latency, throughput and back-of-envelope](/modules/foundations/04-latency-throughput-and-back-of-envelope) | Numbers, queues, percentiles |
| 00-05 | [Consistency models, CAP and PACELC](/modules/foundations/05-consistency-models-cap-and-pacelc) | What you give up, stated precisely |

## The one idea

In a single process, a function call either returns a value or throws. In a distributed
system, a call has a **third outcome**: you don't find out. Every pattern in Module 02
exists because of that third outcome, and every pattern in Module 04 exists because that
third outcome can leave two databases disagreeing.

## ShopFlow at the end of this module

Still a monolith. One process, one database, one deployment. Correct, simple, and about to
become impossible to change fast enough — which is where [Module 01](/modules/communication/README)
starts.

---

**Up:** [Curriculum](/CURRICULUM) · **Next:** [00-01 Why distributed systems →](/modules/foundations/01-why-distributed-systems)
