# KPI catalog

Every KPI must ship with its numerator, denominator, time window, environment,
classification, owner, and source evidence. Targets are policies, not achieved
results.

## Reliability

| KPI | Formula |
|---|---|
| Availability | successful service minutes / scheduled service minutes |
| SLO attainment | compliant SLI windows / total SLI windows |
| Error-budget consumption | consumed error budget / allocated error budget |
| MTTD | detection timestamp - incident start |
| MTTA | acknowledgement timestamp - alert timestamp |
| MTTR | recovery timestamp - incident start |
| Change failure rate | failed production changes / production changes |
| Rollback success rate | successful rollbacks / rollback attempts |

## Elasticsearch-to-VictoriaLogs migration assurance

| KPI | Formula |
|---|---|
| Ingestion parity | target events received / source events received |
| Dropped-event rate | missing or rejected target events / source events |
| Required-field preservation | fields preserved / required fields tested |
| Query equivalence | materially equivalent results / approved queries tested |
| Material detection parity | reproduced material detections / material detections tested |
| Evidence continuity | uninterrupted evidence streams / required evidence streams |
| Compression efficiency | uncompressed bytes / stored bytes |

## Governed AI SRE

| KPI | Formula |
|---|---|
| Recommendation acceptance | approved recommendations / reviewed recommendations |
| Autonomous resolution | eligible incidents resolved autonomously / eligible incidents |
| Unsafe-action prevention | prevented unauthorized actions / unauthorized attempts |
| Approval bypass | gated actions executed without approval / gated attempts |
| Evidence-grounded recommendations | recommendations with current evidence / recommendations |
| Agent-induced incident rate | incidents caused by agent actions / governed actions |
| Successful reversal | successfully reversed actions / reversal attempts |

Autonomous resolution must never be reported without unsafe-action prevention,
approval bypass, agent-induced incidents, and successful reversal.

## GRC evidence

| KPI | Formula |
|---|---|
| Evidence freshness attainment | current evidence / required evidence |
| Evidence-lineage completeness | evidence with complete provenance / evidence collected |
| Control automation coverage | automated controls / automation-eligible controls |
| Operating-effectiveness pass rate | passing tests / control tests executed |
| Evidence acceptance | accepted evidence / reviewed evidence |
| Stale-evidence exposure hours | sum of hours required evidence remained expired |
