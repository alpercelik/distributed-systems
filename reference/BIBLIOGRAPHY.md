---
title: "Bibliography"
---

The sources this course is built from, grouped by how you would use them.

---

## Read these four

If you read nothing else, read these. Between them they cover most of the course at greater
depth than any summary can.

- **Martin Kleppmann, *Designing Data-Intensive Applications*** (O'Reilly, 2017). The best
  single book on distributed data. Ch. 4 (encoding), 5 (replication), 6 (partitioning), 7
  (transactions) and 9 (consistency and consensus) underpin Modules 00, 03 and 04.
- **Michael Nygard, *Release It!*, 2nd ed.** (Pragmatic Bookshelf, 2018). The origin of the
  stability patterns in Module 02 — circuit breaker, bulkhead, fail fast — written by someone
  who was there when they were needed.
- **Gregor Hohpe & Bobby Woolf, *Enterprise Integration Patterns*** (Addison-Wesley, 2003).
  Module 05 is essentially a modern reading of this book. Twenty years on, the vocabulary is
  still the standard.
- **Betsy Beyer et al., *Site Reliability Engineering*** (O'Reilly, 2016), free online. Ch. 21
  (overload), 22 (cascading failures), 26 (data integrity) and the SLO chapters are the basis
  of Modules 02, 07 and 09.

---

## By module

### 00 — Foundations

- Peter Deutsch & James Gosling, "The Eight Fallacies of Distributed Computing" (1994/97).
- Jim Waldo et al., "A Note on Distributed Computing" (Sun, 1994).
- Fischer, Lynch & Paterson, "Impossibility of Distributed Consensus with One Faulty Process" (1985).
- Chandra & Toueg, "Unreliable Failure Detectors for Reliable Distributed Systems" (1996).
- Huang et al., "Gray Failure: The Achilles' Heel of Cloud-Scale Systems" (HotOS 2017).
- Jeff Dean, "Numbers Everyone Should Know" (2009).
- Eric Brewer, "CAP Twelve Years Later: How the 'Rules' Have Changed" (IEEE Computer, 2012).
- Daniel Abadi, "Consistency Tradeoffs in Modern Distributed Database System Design" (2012) — PACELC.
- Werner Vogels, "Eventually Consistent" (ACM Queue, 2008).
- Gil Tene, "How NOT to Measure Latency" — on coordinated omission. Watch it.

### 01 — Communication

- Martin Kleppmann, *DDIA* Ch. 4 — encoding and evolution.
- Google, Protocol Buffers, "Updating A Message Type"; Apache Avro schema resolution.
- Confluent, "Schema Evolution and Compatibility".
- Martin Fowler, "TolerantReader", "Consumer-Driven Contracts".
- Stripe, "Idempotent Requests"; IETF draft, "The Idempotency-Key HTTP Header Field".
- Pat Helland, "Idempotence Is Not a Medical Condition" (ACM Queue, 2012).
- Jay Kreps, "The Log: What every software engineer should know…" (2013).
- Netflix Tech Blog, "Eureka" — and self-preservation mode.

### 02 — Resilience

- Michael Nygard, *Release It!*, 2nd ed., Part I.
- Google SRE Book, Ch. 21–22.
- Marc Brooker (AWS), "Exponential Backoff And Jitter" (2015).
- Bronson et al., "Metastable Failures in Distributed Systems" (HotOS 2021).
- Netflix Tech Blog, "Performance Under Load" — adaptive concurrency limits.
- Resilience4j documentation — the reference implementation, including slow-call rate.
- AWS Builders' Library: "Using load shedding to avoid overload", "Implementing health checks", "Static stability using Availability Zones".
- Brakmo & Peterson, "TCP Vegas" (1995) — the source of latency-gradient congestion control.

### 03 — Scalability

- Kleppmann, *DDIA* Ch. 5–6.
- Mitzenmacher, "The Power of Two Choices in Randomized Load Balancing" (1996).
- Twitter, "Load Balancing at Twitter" — P2C with peak-EWMA.
- Facebook, "Scaling Memcache at Facebook" (NSDI 2013).
- Vattani et al., "Optimal Probabilistic Cache Stampede Prevention" (VLDB 2015).
- DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store" (SOSP 2007).
- Karger et al., "Consistent Hashing and Random Trees" (STOC 1997).
- Mirrokni et al., "Consistent Hashing with Bounded Loads" (Google, 2016).
- Neil Gunther, *Guerrilla Capacity Planning* — the Universal Scalability Law.

### 04 — Data and consistency

- Garcia-Molina & Salem, "Sagas" (SIGMOD 1987).
- Jim Gray, "Notes on Data Base Operating Systems" (1978).
- Pat Helland, "Life Beyond Distributed Transactions: an Apostate's Opinion" (2007).
- Chris Richardson, *Microservices Patterns* (Manning, 2018) — Ch. 3–7.
- Gunnar Morling, "Reliable Microservices Data Exchange With the Outbox Pattern" (Debezium).
- Greg Young, "CQRS Documents" (2010); Martin Fowler, "Event Sourcing" (2005).
- Overeem et al., "An Empirical Characterization of Event Sourced Systems and Their Schema Evolution" (2021).
- Ongaro & Ousterhout, "In Search of an Understandable Consensus Algorithm" (Raft, 2014).
- Lamport, "Paxos Made Simple" (2001).
- Burrows, "The Chubby Lock Service" (OSDI 2006).
- Corbett et al., "Spanner" (OSDI 2012).

### 05 — Messaging and enterprise integration

- Hohpe & Woolf, *Enterprise Integration Patterns*; enterpriseintegrationpatterns.com.
- Gregor Hohpe, "Enterprise Integration Patterns: 20 years later".
- Apache Camel and Spring Integration documentation — the catalogue as running code.
- Uber Engineering, "Building Reliable Reprocessing and Dead Letter Queues with Apache Kafka".
- Confluent, "Exactly-Once Semantics Are Possible: Here's How Kafka Does It" — including the limits.
- Bernd Rücker, *Practical Process Automation* (O'Reilly, 2021).
- Temporal documentation — durable execution and workflow versioning.

### 06 — Domain-driven design

- Eric Evans, *Domain-Driven Design* (2003). Part IV (strategic design) first; it is the most valuable third.
- Eric Evans, "Domain-Driven Design Reference" (2015) — free, and the clearest pattern summary.
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013); "Effective Aggregate Design" (2011), parts I–III.
- Vlad Khononov, *Learning Domain-Driven Design* (2021) — the best modern introduction, especially on subdomains.
- Scott Wlaschin, *Domain Modeling Made Functional* (2018) — making illegal states unrepresentable.
- Alexis King, "Parse, don't validate" (2019).
- Martin Fowler, "AnemicDomainModel", "DomainEvent", "ValueObject".
- Alberto Brandolini, *EventStorming*; Stefan Hofer & Henning Schwentner, *Domain Storytelling* (2021).
- Alistair Cockburn, "Hexagonal Architecture"; Robert C. Martin, "The Clean Architecture".
- Michiel Overeem et al., on event-sourced schema evolution in practice (2021).

### 07 — The modular monolith

- Simon Brown, "Modular Monoliths" (2015) and *Software Architecture for Developers*.
- Kamil Grzybek, "Modular Monolith" series and reference implementation — the most complete worked example available.
- Oliver Drotbohm, Spring Modulith documentation — enforcement, module testing, event publication registry.
- Sam Newman, *Monolith to Microservices* (2019) — Ch. 1, 3 and 4.
- Martin Fowler, "MonolithFirst" (2015), "Microservice Premium", "BranchByAbstraction".
- Neal Ford, Rebecca Parsons, Patrick Kua, *Building Evolutionary Architectures* (2017) — fitness functions.
- Kirk Knoernschild, *Java Application Architecture* (2012) — module design principles.
- Shopify Engineering, "Deconstructing the Monolith" (2019).
- Amazon Prime Video Tech Blog (2023) — consolidating distributed components back into one.
- DHH, "The Majestic Monolith" (2016).
- ArchUnit, NetArchTest, import-linter, dependency-cruiser — the enforcement tooling.

### 08 — Microservice architecture

- Eric Evans, *Domain-Driven Design* (Addison-Wesley, 2003) — bounded contexts, ACL, published language.
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013).
- Sam Newman, *Building Microservices*, 2nd ed. (O'Reilly, 2021) and *Monolith to Microservices* (2019).
- Martin Fowler, "MonolithFirst", "StranglerFigApplication", "BranchByAbstraction".
- Sam Newman, "Backends For Frontends" (2015).
- Brendan Burns & David Oppenheimer, "Design Patterns for Container-based Distributed Systems" (HotCloud 2016).
- Istio, Linkerd and Envoy documentation.
- GitHub Engineering, "Move Fast and Fix Things" — the Scientist library and comparison running.
- Melvin Conway, "How Do Committees Invent?" (1968).
- Alberto Brandolini, *EventStorming*.

### 09 — Availability and disaster recovery

- Google SRE Book, Ch. 22–23, 26.
- AWS Builders' Library — static stability, avoiding fallback, health checks.
- Netflix Tech Blog, "Active-Active for Multi-Regional Resiliency" (2013).
- Shopify Engineering, "Pods" — regional partitioning at scale.
- Gitlab, "Postmortem of database outage of January 31 2017". Read it in full.
- Basiri et al., "Chaos Engineering" (IEEE Software, 2016); principlesofchaos.org.
- Rosenthal & Jones, *Chaos Engineering* (O'Reilly, 2020).
- Kyle Kingsbury, the *Jepsen* reports — jepsen.io.

### 10 — Performance and concurrency

- Dean & Barroso, "The Tail at Scale" (CACM, 2013). Essential.
- Martin Kleppmann, "How to do distributed locking" (2016) — fencing tokens.
- John Little, "A Proof for the Queuing Formula L = λW" (1961).
- HikariCP documentation, "About Pool Sizing".
- Brandur Leach, "Transactionally Staged Job Drains in Postgres"; "Managing Postgres connections".
- Shapiro et al., "Conflict-free Replicated Data Types" (2011).

### 09 — Operations and evolution

- Google SRE Book Ch. 4, 6, 8, 27; *The Site Reliability Workbook* Ch. 5 (burn-rate alerting).
- Charity Majors, Liz Fong-Jones & George Miranda, *Observability Engineering* (O'Reilly, 2022).
- OpenTelemetry documentation.
- Tom Wilkie, "The RED Method"; Brendan Gregg, "The USE Method".
- Humble & Farley, *Continuous Delivery* (2010).
- Forsgren, Humble & Kim, *Accelerate* (2018).
- Martin Fowler & Pete Hodgson, "Feature Toggles (aka Feature Flags)" (2017).
- Michael Nygard, "Documenting Architecture Decisions" (2011).
- Gregor Hohpe, *The Software Architect Elevator* (O'Reilly, 2020).

---

## Where to go next

**If you want depth on data:** Kleppmann, then the Dynamo, Spanner and Raft papers, then Jepsen.

**If you want depth on operations:** the Google SRE Book and Workbook, then *Observability
Engineering*, then real postmortems — Gitlab's, and the published AWS and Cloudflare
post-incident reports, which are unusually honest and unusually instructive.

**If you want depth on design:** Evans, then Khononov for a gentler modern route into the same
material, then Newman, then Hohpe's *Software Architect Elevator* for the organisational half
that no technical book covers. The [DDD pattern reference](/reference/DDD-REFERENCE) is the map.

**If you want to practise:** run a game day ([09-04](/modules/availability-and-dr/04-chaos-engineering)),
write a decision record for your own system
([11-04](/modules/operations-and-evolution/04-capstone-designing-a-system)), and do
the "Break it" exercise in every lesson. Reading a pattern catalogue produces the illusion of
competence; finding the bug in the code you were shown does not.

---

**See also:** [Pattern index](/reference/PATTERN-INDEX) · [Decision guide](/reference/DECISION-GUIDE) · [Curriculum](/CURRICULUM)
