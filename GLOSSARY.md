---
title: "Glossary"
---

Terms used across the course, each linked to the lesson that teaches it properly.

---

**ACID** — Atomicity, Consistency, Isolation, Durability. The guarantees of a single-database
transaction; none of them extends across services. [04-01](/modules/data-and-consistency/01-distributed-transactions-and-two-phase-commit)

**Aggregate** — a cluster of objects treated as one unit for consistency, with one root entity.
Simultaneously the transaction boundary, the concurrency unit and the natural partition key.
[06-02](/modules/domain-driven-design/02-entities-value-objects-and-aggregates)

**Anaemic domain model** — data classes with no behaviour and rules scattered across service
classes. Named as an anti-pattern by Fowler. [06-01](/modules/domain-driven-design/01-ubiquitous-language-and-the-domain-model)

**Application service** — use-case orchestration: load, call the domain, save, publish. Contains
no business rules. [06-04](/modules/domain-driven-design/04-repositories-factories-and-the-application-layer)

**Architecture fitness test** — an automated check that fails the build when a structural rule is
violated. What separates a modular monolith from a monolith with folders.
[07-02](/modules/modular-monolith/02-module-boundaries-and-enforcement)

**Amdahl's Law** — speedup is capped by the serialised fraction of the work. 5% serialised
means 20× maximum, forever. [03-01](/modules/scalability/01-stateless-services-and-horizontal-scaling)

**Anti-corruption layer (ACL)** — a translation boundary preventing a foreign model from
entering your codebase. [08-06](/modules/microservice-architecture/06-anti-corruption-layer)

**At-least-once / at-most-once** — the two honest delivery guarantees. Exactly-once *delivery*
does not exist; exactly-once *processing* does. [01-03](/modules/communication/03-delivery-guarantees-and-idempotency)

**Backpressure** — signalling a producer to slow down, rather than dropping its work.
[02-06](/modules/resilience/06-load-shedding-and-backpressure)

**Bounded context** — a boundary within which one model and one vocabulary hold. A *linguistic*
boundary, discovered in the domain — not the same thing as a service, which is a deployment
boundary. [06-05](/modules/domain-driven-design/05-strategic-design-bounded-contexts-and-context-maps)

**Bulkhead** — isolated resource pools so one dependency cannot consume the process.
[02-04](/modules/resilience/04-bulkhead)

**Context map** — the documented set of relationships between bounded contexts, including the
political ones. [06-05](/modules/domain-driven-design/05-strategic-design-bounded-contexts-and-context-maps)

**Core / supporting / generic subdomain** — where your differentiation lives, what merely
supports it, and what every business needs and nobody differentiates on. Build, build simply,
and buy, respectively. [06-05](/modules/domain-driven-design/05-strategic-design-bounded-contexts-and-context-maps)

**Burn rate** — how fast an error budget is being consumed. The right basis for alerting.
[11-01](/modules/operations-and-evolution/01-observability)

**CAP theorem** — during a network partition, choose availability or (linearizable)
consistency. Not "pick 2 of 3". [00-05](/modules/foundations/05-consistency-models-cap-and-pacelc)

**Canary** — exposing a new version to a small fraction of traffic and judging it against a
concurrent baseline. [11-02](/modules/operations-and-evolution/02-deployment-strategies)

**Cardinality** — the number of unique label combinations on a metric. Unbounded cardinality
destroys metrics backends. [11-01](/modules/operations-and-evolution/01-observability)

**Causal consistency** — if A caused B, nobody observes B without A. Usually what a product
actually needs. [00-05](/modules/foundations/05-consistency-models-cap-and-pacelc)

**CDC (change data capture)** — deriving an event stream from a database's replication log.
[04-03](/modules/data-and-consistency/03-transactional-outbox)

**Circuit breaker** — a three-state machine that stops calling a dependency that is failing.
[02-03](/modules/resilience/03-circuit-breaker)

**Command** — an imperative message with one intended handler, which may be rejected. Contrast
*event*. [01-02](/modules/communication/02-asynchronous-messaging)

