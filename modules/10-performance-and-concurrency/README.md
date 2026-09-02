---
title: "Performance and concurrency"
---

> Meeting a latency budget when many things happen at once and some of them collide.

## What you will be able to do

- Prevent lost updates without holding a lock across a network.
- Move work off the request path, and know what that costs the user.
- Size a connection pool from evidence rather than from a default.
- Explain why your p99 is terrible when every dependency's p99 is fine, and fix it.

## Lessons

| # | Lesson | The problem it solves |
|---|---|---|
| 10-01 | [Concurrency control](/modules/performance-and-concurrency/01-concurrency-control) | Two writers, one record, one lost update |
| 10-02 | [Asynchronous processing and work queues](/modules/performance-and-concurrency/02-asynchronous-processing-and-work-queues) | Slow work on a fast request path |
| 10-03 | [Resource pooling](/modules/performance-and-concurrency/03-resource-pooling) | The invisible ceiling on throughput |
| 10-04 | [Tail latency and hedged requests](/modules/performance-and-concurrency/04-tail-latency-and-hedged-requests) | p99 dominating the user experience |

## The one idea

**Performance problems in distributed systems are almost never about the speed of code. They
are about queueing.**

A request is slow because it waited: for a lock, for a connection, for a thread, for the
slowest of five parallel calls. Every lesson here is about a different queue:

```mermaid
graph LR
  L[Lock contention<br/>10-01] --> Q[Work queue<br/>10-02]
  Q --> P[Connection pool<br/>10-03]
  P --> T[The slowest of N<br/>10-04]
```

Which means the tools are the ones from
[00-04](/modules/foundations/04-latency-throughput-and-back-of-envelope): Little's Law to
size the queue, utilisation to predict the cliff, and percentiles to see what users actually
experience.

## ShopFlow at the end of this module

Two customers racing for the last unit produce one sale and one clear rejection, with no
distributed lock. Order confirmation emails, search indexing and analytics happen off the
request path. Connection pools are sized from measurements, and the p99 of the product page
is 90ms rather than 900ms despite fanning out to six services.

---

**Up:** [Curriculum](/CURRICULUM) · **Previous:** [← Module 09](/modules/availability-and-dr/README) · **Next:** [10-01 Concurrency control →](/modules/performance-and-concurrency/01-concurrency-control)
