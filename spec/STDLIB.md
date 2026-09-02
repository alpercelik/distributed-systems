---
title: "DSPL Standard Library"
---

> The built-in primitives every lesson may use without defining them. Each one is a
> deliberately thin stand-in for a real piece of infrastructure — the point is that you
> can see *which* piece of infrastructure a pattern depends on.

**Contents:** [Storage](#storage) · [Messaging](#messaging) · [Remote calls](#remote-calls) ·
[Caching](#caching) · [Coordination](#coordination) · [Resilience primitives](#resilience-primitives) ·
[Time and randomness](#time-and-randomness) · [Observability](#observability) ·
[Mapping to real technology](#mapping-to-real-technology)

---

## Storage

### `Store<K, V>` — a durable key-value store

Stands in for a database table, a document collection, or a KV store. Single-key operations are
atomic. An `atomically:` block may span multiple declared stores only when the lesson explicitly
states that they share one local database transaction; it never crosses a service boundary.

```
store.get(k) -> Option<V>
store.put(k, v)
store.delete(k)
store.put_if_absent(k, v) -> Bool           # true if it was written
store.compare_and_swap(k, expected, v) -> Bool
store.scan(prefix) -> List<(K, V)>
store.query(predicate) -> List<V>           # "a query happens here", details elided
```

`compare_and_swap` is how optimistic concurrency control is expressed:

```
if not orders.compare_and_swap(id, expected: v3, value: v4):
  raise ConflictError
```

#### Extended operations

Used throughout the lessons. Each maps to something every real datastore provides; each is
**atomic per key**, and none is atomic across keys unless wrapped in `atomically:`.

```
store.update(k, changes: Map)          -> Bool    # partial update; false if absent
store.update_where(pred, set: changes) -> Int     # conditional bulk update, rows affected
store.delete_where(pred)               -> Int     # bulk delete, rows affected
store.query(pred, order_by: f, limit: n) -> List<V>
store.count(pred)                      -> Int
```

`update_where` deserves its own note: it is the primitive behind lost-update-free counters,
because the predicate and the write are evaluated together.

```
# The whole of "reserve stock without a lock" (10-01):
rows = stock.update_where(sku: sku, available_gte: qty,
                          set: {available: expr("available - " + qty)})
return rows == 1 ? Ok(unit) : Err(OutOfStock)
```

#### Fenced writes

For resources protected by a lease ([04-07](/modules/data-and-consistency/07-consensus-and-leader-election)).
The token comparison and the write are **one atomic, durable operation inside the store** —
this is the entire point, and a token cached in process memory provides no protection at all.

```
store.compare_and_swap_fenced(k, value, token: Int) -> Bool
  # Atomically: if token >= the highest token this store has durably seen for k,
  # persist BOTH the new value and the token, and return true.
  # Otherwise change nothing and return false.
```

### `Log<T>` — an ordered, append-only sequence

The abstraction behind event sourcing, replication logs, and Kafka partitions.

```
log.append(entry) -> Offset
log.append_if_version(stream, expected: Int, entries: List<T>) -> Bool
  # Atomically appends only if the stream is still at expected; false means a concurrent writer won.
log.read(from: Offset, limit: Int) -> List<(Offset, T)>
log.truncate(before: Offset)
log.latest_offset() -> Offset
```

---

## Messaging

### `Queue<T>` — point-to-point, competing consumers

Exactly one consumer processes each message. Delivery is **at-least-once** unless stated.

```
queue.send(msg)
queue.send(msg, delay: 30s)
queue.receive() -> Option<Delivery<T>>       # leases the message
queue.depth() -> Int
```

A `Delivery<T>` must be resolved, or its lease expires and it is redelivered:

```
d = queue.receive()
d.body          # the message
d.attempt       # 1 on first delivery, 2+ on redelivery
d.ack()         # done, remove it
d.nack()        # failed, redeliver now
d.retry(after: 10s)
d.dead_letter(reason)
```

### `Topic<T>` — publish/subscribe, one message to many subscribers

```
topic.publish(msg)
topic.publish(msg, key: partition_key)       # ordering guaranteed per key only
```

Subscription is declared inside a service, not called:

```
service ShippingService:
  on event OrderPaid(e):
    ...
```

### `Channel<T>` — an in-process pipe with a bounded buffer

Used for backpressure and worker-pool examples.

```
ch = Channel<Task>(capacity: 100)
ch.send(t)                 # blocks when full  <- this IS backpressure
ch.try_send(t) -> Bool     # false when full   <- this IS load shedding
ch.receive() -> T
```

---

## Remote calls

### `Client<S>` — a handle to another service

Every method on it crosses a network. Every call can time out, be refused, or return an
answer that arrives after you stopped caring.

```
client.method(args) -> Result<T, E>          # always awaited
client.method(args) timeout 500ms
```

The client is the seam where resilience patterns attach:

```
uses payments: Client<PaymentService>
  with timeout(800ms),
       retry(max: 2, backoff: exponential(base: 50ms, jitter: full)),
       circuit_breaker(threshold: 5, cooldown: 30s),
       bulkhead(size: 20)
```

That `with` clause is the entire content of Module 02, written as configuration.

---

## Caching

### `Cache<K, V>`

```
cache.get(k) -> Option<V>
cache.put(k, v, ttl: 5m)
cache.invalidate(k)
cache.get_or_load(k, ttl: 5m, load: () => ...)     # single-flight: one loader per key

# Entry-level access, for stale-on-error and negative caching (03-03, 02-07)
cache.get_entry(k) -> Option<Entry>                # entry.value, entry.age, entry.is_negative
cache.get_stale(k) -> Option<V>                    # expired but still present
cache.put_negative(k, ttl: 30s)                    # remember that k does not exist
```

`get_or_load` collapses concurrent misses for the same key into one downstream call —
that collapsing is the difference between a cache miss and a
[cache stampede](/modules/scalability/03-caching).

---

## Coordination

### `Lock` — a distributed lease

```
with lock(key, ttl: 10s):
  ...
```

A lease, not a lock: it expires. Code inside must still be safe if a second holder
appears — see [fencing tokens](/modules/performance-and-concurrency/01-concurrency-control).

```
lease = lock.acquire(key, ttl: 10s) -> Option<Lease>
lease.token         # monotonically increasing fencing token
lease.renew()
lease.release()
```

### `Mutex` — an in-process critical section

Not distributed, not a lease, cannot expire. Guards mutable `state` inside one process, which
is what a circuit breaker, a token bucket and a single-flight registry all need.

```
state lock: Mutex

with lock:                     # exclusive within this process. Blocks briefly.
  ...                          # keep it short: no I/O, no awaits inside
```

**Never `await` inside a `Mutex`.** Holding a lock across a network call serialises every
caller behind the slowest one — the failure [08-01](/modules/performance-and-concurrency/01-concurrency-control)
warns about, in miniature.

### `Promise<T>` — a value that will exist later

Lets one caller install a placeholder that others await, which is how single-flight
([03-03](/modules/scalability/03-caching)) collapses concurrent misses without a
check-then-act race.

```
p = Promise<Result<Product, Error>>()
p.complete(value)              # resolve it, once
await p                        # any number of waiters
```

### `Election` — leader election

```
election.campaign(role: "sweeper") -> Option<Lease>
election.is_leader() -> Bool
on leadership_lost:
  stop_background_work()
```

---

## Resilience primitives

These are *defined* in Module 02; the definitions live in the lessons, the signatures live
here so earlier lessons can reference them.

```
CircuitBreaker(failure_threshold: Int, cooldown: Duration, half_open_probes: Int = 1)
  .is_open() -> Bool
  .record_success()
  .record_failure()
  .state -> CLOSED | OPEN | HALF_OPEN

RateLimiter(rate: 1000/s, burst: Int)
  .try_acquire(n: Int = 1) -> Bool
  .acquire()                            # blocks

Bulkhead(size: Int, queue: Int = 0)
  .try_enter() -> Bool
  with bulkhead("payments"): ...

Retry(max: Int, backoff: Backoff, retry_on: List<ErrorKind>)
backoff strategies: fixed(d) | exponential(base, cap) | jitter: none|full|equal|decorrelated
```

---

## Time and randomness

Always injected, never ambient — this is what makes the examples testable.

```
now() -> Instant
sleep(d: Duration)
after(d: Duration, fn)                   # schedule
deadline(t: Instant)                     # see spec §8
random() -> Float                        # [0, 1)
uuid() -> UUID
jitter(d: Duration) -> Duration          # random in [0, d)
```

---

## Observability

```
log.info("order placed", order_id: id)
log.error("charge failed", err: e, order_id: id)

metrics.increment("orders.placed", tags: {status: "paid"})
metrics.gauge("queue.depth", queue.depth())
metrics.histogram("charge.latency_ms", elapsed)

with span("payments.charge", order_id: id):    # distributed trace span
  ...
trace_id()                                     # propagated across every call
```

Every network call in every lesson is assumed to carry `trace_id`, `deadline`, and
`idempotency_key` in its context, whether or not the code shows it. Where it matters, it
is shown.

---

## Shorthand and escape hatches

Two things in the lessons are *not* part of this library, deliberately. Both are labelled where
they appear, and neither should be read as a promise the library makes.

**Lesson-local helpers.** A lesson may give a `Store` a domain-named method when the name
carries more meaning than the query would:

```
outbox.unpublished(limit: 100)      # shorthand for query(published_at: None, limit: 100)
outbox.mark_published(id)           # shorthand for update(id, {published_at: now()})
replica.replication_position()      # a datastore-specific introspection call
```

These are always defined by the surrounding lesson, and always reducible to the operations
above. If you cannot see how a helper reduces to `query`/`update`/`compare_and_swap`, that is a
bug in the lesson.

**Raw storage access.** Where the *point* of a lesson is the storage layer itself — the shape of
a SQL join, a schema grant, a migration — the code drops to literal SQL:

```
db.query_one("SELECT * FROM orders WHERE id = ?", id)
db.execute("UPDATE orders SET total_minor = ? WHERE id = ? AND version = ?", ...)
db.batch_insert("order_lines", rows)
db.set_statement_timeout(remaining(ctx))
```

This is an escape hatch, not a primitive. It appears in
[06-04](/modules/domain-driven-design/04-repositories-factories-and-the-application-layer),
[07-04](/modules/modular-monolith/04-data-and-transactions-in-a-modular-monolith) and
[02-01](/modules/resilience/01-timeouts-and-deadlines), where hiding the SQL would
hide the lesson.

---

## Mapping to real technology

The pseudo-code deliberately hides vendors. When you go to build the thing, this is what
each primitive usually becomes.

| DSPL | Typically implemented by |
|---|---|
| `Store<K,V>` | PostgreSQL, MySQL, DynamoDB, MongoDB, Cassandra |
| `Log<T>` | Kafka topic, AWS Kinesis, Pulsar, a WAL, an `events` table |
| `Queue<T>` | RabbitMQ, AWS SQS, Azure Service Bus, Redis Streams, Celery |
| `Topic<T>` | Kafka, Google Pub/Sub, NATS, AWS SNS+SQS fan-out |
| `Channel<T>` | Go channel, Java `BlockingQueue`, Python `asyncio.Queue` |
| `Client<S>` | gRPC stub, HTTP client, Feign, a service-mesh sidecar |
| `Cache<K,V>` | Redis, Memcached, Caffeine, an in-process LRU |
| `Lock` / `Election` | ZooKeeper, etcd, Consul, Redis Redlock, a DB advisory lock |
| `CircuitBreaker` etc. | Resilience4j, Polly, Hystrix (retired), Envoy, Istio |
| `span` / `metrics` | OpenTelemetry, Prometheus, Jaeger, Datadog |

None of these choices change the pattern. All of them change the failure modes — which is
why each lesson has a *Challenges and failure modes* section.

---

**See also:** [Language spec](/spec/PSEUDOCODE-SPEC) · [Running example](/domain/RUNNING-EXAMPLE) · [Curriculum](/CURRICULUM)
