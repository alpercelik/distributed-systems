---
title: "Observability"
sidebar:
  order: 1
---

> Monitoring answers questions you thought of in advance. Observability answers the ones you
> did not — which, in a system nobody can hold in their head, is most of them.

| | |
|---|---|
| **Module** | [11 — Operations and evolution](/modules/operations-and-evolution/README) |
| **Prerequisites** | [00-04 Percentiles](/modules/foundations/04-latency-throughput-and-back-of-envelope), [Module 02](/modules/resilience/README) |
| **Also known as** | telemetry, the three pillars, RED/USE, SLOs |
| **Category** | Operations |

---

## 1. The problem

A customer reports that checkout took 30 seconds at 14:32. The request touched the gateway,
Order, Inventory, Payment, the payment provider, and three event consumers.

- Nine services, nine log files, nine different log formats, no shared identifier.
- Every service dashboard is green — each one's *average* latency is fine.
- The 30-second request is one in ten thousand, so it is invisible in every aggregate.
- Logs are sampled at 1%, and this request was not sampled.

Four hours later an engineer gives up. The ticket is closed as "unable to reproduce", and it
happens again next Tuesday.

## 2. In plain language

The difference between a car's dashboard and a mechanic's diagnostic port.

The dashboard shows what the designers anticipated: speed, fuel, temperature, a warning light.
Excellent for the expected. Useless when the car makes an odd noise on left turns above 50 km/h
in the rain — nobody built a light for that.

The diagnostic port lets a mechanic ask questions nobody anticipated: what was every sensor
doing in the two seconds before the noise? That is observability — not more dashboards, but
enough raw detail retained to reconstruct any specific event afterwards.

The requirement that makes this work is unglamorous: **every reading must be labelled with the
same trip identifier**, or you cannot correlate the engine data with the wheel data with the
GPS data. That identifier is the whole game.

**Where the analogy breaks down:** a car has one trip at a time. Your system has 12,000 per
second, and storing full detail for all of them is unaffordable — which is why sampling
strategy matters.

## 3. How it works

### The three signals

| Signal | Answers | Cost | Cardinality |
|---|---|---|---|
| **Metrics** | "Is something wrong?" — aggregates over time | Low | Must stay low |
| **Logs** | "What happened in this specific case?" | High | Unlimited |
| **Traces** | "Where did the time go, across services?" | Medium | Unlimited |

They are not three separate systems; they are three views that must be **linked by
`trace_id`**. A metric anomaly should lead to an exemplar trace, which should lead to the logs
for that trace. Without those links you have three data silos and four hours of manual
correlation.

### Distributed tracing

A trace is a tree of spans. Context — `trace_id`, `span_id`, sampling decision — propagates
through every call, synchronous and asynchronous alike.

```mermaid
gantt
  dateFormat SSS
  axisFormat %Lms
  section Trace
  gateway POST /orders        :0, 900
  order.place_order           :20, 870
  inventory.reserve           :40, 90
  payment.charge              :140, 760
  psp.capture (external)      :crit, 160, 740
  outbox.append               :770, 790
```

The bar that matters is the external call. A trace makes that obvious in one glance, which is
the entire value proposition.

**The most commonly broken part is asynchronous propagation.** A trace that stops at
`queue.send` and resumes as an unrelated trace in the consumer has lost exactly the half you
needed.

### What to measure

**RED, for request-driven services:** **R**ate, **E**rrors, **D**uration (as percentiles).
**USE, for resources:** **U**tilisation, **S**aturation, **E**rrors.

Then the golden signals specific to *this* course, which generic instrumentation will not give
you:

```
circuit breaker state and transitions        02-03
bulkhead utilisation and rejections          02-04
retry rate and retry-budget exhaustion       02-02
load shed rate, by priority                  02-06
degraded-mode rate, by feature               02-07
cache hit rate and eviction rate             03-03
replication lag                              03-05
outbox lag (age of oldest unpublished)       04-03
consumer lag, per group                      05-02
DLQ depth and age of oldest                  05-06
saga stuck count and age                     04-02
pool acquire-wait time                       10-03
hedge rate                                   10-04
```

