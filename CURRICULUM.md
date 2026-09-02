---
title: "Curriculum"
---

67 lessons, 12 modules, one running example. Each lesson is self-contained but assumes the
modules before it.

**The shape of the course**, and which entry point is yours: see
[the learning path](/#the-learning-path).

**Before lesson 1, read:** [Language spec](/spec/PSEUDOCODE-SPEC) → [Stdlib](/spec/STDLIB) → [ShopFlow](/domain/RUNNING-EXAMPLE). About 30 minutes.

**Legend:** ⭐ core pattern, everyone needs it · ◆ advanced, needed at scale · ▲ enterprise integration

---

## Module 00 — [Foundations](/modules/foundations/README)

*Why any of this is hard. The vocabulary and the physics.*

| # | Lesson | Key idea |
|---|---|---|
| 00-01 | [Why distributed systems](/modules/foundations/01-why-distributed-systems) ⭐ | The four forces that split a monolith, and the bill they come with |
| 00-02 | [The fallacies of distributed computing](/modules/foundations/02-fallacies-of-distributed-computing) ⭐ | Eight assumptions that are false, and what each one costs |
| 00-03 | [Failure models and partial failure](/modules/foundations/03-failure-models-and-partial-failure) ⭐ | Crash, omission, timing, Byzantine — and why "did it work?" is unanswerable |
| 00-04 | [Latency, throughput and back-of-envelope](/modules/foundations/04-latency-throughput-and-back-of-envelope) ⭐ | Little's Law, queueing, percentiles, numbers every engineer should know |
| 00-05 | [Consistency models, CAP and PACELC](/modules/foundations/05-consistency-models-cap-and-pacelc) ⭐ | Linearizable → causal → eventual, and what you actually give up |

## Module 01 — [Communication](/modules/communication/README)

*How services talk. The choice made here constrains every later choice.*

| # | Lesson | Key idea |
|---|---|---|
| 01-01 | [Synchronous request/response](/modules/communication/01-synchronous-request-response) ⭐ | RPC, REST, gRPC; temporal coupling and the latency chain |
| 01-02 | [Asynchronous messaging](/modules/communication/02-asynchronous-messaging) ⭐ | Queues and logs; trading latency certainty for availability |
| 01-03 | [Delivery guarantees and idempotency](/modules/communication/03-delivery-guarantees-and-idempotency) ⭐ | At-most/at-least/exactly-once; why the third one is a lie you can engineer around |
| 01-04 | [Serialization and schema evolution](/modules/communication/04-serialization-and-schema-evolution) ⭐ | Wire formats, forward/backward compatibility, the rules that prevent outages |
| 01-05 | [Service discovery](/modules/communication/05-service-discovery) | Client-side vs server-side, registries, health, DNS TTL traps |

## Module 02 — [Resilience](/modules/resilience/README)

*Staying up while your dependencies do not. The densest module in the course.*

| # | Lesson | Key idea |
|---|---|---|
| 02-01 | [Timeouts and deadlines](/modules/resilience/01-timeouts-and-deadlines) ⭐ | The most important pattern. Budgets that propagate, not constants that don't |
| 02-02 | [Retries, backoff and jitter](/modules/resilience/02-retries-backoff-and-jitter) ⭐ | How retries turn a blip into an outage, and how to stop that |
| 02-03 | [Circuit breaker](/modules/resilience/03-circuit-breaker) ⭐ | Fail fast when failing is certain; the three-state machine |
| 02-04 | [Bulkhead](/modules/resilience/04-bulkhead) ⭐ | Resource isolation so one sick dependency can't drown the process |
| 02-05 | [Rate limiting and throttling](/modules/resilience/05-rate-limiting-and-throttling) ⭐ | Token bucket, sliding window, distributed limiting, fair queuing |
| 02-06 | [Load shedding and backpressure](/modules/resilience/06-load-shedding-and-backpressure) ◆ | Refusing work is a feature; the queue is where latency hides |
| 02-07 | [Fallback and graceful degradation](/modules/resilience/07-fallback-and-graceful-degradation) ⭐ | Ranked feature tiers; a worse answer beats no answer |
| 02-08 | [Health checks and self-healing](/modules/resilience/08-health-checks-and-self-healing) | Liveness vs readiness; how a bad health check causes the outage |

## Module 03 — [Scalability](/modules/scalability/README)

*Serving more without getting slower.*

| # | Lesson | Key idea |
|---|---|---|
| 03-01 | [Stateless services and horizontal scaling](/modules/scalability/01-stateless-services-and-horizontal-scaling) ⭐ | Where state goes when the instance is disposable |
| 03-02 | [Load balancing](/modules/scalability/02-load-balancing) ⭐ | Round-robin vs least-loaded vs power-of-two-choices; why RR is often wrong |
| 03-03 | [Caching](/modules/scalability/03-caching) ⭐ | Layers, invalidation, stampedes, TTL jitter, negative caching |
| 03-04 | [Partitioning and sharding](/modules/scalability/04-partitioning-and-sharding) ⭐ | Key choice, hot partitions, cross-shard queries, resharding |
| 03-05 | [Replication](/modules/scalability/05-replication) ⭐ | Leader/follower, quorums, read-your-writes, replica lag |
| 03-06 | [Consistent hashing](/modules/scalability/06-consistent-hashing) ◆ | Adding a node without moving all the data; virtual nodes |

## Module 04 — [Data and consistency](/modules/data-and-consistency/README)

*Correctness when the data is in more than one place and something is on fire.*

| # | Lesson | Key idea |
|---|---|---|
| 04-01 | [Distributed transactions and 2PC](/modules/data-and-consistency/01-distributed-transactions-and-two-phase-commit) | The obvious solution, why it mostly loses, and when it still wins |
| 04-02 | [Saga](/modules/data-and-consistency/02-saga) ⭐ | Long-running consistency by compensation; orchestration vs choreography |
| 04-03 | [Transactional outbox](/modules/data-and-consistency/03-transactional-outbox) ⭐ | Commit the state change and the event atomically; CDC |
| 04-04 | [Idempotent consumer and inbox](/modules/data-and-consistency/04-idempotent-consumer-and-inbox) ⭐ | The receiving half of exactly-once semantics |
| 04-05 | [Event sourcing](/modules/data-and-consistency/05-event-sourcing) ◆ | The log is the truth; snapshots, replay, versioning |
| 04-06 | [CQRS](/modules/data-and-consistency/06-cqrs) ◆ | Separate write and read models; the staleness you now owe the user |
| 04-07 | [Consensus and leader election](/modules/data-and-consistency/07-consensus-and-leader-election) ◆ | Quorums, Raft in outline, split brain, fencing tokens |

## Module 05 — [Messaging and enterprise integration](/modules/messaging-and-eip/README)

*Connecting systems you do not own and cannot change.* ▲

| # | Lesson | Key idea |
|---|---|---|
| 05-01 | [Channels and endpoints](/modules/messaging-and-eip/01-channels-and-endpoints) ▲ | The EIP vocabulary; channel types and what each guarantees |
| 05-02 | [Point-to-point and publish/subscribe](/modules/messaging-and-eip/02-point-to-point-and-publish-subscribe) ▲ | Competing consumers, fan-out, durable subscriptions |
| 05-03 | [Message router and filter](/modules/messaging-and-eip/03-message-router-and-filter) ▲ | Content-based routing, recipient list, dynamic router |
| 05-04 | [Message translator and canonical data model](/modules/messaging-and-eip/04-message-translator-and-canonical-data-model) ▲ | N² mappings → 2N; when the canonical model becomes the problem |
| 05-05 | [Splitter, aggregator and scatter-gather](/modules/messaging-and-eip/05-splitter-aggregator-and-scatter-gather) ▲ | Decomposing and recomposing; correlation and completeness |
| 05-06 | [Dead letter channel and poison messages](/modules/messaging-and-eip/06-dead-letter-channel-and-poison-messages) ⭐▲ | Where bad messages go, and how to get them back |
| 05-07 | [Process manager and routing slip](/modules/messaging-and-eip/07-process-manager-and-routing-slip) ▲ | Stateful multi-step flows; the EIP name for an orchestrated saga |

## Module 06 — [Domain-driven design](/modules/domain-driven-design/README)

*Where the boundaries come from. Every later boundary decision is made here.*

| # | Lesson | Key idea |
|---|---|---|
| 06-01 | [Ubiquitous language and the domain model](/modules/domain-driven-design/01-ubiquitous-language-and-the-domain-model) ⭐ | One word, one meaning; making illegal states unrepresentable |
| 06-02 | [Entities, value objects and aggregates](/modules/domain-driven-design/02-entities-value-objects-and-aggregates) ⭐ | The consistency boundary that becomes your transaction, lock and shard key |
| 06-03 | [Domain events and domain services](/modules/domain-driven-design/03-domain-events-and-domain-services) ⭐ | Domain vs integration events; policies instead of 400-line handlers |
| 06-04 | [Repositories, factories and the application layer](/modules/domain-driven-design/04-repositories-factories-and-the-application-layer) ⭐ | Ports and adapters; keeping the database out of the model |
| 06-05 | [Strategic design: bounded contexts and context maps](/modules/domain-driven-design/05-strategic-design-bounded-contexts-and-context-maps) ⭐ | Core/supporting/generic; the nine relationship patterns |
| 06-06 | [Modelling in practice](/modules/domain-driven-design/06-modelling-in-practice) | EventStorming; refactoring toward deeper insight |

## Module 07 — [The modular monolith](/modules/modular-monolith/README)

*Most of what microservices promise, without the network. And the exit, kept open.*

| # | Lesson | Key idea |
|---|---|---|
| 07-01 | [Why a modular monolith first](/modules/modular-monolith/01-why-a-modular-monolith-first) ⭐ | The two benefits boundaries can't give you, and the four costs they avoid |
| 07-02 | [Module boundaries and enforcement](/modules/modular-monolith/02-module-boundaries-and-enforcement) ⭐ | Architecture tests; an unenforced boundary is already crossed |
| 07-03 | [In-process communication between modules](/modules/modular-monolith/03-in-process-communication-between-modules) ⭐ | Calls, events and read models — chosen to match the distributed equivalent |
| 07-04 | [Data and transactions in a modular monolith](/modules/modular-monolith/04-data-and-transactions-in-a-modular-monolith) ⭐ | Schema per module; every shared transaction is a future extraction cost |
| 07-05 | [Extracting a module into a service](/modules/modular-monolith/05-extracting-a-module-into-a-service) ⭐ | The payoff: a week, not a quarter |

## Module 08 — [Microservice architecture](/modules/microservice-architecture/README)

*Where to draw the lines, and how to move them later.*

| # | Lesson | Key idea |
|---|---|---|
| 08-01 | [Decomposition and bounded contexts](/modules/microservice-architecture/01-decomposition-and-bounded-contexts) ⭐ | Cut along change, not along nouns; the distributed monolith smell |
| 08-02 | [API gateway and backend-for-frontend](/modules/microservice-architecture/02-api-gateway-and-backend-for-frontend) ⭐ | One front door; aggregation, auth, and the chatty-client problem |
| 08-03 | [Database per service](/modules/microservice-architecture/03-database-per-service) ⭐ | Private data, and every join you just gave up |
| 08-04 | [Sidecar and service mesh](/modules/microservice-architecture/04-sidecar-and-service-mesh) ◆ | Moving resilience out of the app; mTLS, retries, traffic shifting |
| 08-05 | [Strangler fig](/modules/microservice-architecture/05-strangler-fig) ⭐▲ | Replacing a legacy system while it stays in production |
| 08-06 | [Anti-corruption layer](/modules/microservice-architecture/06-anti-corruption-layer) ▲ | Keeping someone else's bad model out of your codebase |

## Module 09 — [Availability and disaster recovery](/modules/availability-and-dr/README)

*Surviving the loss of a machine, a rack, a region, a decision.*

| # | Lesson | Key idea |
|---|---|---|
| 09-01 | [Redundancy and failover](/modules/availability-and-dr/01-redundancy-and-failover) ⭐ | Active-passive vs active-active; failover is a distributed algorithm |
| 09-02 | [Multi-region architecture](/modules/availability-and-dr/02-multi-region-architecture) ◆ | Data gravity, write routing, conflict resolution, cost |
| 09-03 | [Disaster recovery: RPO and RTO](/modules/availability-and-dr/03-disaster-recovery-rpo-and-rto) ⭐ | Backups you have restored vs backups you have taken |
| 09-04 | [Chaos engineering](/modules/availability-and-dr/04-chaos-engineering) ◆ | Proving the patterns work before the incident does it for you |

## Module 10 — [Performance and concurrency](/modules/performance-and-concurrency/README)

*Meeting a latency budget under contention.*

| # | Lesson | Key idea |
|---|---|---|
| 10-01 | [Concurrency control](/modules/performance-and-concurrency/01-concurrency-control) ⭐ | Optimistic vs pessimistic, leases, fencing tokens, lost updates |
| 10-02 | [Asynchronous processing and work queues](/modules/performance-and-concurrency/02-asynchronous-processing-and-work-queues) ⭐ | Getting work off the request path; batching; priority |
| 10-03 | [Resource pooling](/modules/performance-and-concurrency/03-resource-pooling) | Connection pools as the hidden bulkhead; sizing by Little's Law |
| 10-04 | [Tail latency and hedged requests](/modules/performance-and-concurrency/04-tail-latency-and-hedged-requests) ◆ | Why p99 dominates fan-out, and the tricks that fix it |

## Module 11 — [Operations and evolution](/modules/operations-and-evolution/README)

*Changing a running system without fear.*

| # | Lesson | Key idea |
|---|---|---|
| 11-01 | [Observability](/modules/operations-and-evolution/01-observability) ⭐ | Logs, metrics, traces; RED/USE; SLOs and error budgets |
| 11-02 | [Deployment strategies](/modules/operations-and-evolution/02-deployment-strategies) ⭐ | Rolling, blue/green, canary; expand-contract schema migration |
| 11-03 | [Configuration and feature flags](/modules/operations-and-evolution/03-configuration-and-feature-flags) | Decoupling deploy from release; kill switches as a resilience pattern |
| 11-04 | [Capstone: designing a system](/modules/operations-and-evolution/04-capstone-designing-a-system) ⭐ | Assembling everything into one design, with the trade-offs argued |

---

## Suggested paths

**Complete (recommended)** — 00 → 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11.

**"My service keeps falling over"** — 00-02, 00-03 → all of Module 02 → 10-03 → 11-01.

**"We're splitting the monolith"** — 00-01 → Module 06 → Module 07 → 08-01, 08-03, 08-05, 08-06 → 04-02, 04-03.

**"We're starting a new system"** — 00-01, 00-04 → Module 06 → Module 07 → stop. Return when [07-01](/modules/modular-monolith/01-why-a-modular-monolith-first)'s test says yes.

**"How do we model this domain?"** — all of Module 06 → 07-02 → 04-02, 04-05.

**"Integrate this legacy system"** — 01-02, 01-03 → Module 05 → 08-05, 08-06.

**"It's too slow"** — 00-04 → Module 03 → 10-01…10-04.

**"Data keeps going wrong"** — 00-05 → Module 04 → 03-05.

**Interview preparation** — 00-04, 00-05, 03-02…03-06, 04-01, 04-02, 08-01, 11-04.

---

## Cross-cutting reference

- [DDD pattern reference](/reference/DDD-REFERENCE) — the complete DDD catalogue in one page
- [Pattern index](/reference/PATTERN-INDEX) — every pattern, alphabetically, with its problem
- [Decision guide](/reference/DECISION-GUIDE) — start from a symptom, arrive at a pattern
- [Glossary](/GLOSSARY) — terms, with links to where they are taught
- [Bibliography](/reference/BIBLIOGRAPHY) — the books and papers this course is built from
