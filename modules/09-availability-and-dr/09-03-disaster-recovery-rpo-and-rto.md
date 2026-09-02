---
title: "Disaster recovery: RPO and RTO"
sidebar:
  order: 3
---

> Replication protects against a machine dying. Nothing but backups protects against a
> `DELETE FROM orders` — which replicates faithfully to every replica in milliseconds.

| | |
|---|---|
| **Module** | [09 — Availability and DR](/modules/availability-and-dr/README) |
| **Prerequisites** | [09-01 Failover](/modules/availability-and-dr/01-redundancy-and-failover), [03-05 Replication](/modules/scalability/05-replication) |
| **Also known as** | business continuity, backup and restore, point-in-time recovery |
| **Category** | Availability |

---

## 1. The problem

ShopFlow has three replicas across three availability zones. Availability is excellent.

Then a migration script runs against production instead of staging. `orders` loses 12 million
rows. All three replicas apply the deletion in under a second.

The team discovers:

- Nightly backups exist and have been running for two years. Nobody has ever restored one.
- Restoring the 400GB backup takes 6 hours, and nobody knew that.
- The most recent backup is 19 hours old, so 19 hours of orders are gone.
- The backup for the payments database was silently failing since a credentials rotation in
  March. There is no alert on backup *success*, only on backup job *errors* — and it was
  exiting zero.

The system was highly available and completely unrecoverable. **Replication is not backup.**

## 2. In plain language

Insurance you have never claimed on.

Two numbers define the policy. **How much can you lose?** If your house burns down, do you
need every photograph, or is last month's copy acceptable? **How long can you be without it?**
A week in a hotel, or must you be back tomorrow?

Both cost money, and both cost more the tighter you make them. Losing nothing at all means
copying every photograph the instant it is taken; being back tomorrow means keeping a fully
furnished second house.

And the thing that ruins people: they pay for the policy for twenty years, and when the fire
comes they discover the copies were being made to a drawer inside the same house.

**Where the analogy breaks down:** you would notice a missing second house. A backup that has
silently been writing zero bytes for eight months looks exactly like one that works.

## 3. How it works

### The two numbers

```mermaid
graph LR
  A[Last good backup] -->|RPO: data you lose| B[Disaster]
  B -->|RTO: time you are down| C[Service restored]
  style B fill:#fce8e6,stroke:#d93025
```

- **RPO — Recovery Point Objective.** How much data you can afford to lose, in time. An RPO of
  15 minutes means backups or log shipping at least every 15 minutes.
- **RTO — Recovery Time Objective.** How long recovery may take. An RTO of 1 hour means the
  entire detect-decide-restore-verify-cutover sequence fits in an hour.

**These are business decisions with engineering prices**, and they should be agreed per
dataset, written down, and tested. Different data deserves different numbers:

| ShopFlow data | RPO | RTO | Why |
|---|---|---|---|
| Payments ledger | 0 | 15 min | Money. Losing a transaction is not recoverable commercially |
| Orders | 5 min | 1 hour | A lost order is a lost customer, but reconstructable from payments |
| Customer accounts | 1 hour | 4 hours | Slow-changing |
| Product catalogue | 24 hours | 4 hours | Re-importable from the ERP |
| Analytics | 24 hours | 72 hours | Reconstructable from event logs |
| Sessions, caches | ∞ | 0 | Regenerated. Do not back up |

Applying the strictest numbers to everything is how DR becomes unaffordable and therefore
untested.

**RPO 0 is not a backup cadence.** It means acknowledging a payment only after its durable
replica has also acknowledged it — typically synchronous replication or a transactional ledger
protocol. PITR and log shipping can make the RPO very small, not zero; this guarantee costs
latency and availability during a replica failure.

### The disasters, and what actually protects against each

| Disaster | Replication helps? | Backups help? |
|---|---|---|
| Machine failure | ✅ | Not needed |
| Zone failure | ✅ | Not needed |
| Region failure | ✅ (cross-region) | Yes, if backups are cross-region |
| **Accidental deletion** | ❌ **Replicated instantly** | ✅ Point-in-time restore |
| **Application bug corrupting data** | ❌ Replicated instantly | ✅ |
| **Ransomware** | ❌ Encrypts replicas too | ✅ **Only if immutable and offline** |
| **Malicious insider** | ❌ | ✅ Only if they cannot delete backups |