**Every one of these is invisible in RED metrics and each is a silent failure mode.** A system
with perfect RED dashboards can have a four-hour outbox lag and report 100% success.

### Cardinality

Metrics cost is driven by unique label combinations. Adding `customer_id` to a metric with 8M
customers creates 8M time series and will take down your metrics backend before it helps
anyone.

**Rule: high cardinality belongs in traces and logs, never in metrics.** Wide structured
events — one event per request with many fields — are the modern answer, giving log-like
cardinality with trace-like structure.

### SLOs and error budgets

An SLI is a measurement. An SLO is a target. The **error budget** is `1 - SLO`, and it is the
useful part: at 99.9%, you may be unavailable for 43 minutes a month.

The budget converts arguments into arithmetic. Budget remaining → ship features. Budget
exhausted → stop shipping and fix reliability. Alerting on **burn rate** rather than on
absolute thresholds is what produces alerts that are worth waking someone for.

## 4. Pseudo-code

**Before — logs nobody can correlate.**

```
handler place_order(cmd) -> Result<Order, OrderError>:
  log.info("placing order")                     # which order? which customer? which request?
  r = await inventory.reserve(cmd.lines)
  log.info("reserved")                          # no timing, no trace, no ids
  ...
  # Nine services × this = four hours of grep and guesswork.
```

**The pattern — context that propagates, and events that are wide.**

```
record TraceContext:
  trace_id: String            # the whole request, end to end
  span_id: String             # this operation
  parent_span_id: Option<String>
  sampled: Bool
  baggage: Map<String, String>    # e.g. customer_tier, for filtering later

service OrderService:
  @timeout(2s)
  handler place_order(ctx: RequestContext, cmd: PlaceOrder) -> Result<Order, OrderError>:
    with span("order.place_order",
              attributes: {order_id: cmd.order_id, customer_id: cmd.customer_id,
                           line_count: cmd.lines.size, total_cents: cmd.total.amount}):

      # Context flows into the call. Without this, the trace stops here.
      reservation = await inventory.reserve(ctx, cmd.lines) timeout 300ms

      with span("order.charge", attributes: {amount_cents: cmd.total.amount}):
        receipt = await payments.charge(ctx, cmd) timeout 800ms

      # ONE wide event per request, with every field that might matter later.
      # This is what makes unanticipated questions answerable.
      log.event("order_placed", {
        trace_id: ctx.trace_id,
        order_id: order.id, customer_id: cmd.customer_id, customer_tier: ctx.tier,
        total_cents: order.total.amount, line_count: cmd.lines.size,
        duration_ms: elapsed, inventory_ms: inv_elapsed, payment_ms: pay_elapsed,
        breaker_state: pay_breaker.state, bulkhead_utilisation: pool.utilisation(),
        degraded: degraded_features, retries: retry_count,
        instance: INSTANCE_ID, version: BUILD_VERSION, region: MY_REGION,
      })
      # WHY one wide event rather than eight log lines: you can query it. "p99
      # duration for GOLD customers on version 2.3 in eu-west-1 where the breaker
      # was HALF_OPEN" is a filter, not a research project.

      return Ok(order)
```

**Propagating through the asynchronous boundary — the half that is usually lost.**

```
service OrderService:
  fn publish(ctx: RequestContext, e: OrderEvent):
    bus.publish(e, headers: {
      traceparent: ctx.to_w3c_header(),     # standard propagation format
      correlation_id: ctx.correlation_id,
    })

service ShippingService:
  on event OrderPlaced(e, meta):
    # Continue the SAME trace, as a linked span rather than a child: the producer's
    # span has already ended, so a parent-child relationship would be a lie.
    ctx = TraceContext.from_w3c(meta.headers.traceparent)
    with span("shipping.on_order_placed", links: [ctx.span_id], attributes: {...}):
      handle(e)
    # TRAP without this: the trace ends at the queue. Every async effect becomes
    # an orphan, and "why did this order not ship?" is unanswerable.
```