**Compensating transaction** — a forward action that semantically undoes a committed step.
[04-02](/modules/data-and-consistency/02-saga)

**Congestion collapse** — throughput approaching zero under overload, sustained by retry load
even after the trigger is removed. [02-06](/modules/resilience/06-load-shedding-and-backpressure)

**Consistent hashing** — mapping keys to nodes so that adding or removing a node moves
approximately `1/N` of keys under uniform hashing. [03-06](/modules/scalability/06-consistent-hashing)

**Correlation ID** — an identifier tying together every message in one business flow. Without
it, asynchronous debugging is guesswork. [05-01](/modules/messaging-and-eip/01-channels-and-endpoints)

**CQRS** — separating the write model from purpose-built read models.
[04-06](/modules/data-and-consistency/06-cqrs)

**CRDT** — a data type that merges deterministically without coordination.
[00-05](/modules/foundations/05-consistency-models-cap-and-pacelc)

**Dead letter channel (DLQ)** — where messages go after exhausting retries. Useless without a
replay tool and an owner. [05-06](/modules/messaging-and-eip/06-dead-letter-channel-and-poison-messages)

**Deadline** — an absolute instant by which a whole request must complete, propagated to every
downstream call. Contrast *timeout*. [02-01](/modules/resilience/01-timeouts-and-deadlines)

**Domain event** — a record of something that happened, past tense, raised by an aggregate.
Internal to a context, and refactorable — unlike an *integration event*.
[06-03](/modules/domain-driven-design/03-domain-events-and-domain-services)

**Domain service** — stateless domain logic belonging to no single aggregate. Rare, and
frequently confused with an application service. [06-03](/modules/domain-driven-design/03-domain-events-and-domain-services)

**Distributed monolith** — services that must be deployed together. All the costs of
distribution, none of the benefits. [08-01](/modules/microservice-architecture/01-decomposition-and-bounded-contexts)

**Dual-write problem** — writing to a database and a broker separately; a crash between them
loses one. Solved by the outbox. [04-03](/modules/data-and-consistency/03-transactional-outbox)

**Entity** — an object with identity that persists as its values change. Contrast *value object*,
which most things should be. [06-02](/modules/domain-driven-design/02-entities-value-objects-and-aggregates)

**EventStorming** — a workshop format using sticky notes to discover events, policies, contexts
and aggregates from the domain rather than the schema.
[06-06](/modules/domain-driven-design/06-modelling-in-practice)

**Error budget** — `1 - SLO`. The permitted unreliability, and the basis for deciding whether
to ship or to stabilise. [11-01](/modules/operations-and-evolution/01-observability)

**Event** — a past-tense fact with zero or more listeners, which cannot be rejected. Contrast
*command*. [01-02](/modules/communication/02-asynchronous-messaging)

**Event sourcing** — storing events as the source of truth and deriving state by folding them.
[04-05](/modules/data-and-consistency/05-event-sourcing)

**Eventual consistency** — replicas converge given no new writes. Says nothing about how long.
[00-05](/modules/foundations/05-consistency-models-cap-and-pacelc)

**Expand/contract (parallel change)** — schema changes in three releases: add, migrate, remove.
[11-02](/modules/operations-and-evolution/02-deployment-strategies)

**Fallacies of distributed computing** — eight false assumptions, each a class of outage.
[00-02](/modules/foundations/02-fallacies-of-distributed-computing)

**Fencing token** — a monotonically increasing number carried with a lease and checked by the
*storage*, preventing a zombie holder from writing. [10-01](/modules/performance-and-concurrency/01-concurrency-control)

**Integration event** — a published, versioned contract crossing a context boundary. Must be
translated from domain events, never published directly.
[06-03](/modules/domain-driven-design/03-domain-events-and-domain-services)

**Gray failure** — a component that is up, passes health checks, and serves badly. Harder than
a crash. [00-03](/modules/foundations/03-failure-models-and-partial-failure)

**Hedged request** — a proactive second request sent at ~p95 to cut tail latency.
[10-04](/modules/performance-and-concurrency/04-tail-latency-and-hedged-requests)