The four rows where replication fails are precisely the ones people forget when they say "we
have three replicas, we're covered."

### The 3-2-1 rule and immutability

**3** copies, on **2** different media/systems, with **1** off-site. Modernised for cloud:
production, a backup in a different region, and one in a different *account* with
**write-once** retention that even an administrator cannot delete.

That last part is the ransomware and insider defence. If the credentials that can write your
data can also delete your backups, you do not have backups.

### Backup types

| Type | RPO | Restore speed | Storage |
|---|---|---|---|
| Full | Since last full | Slowest | Highest |
| Incremental | Since last incremental | Slow (chain of restores) | Lowest |
| Differential | Since last differential | Medium | Medium |
| **Continuous / log shipping (PITR)** | **Seconds** | Medium | Medium |
| Snapshot (block-level) | Snapshot interval | Fast | Medium |

**Point-in-time recovery** — a full backup plus a continuous stream of transaction logs — is
what makes "restore to 14:22:31, just before the bad migration" possible. It is the single most
valuable capability in this lesson.

## 4. Pseudo-code

**Before — backups that exist and do not work.**

```
service BackupJob:
  every 1d at 02:00:
    dump = database.dump()
    s3.put("backups/" + today() + ".sql", dump)
    # TRAP 1: RPO is 24 hours. Nobody agreed to that.
    # TRAP 2: no verification. A zero-byte file counts as success.
    # TRAP 3: same account, same credentials — ransomware deletes it too.
    # TRAP 4: never restored. Restore time is unknown.
    # TRAP 5: alerts on job failure, not on backup ABSENCE. A job that stops
    #         being scheduled at all is completely silent.
```

**The pattern — backups with verification, immutability and known restore times.**

```
record BackupPolicy:
  dataset: String
  rpo: Duration
  rto: Duration
  full_backup_interval: Duration
  continuous_log_shipping: Bool
  retention: Duration
  immutable_copy: Bool
  destinations: List<Destination>       # different region AND different account

service BackupService:
  uses policies: Store<String, BackupPolicy>
  uses backup_catalog: Store<UUID, BackupRecord>

  every 1h:
    for p in policies.values():
      if now() - last_full(p.dataset) >= p.full_backup_interval:
        spawn take_full_backup(p)

  async fn take_full_backup(p: BackupPolicy):
    started = now()
    snapshot = await database.snapshot(p.dataset)        # consistent point in time

    record = BackupRecord(id: uuid(), dataset: p.dataset, at: started,
                          size: snapshot.size, checksum: sha256(snapshot))

    for d in p.destinations:
      await d.put(snapshot, record.id,
                  retention: p.retention,
                  immutable: p.immutable_copy)
      # WHY immutable: object-lock / write-once storage. An attacker (or a
      # mistaken engineer) holding production credentials still cannot delete it.

    # Verification is part of the backup, not a separate optional activity.
    if not await verify(record):
      alert("BACKUP VERIFICATION FAILED", dataset: p.dataset)
      return
    backup_catalog.put(record.id, record with { verified: true })

  async fn verify(r: BackupRecord) -> Bool:
    # 1. It exists and is the right size and checksum.
    for d in destinations_of(r):
      stored = await d.stat(r.id)
      if stored.size != r.size or stored.checksum != r.checksum: return false
    # 2. It is structurally restorable — restore into a scratch environment.
    scratch = await provision_scratch_db()
    if not await restore_into(scratch, r): return false
    # 3. It contains what it should. A restore of an empty database succeeds.
    if scratch.row_count("orders") < expected_row_count(r.at) * 0.95: return false
    await scratch.destroy()
    return true

  # The alert that matters most, and that almost nobody has.
  every 15m:
    for p in policies.values():
      age = now() - last_verified_backup(p.dataset)
      metrics.gauge("backup.age_s", age, tags: {dataset: p.dataset})
      if age > p.rpo * 2:
        page("RPO AT RISK", dataset: p.dataset, age: age, rpo: p.rpo)
      # WHY page and not warn: this is the only signal that distinguishes
      # "backups are fine" from "backups silently stopped eight months ago".
```