**The metrics that generic instrumentation will not give you.**

```
service ResilienceMetrics:
  every 10s:
    # Each of these is a SILENT failure mode: no errors, no latency change,
    # nothing in RED, and the system is quietly broken.
    metrics.gauge("breaker.state", pay_breaker.state, tags: {dep: "payments"})
    metrics.gauge("bulkhead.utilisation", pool.utilisation(), tags: {pool: "payments"})
    oldest_outbox = outbox.oldest_unpublished()
    metrics.gauge("outbox.lag_s", oldest_outbox is None ? 0 : now() - oldest_outbox.created_at)
    metrics.gauge("consumer.lag", consumer.lag(), tags: {group: "shipping"})
    oldest_dlq = dlq.oldest()
    metrics.gauge("dlq.oldest_age_s", oldest_dlq is None ? 0 : now() - oldest_dlq.failed_at)
    metrics.gauge("saga.stuck_count", sagas.count(status: STUCK))
    metrics.gauge("replication.lag_ms", replica.lag())
    metrics.gauge("pool.acquire_wait_p99", pool.acquire_wait_p99())
```

**SLOs and burn-rate alerting.**

```
slo checkout_availability:
  sli: "successful checkouts / total checkout attempts"
  objective: 0.999                            # 43 min/month of budget
  window: 30d

service BurnRateAlerting:
  every 1m:
    # Multi-window, multi-burn-rate: catches both a sudden outage and a slow leak,
    # without paging for a two-minute blip.
    fast = error_rate(window: 1h) / (1 - slo.objective)
    slow = error_rate(window: 6h) / (1 - slo.objective)

    if fast > 14.4 and slow > 6:
      page("burning budget fast — 2% of the monthly budget in 1 hour")
    elif error_rate(window: 6h) / (1-slo.objective) > 6 and
         error_rate(window: 3d) / (1-slo.objective) > 1:
      ticket("slow burn — will exhaust the budget before month end")

    metrics.gauge("slo.budget_remaining", budget_remaining())
    # WHY burn rate and not a threshold: "error rate > 1%" pages at 3am for a
    # blip that consumed 0.1% of the budget, and stays silent through a
    # three-day 0.5% degradation that consumes all of it.
```

## 5. Knobs and variants

| Knob | Guidance | Failure if wrong |
|---|---|---|
| Trace sampling | Head-based 1–10%, plus tail-based for errors and slow requests | Uniform low sampling misses exactly the interesting requests |
| Metric cardinality | No unbounded labels, ever | `customer_id` as a label kills the metrics backend |
| Log level in production | INFO plus structured events; DEBUG on demand | DEBUG everywhere is unaffordable and unsearchable |
| Retention | Traces 7–30d, metrics 13mo, logs 30d | Short metric retention prevents year-on-year comparison |
| Alerting | Burn rate, multi-window | Threshold alerts produce noise and miss slow burns |
| Event shape | One wide event per request | Many narrow log lines cannot be queried together |
| Async propagation | Always, via standard headers | Broken traces at every queue boundary |

## 6. Challenges and failure modes

- **Broken trace propagation.** The most common gap. A single service that drops the header
  orphans everything downstream. Test propagation explicitly, including across queues.
- **Cardinality explosions.** One unbounded label takes down the metrics system, usually during
  an incident when someone adds a label to debug.
- **Alert fatigue.** Hundreds of threshold alerts, most ignored. Symptom-based, burn-rate
  alerting on a small number of SLOs is strictly better than component alerts on everything.
- **Averages on dashboards.** A 40ms mean hides 1% of users waiting 4 seconds. Percentiles, and
  never aggregate percentiles across instances by averaging them.
- **Sampling away the interesting requests.** Uniform 1% head sampling loses the slow ones. Use
  tail-based sampling: decide *after* the request completes, keeping all errors and all slow
  requests.
- **Observability costs more than the system.** Telemetry bills of 20–30% of infrastructure
  spend are common. Sample aggressively, drop low-value metrics, and treat the bill as a design
  input.