**Idempotency** — running an operation more than once has the same effect as running it once.
[01-03](/modules/communication/03-delivery-guarantees-and-idempotency)

**Inbox pattern** — recording processed message IDs in the same transaction as the effect.
[04-04](/modules/data-and-consistency/04-idempotent-consumer-and-inbox)

**Jitter** — randomness added to a delay so that clients do not act in synchrony. The part of
backoff that actually matters. [02-02](/modules/resilience/02-retries-backoff-and-jitter)

**Lease** — a lock that expires. The holder may lose it without knowing.
[04-07](/modules/data-and-consistency/07-consensus-and-leader-election)

**Linearizability** — every read observes the most recent completed write, globally. The
strongest and most expensive consistency model. [00-05](/modules/foundations/05-consistency-models-cap-and-pacelc)

**Little's Law** — `L = λW`. Concurrency equals arrival rate times latency. The most useful
formula in the course. [00-04](/modules/foundations/04-latency-throughput-and-back-of-envelope)

**Liveness probe** — "would restarting this help?" Must not check shared dependencies.
[02-08](/modules/resilience/08-health-checks-and-self-healing)

**Load shedding** — deliberately refusing work you cannot complete.
[02-06](/modules/resilience/06-load-shedding-and-backpressure)

**Modular monolith** — one deployable with enforced internal module boundaries. Delivers module
ownership without a network, and keeps extraction cheap.
[07-01](/modules/modular-monolith/01-why-a-modular-monolith-first)

**Metastable failure** — a system that stays broken after its trigger is removed, sustained by
its own retry load. [02-02](/modules/resilience/02-retries-backoff-and-jitter)

**Outbox** — writing an event to a table in the same transaction as the state change, published
separately. [04-03](/modules/data-and-consistency/03-transactional-outbox)

**PACELC** — if Partitioned, choose Availability or Consistency; Else choose Latency or
Consistency. More useful than CAP. [00-05](/modules/foundations/05-consistency-models-cap-and-pacelc)

**Partial failure** — the third outcome of a remote call: not success, not failure, but *you
never find out*. The root of most difficulty. [00-03](/modules/foundations/03-failure-models-and-partial-failure)

**Policy** — a named rule of the form "whenever X happens, do Y", implemented as an event
handler. [06-03](/modules/domain-driven-design/03-domain-events-and-domain-services)

**Ports and adapters** — the domain defines interfaces (ports); infrastructure implements them
(adapters); dependencies point inward. Also called hexagonal or clean architecture.
[06-04](/modules/domain-driven-design/04-repositories-factories-and-the-application-layer)

**Poison message** — a message that always fails processing.
[05-06](/modules/messaging-and-eip/06-dead-letter-channel-and-poison-messages)

**Power of two choices (P2C)** — pick two backends at random, send to the less loaded. Nearly
optimal for nearly nothing. [03-02](/modules/scalability/02-load-balancing)

**Repository** — collection-like access to whole aggregates, hiding persistence. Serves the write
side; arbitrary queries belong in a read model.
[06-04](/modules/domain-driven-design/04-repositories-factories-and-the-application-layer)

**Quorum** — a protocol-sufficient subset of replicas. In consensus it is normally a majority,
so any two quorums intersect; read/write quorums can use other sizes with different guarantees.
[03-05](/modules/scalability/05-replication), [04-07](/modules/data-and-consistency/07-consensus-and-leader-election)

**Read-your-writes** — a session always observes its own writes. Usually the cheapest fix for
"it didn't save". [00-05](/modules/foundations/05-consistency-models-cap-and-pacelc)

**Readiness probe** — "can this instance serve right now?" Checks instance-local resources only.
[02-08](/modules/resilience/08-health-checks-and-self-healing)

**RED metrics** — Rate, Errors, Duration. The default service-level signals.
[11-01](/modules/operations-and-evolution/01-observability)

**Retry budget** — a system-wide cap on retries as a fraction of traffic. The most effective
control against retry storms. [02-02](/modules/resilience/02-retries-backoff-and-jitter)