**Point-in-time recovery — restoring to just before the mistake.**

```
service PointInTimeRestore:
  async fn restore_to(dataset: String, target: Instant) -> Result<Restore, Error>:
    base = backup_catalog.latest_verified_before(dataset, target)
    if base is None: return Err(NoSuitableBackup)

    logs = log_archive.range(dataset, from: base.at, to: target)

    # Restore into a NEW instance. Never over the top of production: if the
    # restore is wrong you have then destroyed the evidence as well as the data.
    target_db = await provision(size_of(base))
    await restore_full(target_db, base)
    await replay_logs(target_db, logs)              # to the exact instant

    return Ok(Restore(instance: target_db, point: target,
                      data_loss: now() - target))   # everything since `target`
                                                    # is intentionally discarded

  # The realistic recovery flow for the incident in §1:
  #   1. STOP writes immediately — every second makes reconstruction harder
  #   2. Restore to 14:22:31 (just before the migration) into a new instance
  #   3. Diff: which rows exist in the restore and not in production?
  #   4. Copy back ONLY the deleted rows, preserving legitimate writes since
  #   5. Resume writes
  #
  # Step 3–4 is why a full "restore over production" is usually wrong: it would
  # also discard the two hours of legitimate orders taken after the deletion.
```

**The DR drill — the only thing that makes any of this real.**

```
service DisasterRecoveryDrill:
  every 1 quarter:
    for p in policies.values():
      started = now()

      # A genuine restore, into an isolated environment, from the real backup.
      r = await PointInTimeRestore.restore_to(p.dataset, now() - 1h)
      restore_duration = now() - started

      checks = [
        row_counts_plausible(r), referential_integrity(r),
        recent_records_present(r), application_can_start_against(r),
      ]

      metrics.gauge("dr.actual_rto_s", restore_duration, tags: {dataset: p.dataset})

      if restore_duration > p.rto:
        # This is the finding that matters. Everyone assumes their RTO; almost
        # nobody has measured it, and the measurement is usually 3–10× the guess.
        alert("RTO NOT MET IN DRILL", dataset: p.dataset,
              actual: restore_duration, target: p.rto)

      record_drill_result(p.dataset, restore_duration, checks, evidence: r.report)
      await r.instance.destroy()
```

## 5. Knobs and variants

| Knob | Guidance | Failure if wrong |
|---|---|---|
| RPO / RTO | Per dataset, agreed with the business | One strict number for everything makes DR unaffordable |
| Backup frequency | ≤ RPO | Longer intervals silently violate the agreed RPO |
| PITR | Enable for anything with an RPO under a day | Without it, you restore to a whole-day boundary |
| Retention | 30–90 days operational, longer if regulated | Short retention misses slow-burn corruption |
| Immutability | Object-lock on at least one copy | Without it, backups are as deletable as production |
| Isolation | Different region **and** different account | Same-account backups share a blast radius |
| Verification | Automated restore, every backup | Unverified backups fail ~when you need them |
| Drills | Quarterly minimum, measured | An unmeasured RTO is a guess |
| Alerting | On backup **age**, not job errors | A job that stops running produces no errors |

## 6. Challenges and failure modes

- **Backups that were never restored.** The defining failure. Verification must be automatic
  and part of the backup, not an annual intention.
- **Alerting on the wrong thing.** Job-failure alerts miss the case where the job stopped being
  scheduled, or exits zero having written nothing. Alert on the *age of the last verified
  backup*.
- **Restore time discovered during the incident.** Restoring 400GB over a network at 50MB/s is
  over two hours before any application starts. Measure it.
- **Backups in the same blast radius.** Same account, same credentials, same region.
  Ransomware, a compromised key or a mistaken `terraform destroy` takes both.
- **Silent corruption.** A bug corrupts data slowly over weeks. By detection, every retained
  backup contains the corruption. Longer retention and integrity checks are the only defence.
- **Application state outside the database.** Object storage, secrets, configuration, message
  queues, search indices. A perfect database restore into a system missing its uploaded images
  is not a recovery.
- **Restoring over production.** Destroys both the corrupted state and any legitimate writes
  since. Restore beside, diff, then repair.
