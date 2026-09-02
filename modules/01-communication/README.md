---
title: "Communication"
---

> The choice made here — synchronous or asynchronous — constrains every choice in the eight
> modules that follow. It is the single highest-leverage decision in the system.

## What you will be able to do

- Choose between a request/response call and a message, with a reason you can defend.
- State the delivery guarantee of every path in your system, and make at-least-once safe.
- Change a message schema without breaking a consumer that hasn't been redeployed.
- Explain why the client, not the server, generates the idempotency key.
- Find a service instance in a topology that changes every few minutes.

## Lessons

| # | Lesson | The decision it settles |
|---|---|---|
| 01-01 | [Synchronous request/response](/modules/communication/01-synchronous-request-response) | When you genuinely need an answer now |
| 01-02 | [Asynchronous messaging](/modules/communication/02-asynchronous-messaging) | When you don't, and what that buys |
| 01-03 | [Delivery guarantees and idempotency](/modules/communication/03-delivery-guarantees-and-idempotency) | How many times will this actually run |
| 01-04 | [Serialization and schema evolution](/modules/communication/04-serialization-and-schema-evolution) | How to change a contract without an outage |
| 01-05 | [Service discovery](/modules/communication/05-service-discovery) | Where is the thing I'm calling |

## The one idea

**Synchronous coupling is temporal coupling.** If A calls B synchronously, A cannot be more
available than B, cannot be faster than B, and cannot be deployed independently of B's
contract. Every one of those three is recoverable — with the patterns in
[Module 02](/modules/resilience/README) — but the default is coupling, and the default is
what you get if you don't decide.

Asynchronous messaging removes temporal coupling and hands you, in exchange, duplicates,
reordering, and eventual consistency. There is no third option that has neither problem.

## ShopFlow at the end of this module

Split into services. Checkout calls Inventory and Payment synchronously because it needs
answers before responding to the customer. Shipping, Notification and Analytics consume
events, because they don't. Every message has a schema in a registry, every command carries
an idempotency key, and instances find each other through a registry rather than a config
file.

It is now considerably less reliable than the monolith was. That is
[Module 02](/modules/resilience/README)'s job.

---

**Up:** [Curriculum](/CURRICULUM) · **Previous:** [← Module 00](/modules/foundations/README) · **Next:** [01-01 Synchronous request/response →](/modules/communication/01-synchronous-request-response)