**RPO / RTO** — how much data you may lose, and how long recovery may take.
[09-03](/modules/availability-and-dr/03-disaster-recovery-rpo-and-rto)

**Saga** — a sequence of local transactions with compensations, replacing a distributed
transaction. [04-02](/modules/data-and-consistency/02-saga)

**Scatter-gather** — querying many sources and combining the replies. Latency becomes the
slowest source's. [05-05](/modules/messaging-and-eip/05-splitter-aggregator-and-scatter-gather)

**Semantic lock** — marking an entity as in-progress so others know its state is not final.
[04-02](/modules/data-and-consistency/02-saga)

**Schema per module** — each module owns its database schema, enforced by database grants. The
data equivalent of a module boundary. [07-04](/modules/modular-monolith/04-data-and-transactions-in-a-modular-monolith)

**Shard** — a horizontal partition of data. [03-04](/modules/scalability/04-partitioning-and-sharding)

**Sidecar** — a proxy deployed alongside each service instance, handling transport concerns.
[08-04](/modules/microservice-architecture/04-sidecar-and-service-mesh)

**Single-flight** — collapsing concurrent misses for the same key into one downstream call.
[03-03](/modules/scalability/03-caching)

**SLI / SLO / SLA** — a measurement, a target, and a contract with consequences.
[11-01](/modules/operations-and-evolution/01-observability)

**Split brain** — two nodes both believing they are the leader, accepting conflicting writes.
[04-07](/modules/data-and-consistency/07-consensus-and-leader-election)

**Static stability** — behaving identically during a dependency failure because you were never
depending on it at request time. The best kind of fallback. [02-07](/modules/resilience/07-fallback-and-graceful-degradation)

**Strangler fig** — replacing a legacy system incrementally while it stays in production.
[08-05](/modules/microservice-architecture/05-strangler-fig)

**Supple design** — Evans' patterns for a model that stays changeable: intention-revealing
interfaces, side-effect-free functions, closure of operations, specifications.
[Reference](/reference/DDD-REFERENCE)

**Tail latency** — the slow end of the distribution (p99, p99.9). Under fan-out it dominates
what users experience. [10-04](/modules/performance-and-concurrency/04-tail-latency-and-hedged-requests)

**Thundering herd** — many clients acting simultaneously after a shared trigger.
[03-03](/modules/scalability/03-caching), [02-02](/modules/resilience/02-retries-backoff-and-jitter)

**Timeout** — a duration bound on a single call. Contrast *deadline*.
[02-01](/modules/resilience/01-timeouts-and-deadlines)

**Ubiquitous language** — one vocabulary shared by code, conversation and documentation, within
one bounded context. [06-01](/modules/domain-driven-design/01-ubiquitous-language-and-the-domain-model)

**Two generals problem** — no finite exchange of messages makes both parties certain the other
will act. Why exactly-once delivery is impossible. [00-03](/modules/foundations/03-failure-models-and-partial-failure)

**Two-phase commit (2PC)** — atomic commit across resources, which blocks if the coordinator
fails. [04-01](/modules/data-and-consistency/01-distributed-transactions-and-two-phase-commit)

**USE metrics** — Utilisation, Saturation, Errors. The resource-level counterpart to RED.
[11-01](/modules/operations-and-evolution/01-observability)

**Virtual node** — one of many ring positions per physical node, used to even out a consistent
hash. [03-06](/modules/scalability/06-consistent-hashing)

**Value object** — an object whose identity is its value: immutable, compared by fields, carrying
behaviour. The default choice over an entity.
[06-02](/modules/domain-driven-design/02-entities-value-objects-and-aggregates)

**Wide event** — one structured log event per request carrying every field that might matter.
What makes production queryable. [11-01](/modules/operations-and-evolution/01-observability)

---

**See also:** [DDD pattern reference](/reference/DDD-REFERENCE) · [Pattern index](/reference/PATTERN-INDEX) · [Decision guide](/reference/DECISION-GUIDE) · [Curriculum](/CURRICULUM)