- **Encrypted backups with lost keys.** The key management system was in the region you lost.
- **Cross-service consistency.** Nine databases restored to nine slightly different points in
  time produce orders without payments. Coordinate restore points, or design reconciliation.

## 7. Alternatives

- **Cross-region replication + PITR.** The modern default: replication for availability,
  point-in-time recovery for the four disasters replication cannot handle.
- **Event sourcing** ([04-05](/modules/data-and-consistency/05-event-sourcing)). The event
  log *is* a continuous backup, and state can be rebuilt to any point. Still needs the log
  itself backed up.
- **Managed database backups.** Cloud providers handle mechanics and PITR. **You still own
  verification and drills** — the provider guarantees the backup exists, not that it contains
  what you need.
- **Soft deletes and immutable data models.** Never actually deleting removes the most common
  disaster entirely. Costs storage and complicates GDPR.
- **Accept the loss.** For genuinely reconstructable data — caches, derived indices, analytics
  aggregates — no backup is correct. Write down that this was a decision.

## 8. Trade-offs

| Advantage | Disadvantage |
|---|---|
| Protects against the failures replication cannot | Storage and transfer cost, growing with retention |
| PITR allows recovery to just before the mistake | Restore is slow, and slower than everyone estimates |
| Immutable copies defeat ransomware and insiders | Immutability means you cannot delete data on request either |
| Drills convert assumptions into measurements | Drills cost real engineering time every quarter |
| Per-dataset RPO/RTO makes DR affordable | Requires per-dataset agreement and documentation |

## 9. Complexity introduced

- **Operational.** Backup infrastructure across accounts and regions; verification pipelines;
  quarterly drills with recorded evidence; restore runbooks; key management that survives the
  disaster.
- **Cognitive.** Engineers must know which data is backed up, to what RPO, and what "restore"
  actually entails for their service.
- **Failure surface.** Silent backup failure, unrestorable backups, lost keys, incomplete state
  coverage, cross-service restore inconsistency.
- **Testing.** The drill *is* the test, and it must be measured rather than performed
  ceremonially.

## 10. Related concepts

- **Builds on:** [09-01 Failover](/modules/availability-and-dr/01-redundancy-and-failover), [03-05 Replication](/modules/scalability/05-replication)
- **Composes with:** [09-02 Multi-region](/modules/availability-and-dr/02-multi-region-architecture), [09-04 Chaos engineering](/modules/availability-and-dr/04-chaos-engineering), [04-05 Event sourcing](/modules/data-and-consistency/05-event-sourcing)
- **Conflicts with / tension:** GDPR erasure — immutable backups cannot selectively delete
- **Contrast with:** [09-01 Failover](/modules/availability-and-dr/01-redundancy-and-failover) — failover restores *service*, DR restores *data*. Both are needed and they protect against different things
- **Leads to:** [09-04 Chaos engineering](/modules/availability-and-dr/04-chaos-engineering)

## 11. Exercises

1. **Trace it.** A migration deletes 12M rows at 14:23. It is noticed at 15:40. Backups are
   nightly at 02:00 with no PITR. Write the recovery plan and compute the data loss. Now add
   PITR and rewrite it.
2. **Extend it.** Set RPO and RTO for every ShopFlow dataset in
   [the running example](/domain/RUNNING-EXAMPLE) and justify each. Which is strictest,
   and what does it cost?
3. **Break it.** Backups run nightly to S3 in the same account, and there is an alert on the
   backup job's exit code. Describe a failure mode where backups have been useless for eight
   months and every alert stayed green.

## 12. References

- Google SRE Book — Ch. 26, "Data Integrity: What You Read Is What You Wrote". The best treatment available, including the GMail restore story.
- AWS Well-Architected Framework — Reliability Pillar, backup and recovery.
- ISO 22301 — business continuity, if you need the formal framing.
- Gitlab, "Postmortem of database outage of January 31 2017" — five backup mechanisms, all broken. Required reading.
- Backblaze / cloud provider documentation on object lock and immutable storage.

---

**Up:** [Module 09](/modules/availability-and-dr/README) · **Previous:** [← 09-02](/modules/availability-and-dr/02-multi-region-architecture) · **Next:** [09-04 Chaos engineering →](/modules/availability-and-dr/04-chaos-engineering)
