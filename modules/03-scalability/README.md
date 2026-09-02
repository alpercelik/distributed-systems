---
title: "Scalability"
---

> Serving ten times the traffic without being ten times slower. Every pattern here is a way
> of dividing work — across machines, across time, or across keys.

## What you will be able to do

- Make a service disposable, so that adding capacity is a number in a config.
- Pick a load-balancing algorithm for a reason rather than by default.
- Add a cache without creating a stampede, a staleness bug, or a new outage.
- Choose a partition key you will not regret in two years.
- Reason about replication lag as a product decision, not a database setting.

## Lessons

| # | Lesson | The limit it removes |
|---|---|---|
| 03-01 | [Stateless services and horizontal scaling](/modules/scalability/01-stateless-services-and-horizontal-scaling) | One machine's capacity |
| 03-02 | [Load balancing](/modules/scalability/02-load-balancing) | Uneven distribution across those machines |
| 03-03 | [Caching](/modules/scalability/03-caching) | Repeating expensive work |
| 03-04 | [Partitioning and sharding](/modules/scalability/04-partitioning-and-sharding) | One database's write capacity |
| 03-05 | [Replication](/modules/scalability/05-replication) | One database's read capacity, and its single failure domain |
| 03-06 | [Consistent hashing](/modules/scalability/06-consistent-hashing) | The cost of changing the number of nodes |

## The one idea

**Scalability is about what happens to the constant of proportionality when you add
resources.** A system scales if doubling the machines roughly doubles the throughput. Three
things prevent that, and they are the three enemies of this module:

1. **Shared mutable state** — every instance contending on one thing (03-01, 03-04).
2. **Uneven distribution** — one instance or one key taking most of the load (03-02, 03-04).
3. **Coordination** — work spent agreeing rather than serving (03-05, and
   [04-07](/modules/data-and-consistency/07-consensus-and-leader-election)).

Amdahl's Law puts a number on the first: if 5% of the work is serialised, no amount of
hardware gets you past 20× — and the Universal Scalability Law is worse, because coordination
overhead means throughput eventually goes *down* as you add machines.

## ShopFlow at the end of this module

The catalogue serves 12,000 req/s from 20 stateless instances behind a load balancer that
routes around slow hosts, with a two-tier cache absorbing 95% of it. Read replicas serve
order history, and the whole thing survives losing any single instance without anyone
noticing.

**The order store is not sharded.** 40M orders at ~2KB is 80GB, which fits comfortably on one
machine — so [03-04](/modules/scalability/04-partitioning-and-sharding) teaches partitioning against ShopFlow
as a worked hypothetical, and the
[capstone](/modules/operations-and-evolution/04-capstone-designing-a-system) rejects it with
that arithmetic. Knowing when *not* to shard is the more valuable half of that lesson.

---

**Up:** [Curriculum](/CURRICULUM) · **Previous:** [← Module 02](/modules/resilience/README) · **Next:** [03-01 Stateless services →](/modules/scalability/01-stateless-services-and-horizontal-scaling)
