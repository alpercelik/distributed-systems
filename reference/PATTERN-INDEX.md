---
title: "Pattern index"
---

Every pattern in the course, alphabetically, with the problem it solves and its main cost.

**Legend:** ⭐ core · ◆ advanced · ▲ enterprise integration · ◇ domain modelling

For DDD specifically, the [DDD pattern reference](/reference/DDD-REFERENCE) has the full catalogue
with decision tables.

| Pattern | Solves | Main cost | Lesson |
|---|---|---|---|
| Aggregate ⭐◇ | Undefined consistency boundaries | Becomes transaction, lock and shard key — expensive to change | [06-02](/modules/domain-driven-design/02-entities-value-objects-and-aggregates) |
| Application service ◇ | Business rules leaking into controllers | Another layer; easily grows rules | [06-04](/modules/domain-driven-design/04-repositories-factories-and-the-application-layer) |
| Architecture fitness test ⭐ | Boundaries eroding silently | Tests to maintain; can entrench a wrong boundary | [07-02](/modules/modular-monolith/02-module-boundaries-and-enforcement) |
| Adaptive concurrency limits | Capacity that changes | A control loop that can oscillate | [02-06](/modules/resilience/06-load-shedding-and-backpressure) ◆ |
| Aggregator ▲ | Recombining split messages | Completeness is hard; state leaks | [05-05](/modules/messaging-and-eip/05-splitter-aggregator-and-scatter-gather) |
| Anti-corruption layer ▲ | A foreign model infecting yours | A mapping layer per dependency | [08-06](/modules/microservice-architecture/06-anti-corruption-layer) |
| API gateway ⭐ | Chatty clients; duplicated edge concerns | A component every request depends on | [08-02](/modules/microservice-architecture/02-api-gateway-and-backend-for-frontend) |
| Asynchronous messaging ⭐ | Temporal coupling | Duplicates, reordering, eventual consistency | [01-02](/modules/communication/02-asynchronous-messaging) |
| Backend-for-frontend ⭐ | One gateway serving incompatible clients | One BFF per client type to maintain | [08-02](/modules/microservice-architecture/02-api-gateway-and-backend-for-frontend) |
| Backpressure ◆ | Producers outpacing consumers | Pressure must reach something that can say no | [02-06](/modules/resilience/06-load-shedding-and-backpressure) |
| Blue/green deployment | Risky cutovers | 2× infrastructure; no help with schemas | [11-02](/modules/operations-and-evolution/02-deployment-strategies) |
| Bounded context ⭐ | Where to draw service lines | Duplicated data across contexts | [08-01](/modules/microservice-architecture/01-decomposition-and-bounded-contexts) |
| Bounded context ⭐◇ | One word meaning four things | Deliberate duplication; translation at edges | [06-05](/modules/domain-driven-design/05-strategic-design-bounded-contexts-and-context-maps) |
| Bulkhead ⭐ | One dependency consuming the process | Stranded capacity; sizing per dependency | [02-04](/modules/resilience/04-bulkhead) |
| Cache-aside ⭐ | Repeated expensive reads | Staleness; invalidation; stampedes | [03-03](/modules/scalability/03-caching) |
| Canary deployment ⭐ | 100% exposure to a new bug | Slower rollouts; needs good SLIs | [11-02](/modules/operations-and-evolution/02-deployment-strategies) |
| Canonical data model ▲ | N² mappings between systems | Becomes a committee and a mega-schema | [05-04](/modules/messaging-and-eip/04-message-translator-and-canonical-data-model) |
| Chaos engineering ◆ | Untested failure paths | Real risk; needs observability first | [09-04](/modules/availability-and-dr/04-chaos-engineering) |
| Channel adapter ▲ | Systems that speak no messaging | Idempotency at the adapter | [05-01](/modules/messaging-and-eip/01-channels-and-endpoints) |
| Circuit breaker ⭐ | Spending capacity on a dead dependency | Thresholds that cause their own outages | [02-03](/modules/resilience/03-circuit-breaker) |
| Compensating transaction ⭐ | Undoing a committed step | Compensation may not fully undo | [04-02](/modules/data-and-consistency/02-saga) |
| Competing consumers ⭐ | Scaling work processing | Destroys ordering | [05-02](/modules/messaging-and-eip/02-point-to-point-and-publish-subscribe) |
| Context map ◇ | Undocumented, political inter-team dependencies | Decays after every reorganisation | [06-05](/modules/domain-driven-design/05-strategic-design-bounded-contexts-and-context-maps) |
| Consistent hashing ◆ | Remapping on membership change | Balances keys, not load | [03-06](/modules/scalability/06-consistent-hashing) |
| Consensus (Raft/Paxos) ◆ | Agreement despite failures | Unavailable without a quorum; a round trip per decision | [04-07](/modules/data-and-consistency/07-consensus-and-leader-election) |
| Content-based router ▲ | Routing without coupling sender to receivers | A central point that can drop everything | [05-03](/modules/messaging-and-eip/03-message-router-and-filter) |
| CQRS ◆ | One model serving reads and writes badly | Two models; eventual consistency in the UI | [04-06](/modules/data-and-consistency/06-cqrs) |
| Conformist ◇ | An upstream that won't accommodate you | Full coupling to their model | [06-05](/modules/domain-driven-design/05-strategic-design-bounded-contexts-and-context-maps) |
| Database per service ⭐ | Schema coupling between services | No joins, no FKs, no transactions | [08-03](/modules/microservice-architecture/03-database-per-service) |
| Dead letter channel ⭐▲ | Messages that can never succeed | Needs an owner and a replay tool | [05-06](/modules/messaging-and-eip/06-dead-letter-channel-and-poison-messages) |
| Deadline propagation ⭐ | Timeouts that don't compose | Context plumbing everywhere | [02-01](/modules/resilience/01-timeouts-and-deadlines) |
| Domain event ⭐◇ | Consequences hard-coded into the handler | Flow no longer visible in one place | [06-03](/modules/domain-driven-design/03-domain-events-and-domain-services) |
| Domain service ◇ | Logic belonging to no single aggregate | Easily abused into an anaemic service layer | [06-03](/modules/domain-driven-design/03-domain-events-and-domain-services) |
| Event sourcing ◆ | Lost history; audit; temporal queries | Schema versioning forever; replay cost | [04-05](/modules/data-and-consistency/05-event-sourcing) |
| Expand/contract migration ⭐ | Schema changes breaking running code | Three releases per change | [11-02](/modules/operations-and-evolution/02-deployment-strategies) |
| Fallback ⭐ | A non-essential failure failing everything | Fallback code is rarely exercised | [02-07](/modules/resilience/07-fallback-and-graceful-degradation) |
| Factory ◇ | Complex construction that is itself a domain rule | Overkill for most aggregates | [06-04](/modules/domain-driven-design/04-repositories-factories-and-the-application-layer) |
| Feature flag / kill switch ⭐ | Rollback taking a deploy cycle | Flag debt; untested combinations | [11-03](/modules/operations-and-evolution/03-configuration-and-feature-flags) |
| Fencing token ⭐ | Zombie lease holders; split brain | Storage must enforce it | [10-01](/modules/performance-and-concurrency/01-concurrency-control) |
| Graceful degradation ⭐ | All-or-nothing availability | Requires a product-level tier ranking | [02-07](/modules/resilience/07-fallback-and-graceful-degradation) |
| Health check (liveness/readiness) | Traffic to broken instances | Badly scoped checks cause outages | [02-08](/modules/resilience/08-health-checks-and-self-healing) |
| Hedged request ◆ | Tail latency under fan-out | Extra load; idempotent operations only | [10-04](/modules/performance-and-concurrency/04-tail-latency-and-hedged-requests) |
| Idempotency key ⭐ | Duplicate side effects from retries | A dedup store on the hot path | [01-03](/modules/communication/03-delivery-guarantees-and-idempotency) |
| Idempotent consumer / inbox ⭐ | At-least-once delivery duplicating effects | An extra write per message | [04-04](/modules/data-and-consistency/04-idempotent-consumer-and-inbox) |
| Leader election ◆ | Work that must run exactly once | A consensus dependency | [04-07](/modules/data-and-consistency/07-consensus-and-leader-election) |
| Load balancing (P2C) ⭐ | Uneven distribution; slow instances | Per-backend state and measurement | [03-02](/modules/scalability/02-load-balancing) |
| Load shedding ◆ | Congestion collapse | Some users are refused | [02-06](/modules/resilience/06-load-shedding-and-backpressure) |
| Integration event ⭐◇ | Internal model becoming a public contract | A translation layer, versioned forever | [06-03](/modules/domain-driven-design/03-domain-events-and-domain-services) |
| Message filter ▲ | Consumers receiving irrelevant messages | Wasted transfer if done client-side | [05-03](/modules/messaging-and-eip/03-message-router-and-filter) |
| Message translator ▲ | Systems with incompatible models | Semantic errors are invisible | [05-04](/modules/messaging-and-eip/04-message-translator-and-canonical-data-model) |
| Modular monolith ⭐ | Distribution costs with no distribution benefit | No independent deploy or scale; needs enforced discipline | [07-01](/modules/modular-monolith/01-why-a-modular-monolith-first) |
| Module extraction ⭐ | One component with a genuinely different profile | Nine lessons of machinery, permanently | [07-05](/modules/modular-monolith/05-extracting-a-module-into-a-service) |
| Multi-region ◆ | Region loss; global latency; residency | 2–3× cost; cross-region latency is physics | [09-02](/modules/availability-and-dr/02-multi-region-architecture) |
| Optimistic concurrency ⭐ | Lost updates | Retries under contention | [10-01](/modules/performance-and-concurrency/01-concurrency-control) |
| Outbox (transactional) ⭐ | The dual-write problem | Duplicates guaranteed; a publisher to run | [04-03](/modules/data-and-consistency/03-transactional-outbox) |
| Partitioning / sharding ⭐ | One database's write ceiling | No cross-shard transactions; irreversible key | [03-04](/modules/scalability/04-partitioning-and-sharding) |
| Ports and adapters ⭐◇ | Infrastructure fused into the domain | More types; mapping code to maintain | [06-04](/modules/domain-driven-design/04-repositories-factories-and-the-application-layer) |
| Point-to-point channel ⭐▲ | Work executed more than once | No fan-out | [05-02](/modules/messaging-and-eip/02-point-to-point-and-publish-subscribe) |
| Process manager ▲ | Multi-step stateful flows | A central component; version management | [05-07](/modules/messaging-and-eip/07-process-manager-and-routing-slip) |
| Publish-subscribe ⭐▲ | Adding consumers without changing producers | You cannot enumerate consumers | [05-02](/modules/messaging-and-eip/02-point-to-point-and-publish-subscribe) |
| Rate limiting ⭐ | One caller consuming all capacity | Legitimate bursts rejected | [02-05](/modules/resilience/05-rate-limiting-and-throttling) |
| Recipient list ▲ | Sending to a computed set | Sender knows the recipients | [05-03](/modules/messaging-and-eip/03-message-router-and-filter) |
| Repository ⭐◇ | Persistence knowledge spread through the model | Not a query service — reads need a read model | [06-04](/modules/domain-driven-design/04-repositories-factories-and-the-application-layer) |
| Redundancy and failover ⭐ | Loss of an instance, host or zone | Failover itself can fail | [09-01](/modules/availability-and-dr/01-redundancy-and-failover) |
| Replication ⭐ | Read capacity; durability | Lag is user-visible | [03-05](/modules/scalability/05-replication) |
| Reservation / escrow | Contention on scarce resources | Expiry sweeping | [10-01](/modules/performance-and-concurrency/01-concurrency-control) |
| Resequencer ▲ | Out-of-order parts | A missing part stalls the sequence | [05-05](/modules/messaging-and-eip/05-splitter-aggregator-and-scatter-gather) |
| Resource pooling | Connection setup cost | A hard throughput ceiling if mis-sized | [10-03](/modules/performance-and-concurrency/03-resource-pooling) |
| Retry with backoff and jitter ⭐ | Transient failures reaching users | Amplification; requires idempotency | [02-02](/modules/resilience/02-retries-backoff-and-jitter) |
| Routing slip ▲ | Variable linear sequences | No branching; no visibility | [05-07](/modules/messaging-and-eip/07-process-manager-and-routing-slip) |
| Saga ⭐ | Cross-service consistency | No isolation; compensations to design | [04-02](/modules/data-and-consistency/02-saga) |
| Scatter-gather ▲ | Querying many sources | Latency is the slowest source | [05-05](/modules/messaging-and-eip/05-splitter-aggregator-and-scatter-gather) |
| Schema per module ⭐ | A convenient join ending the architecture | Cross-module reads need APIs or projections | [07-04](/modules/modular-monolith/04-data-and-transactions-in-a-modular-monolith) |
| Schema evolution ⭐ | Contract changes breaking consumers | Three releases per breaking change | [01-04](/modules/communication/04-serialization-and-schema-evolution) |
| Service discovery | Changing topology | Stale routing; another dependency | [01-05](/modules/communication/05-service-discovery) |
| Service mesh ◆ | Duplicated resilience across languages | Heavy ops; unsafe default retries | [08-04](/modules/microservice-architecture/04-sidecar-and-service-mesh) |
| Sidecar ◆ | Cross-cutting concerns in every codebase | CPU, memory and latency per pod | [08-04](/modules/microservice-architecture/04-sidecar-and-service-mesh) |
| Single-flight | Cache stampedes | Per-instance unless coordinated | [03-03](/modules/scalability/03-caching) |
| Splitter ▲ | Messages too large or heterogeneous | Reassembly must be designed | [05-05](/modules/messaging-and-eip/05-splitter-aggregator-and-scatter-gather) |
| Specification ◇ | The same conditional repeated in five places | An extra abstraction where an `if` would do | [06-06](/modules/domain-driven-design/06-modelling-in-practice) |
| Static stability | Fallbacks that fail | Constant bounded staleness; memory | [02-07](/modules/resilience/07-fallback-and-graceful-degradation) |
| Stateless service ⭐ | Instances that cannot be replaced | State moves to a shared bottleneck | [03-01](/modules/scalability/01-stateless-services-and-horizontal-scaling) |
| Strangler fig ⭐▲ | Replacing a system that cannot stop | Both systems run for a long time | [08-05](/modules/microservice-architecture/05-strangler-fig) |
| Timeout ⭐ | Unbounded waits | Too aggressive causes the outage it prevents | [02-01](/modules/resilience/01-timeouts-and-deadlines) |
| Ubiquitous language ⭐◇ | Four teams meaning four things by "confirmed" | Needs sustained access to domain experts | [06-01](/modules/domain-driven-design/01-ubiquitous-language-and-the-domain-model) |
| Two-phase commit | Cross-resource atomicity | Blocks on coordinator failure | [04-01](/modules/data-and-consistency/01-distributed-transactions-and-two-phase-commit) |
| Value object ⭐◇ | Primitive obsession; impossible values | More types than a primitive-typed model | [06-02](/modules/domain-driven-design/02-entities-value-objects-and-aggregates) |
| Work queue ⭐ | Slow work on the request path | Eventual consistency; a queue to operate | [10-02](/modules/performance-and-concurrency/02-asynchronous-processing-and-work-queues) |

---

**See also:** [DDD pattern reference](/reference/DDD-REFERENCE) · [Decision guide](/reference/DECISION-GUIDE) — start from a symptom · [Glossary](/GLOSSARY) · [Curriculum](/CURRICULUM)
