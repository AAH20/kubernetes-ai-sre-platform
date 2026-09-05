# Unit economics

## Observability

```text
Monthly observability cost
= ingestion compute + storage + query compute + transfer + licensing
+ platform engineering + on-call support

Cost per ingested GB
= monthly observability cost / GB ingested

Cost per monitored service
= monthly observability cost / monitored services

Cost per valid evidence object
= evidence-platform cost / evidence accepted by control owners
```

## Migration

```text
Verified monthly run-rate savings
= equivalent baseline monthly cost - target monthly cost

Migration investment
= engineering + dual-write infrastructure + validation + training + risk reserve

Break-even months
= migration investment / verified monthly run-rate savings
```

Baseline and target must use equivalent volume, retention, availability, query,
support and evidence-continuity requirements.

## AI SRE

```text
Agent investigation cost
= inference + runtime + telemetry queries + human review + failed-action recovery

Cost per safe validated resolution
= agent investigation cost / resolutions validated without agent-induced harm

Net toil value saved
= verified hours avoided × loaded engineer rate - agent investigation cost
```

Do not count work transferred to another team as time saved.

## Decision classification

- `observed`: system-of-record measurements;
- `estimated`: disclosed model and assumptions;
- `synthetic_controlled_test`: demonstration fixture;
- `insufficient_evidence`: missing or stale decision inputs.

Expected-loss reduction belongs in a separately calibrated probabilistic risk
scenario. It must not be inferred from alert severity, log volume, or failed
controls.