- **Missing the pattern-specific signals.** Perfect RED dashboards and a four-hour outbox lag.
  The list in §3 is not optional.
- **Observability that only exists in production.** Engineers cannot debug in staging, so they
  test in production by accident.
- **No exemplars.** A metric spike with no link to a trace means starting the investigation from
  scratch.

## 7. Alternatives

- **Classic monitoring** (metrics + threshold alerts). Adequate for simple systems; inadequate
  the moment a request crosses more than two services.
- **Logging only.** Extremely flexible and expensive at scale, and correlation is manual unless
  you have `trace_id` — at which point you have half of tracing anyway.
- **APM products.** Auto-instrumentation, fast to adopt, vendor lock-in and per-host pricing.
- **eBPF-based observability.** Zero code changes, network-level visibility, and no application
  semantics — it cannot tell you `customer_tier`.
- **Profiling in production.** Continuous profilers answer "where did the CPU go?" better than
  any trace. Complementary, not alternative.

## 8. Trade-offs

| Advantage | Disadvantage |
|---|---|
| Unanticipated questions become answerable | Telemetry can cost 20–30% of infrastructure spend |
| One trace replaces four hours of correlation | Instrumentation is work in every service, forever |
| SLOs turn reliability arguments into arithmetic | SLOs require agreement the organisation may not want to give |
| Burn-rate alerting drastically reduces noise | Requires a working SLI first |
| Wide events make production queryable | High-cardinality storage is expensive |

## 9. Complexity introduced

- **Operational.** A telemetry pipeline and storage to run and pay for; sampling configuration;
  dashboards and alert rules to maintain; cardinality policing.
- **Cognitive.** Engineers must instrument deliberately and understand sampling, cardinality
  and percentile aggregation.
- **Failure surface.** The observability system itself can fail — usually during an incident,
  because that is when load spikes. Ensure it degrades independently of the system it watches.
- **Testing.** Trace propagation, including across async boundaries, should be asserted in
  integration tests. Almost nobody does this, and it breaks constantly.

## 10. Related concepts

- **Builds on:** [00-04 Percentiles](/modules/foundations/04-latency-throughput-and-back-of-envelope)
- **Composes with:** every pattern in the course — each has signals that only observability makes visible; [09-04 Chaos engineering](/modules/availability-and-dr/04-chaos-engineering) (a hard prerequisite)
- **Conflicts with / tension:** cost, and the performance overhead of instrumentation
- **Contrast with:** monitoring — known questions versus unknown ones
- **Leads to:** [11-02 Deployment strategies](/modules/operations-and-evolution/02-deployment-strategies)

## 11. Exercises

1. **Trace it.** A checkout takes 30 seconds. Using only the wide event above, write the query
   that finds it and the three fields that would identify the cause. Now do it without tracing.
2. **Extend it.** ShopFlow adds a `customer_id` label to `orders.placed` to debug one customer.
   Compute the resulting time series count for 8M customers, and give a correct way to answer
   the same question.
3. **Break it.** All nine services have RED dashboards and they are all green. The outbox
   publisher has been stopped for four hours. Explain why nothing alerts, and write the one
   metric and one alert that would have caught it in 30 seconds.

## 12. References

- Google SRE Book — Ch. 4 (SLOs), Ch. 6 (monitoring); *The Site Reliability Workbook* Ch. 5 on burn-rate alerting.
- Charity Majors, Liz Fong-Jones, George Miranda, *Observability Engineering* (O'Reilly, 2022).
- OpenTelemetry documentation — the vendor-neutral standard for traces, metrics and logs.
- Tom Wilkie, "The RED Method"; Brendan Gregg, "The USE Method".
- Cindy Sridharan, *Distributed Systems Observability*.

---

**Up:** [Module 11](/modules/operations-and-evolution/README) · **Previous:** [← Module 10](/modules/performance-and-concurrency/README) · **Next:** [11-02 Deployment strategies →](/modules/operations-and-evolution/02-deployment-strategies)
