# Kubernetes AI SRE Platform

**Open-source AWS Kubernetes AI SRE platform for automated incident response,
continuous compliance evidence, Elasticsearch-to-VictoriaLogs migration,
OpenTelemetry observability, security automation, SLO KPIs, and cloud unit
economics.**

This project connects AWS and Amazon EKS telemetry, Kubernetes reliability,
governed AI incident investigation, compliance evidence, observability migration,
and FinOps in one decision model.

> **Maturity:** v0.1 is an offline reference implementation using a synthetic
> controlled-test scenario. It does not connect to or modify live infrastructure.

## Why this exists

SRE, security, GRC, and FinOps teams frequently measure the same infrastructure
through disconnected systems. The result is duplicated evidence work, migrations
that lack detection-parity gates, AI automation without clear authority, and cost
reports that omit reliability and compliance requirements.

Kubernetes AI SRE Platform provides a shared evidence and economics layer:

```text
AWS + EKS + Kubernetes
          |
     OpenTelemetry
          |
  Elasticsearch-compatible source ---- VictoriaLogs target
          |                                  |
          +-------- migration assurance -----+
                           |
                  evidence and KPI graph
                    /       |       \
                AI SRE     GRC     FinOps
                           |
                engineering and executive decisions
```

## Five-minute demonstration

```bash
python -m kube_ai_sre.cli \
  scenarios/deployment-auth-regression.json \
  --output kubernetes-ai-sre-report.json
```

Run the tests:

```bash
python -m unittest discover -s tests -v
```

The scenario models an EKS deployment authorization regression, an SLO burn,
dual-write observability validation, an unsafe AI action attempt, an approved
rollback, evidence refresh, and a migration business case.

## Decision gates

- At least 99.9% ingestion parity
- 100% required-field preservation
- 100% parity for tested material detections
- 100% compliance-evidence stream continuity
- Zero unauthorized AI actions executed
- Successful rollback validation
- Positive verified monthly run-rate savings

## KPI coverage

The report calculates reliability, migration, AI-agent safety, GRC evidence, and
unit-economic metrics. See:

- [KPI catalog](docs/KPI_CATALOG.md)
- [Unit economics](docs/UNIT_ECONOMICS.md)
- [Claims and limitations](docs/CLAIMS_AND_LIMITATIONS.md)

## Reference integration assets

- OpenTelemetry dual-write configuration
- Elasticsearch-compatible source exporter
- VictoriaLogs OTLP target exporter
- Safety-first Helm values with live actions disabled
- Synthetic incident and migration fixture
- CI-generated evidence report

## Search and use-case coverage

This repository addresses AWS Kubernetes monitoring, Kubernetes AI, AI for site
reliability engineering, EKS audit logs, AI incident response, continuous
compliance monitoring, Elasticsearch-to-VictoriaLogs migration, VictoriaLogs on
Kubernetes, OpenTelemetry logs, cloud observability cost optimization, security
automation, and Kubernetes FinOps.

## Roadmap

1. Live read-only AWS CloudTrail, Config, Security Hub and EKS audit collectors.
2. OpenTelemetry evidence schema and VictoriaLogs query-parity runner.
3. Kubernetes change-risk and rollback simulation.
4. Compliance-platform and OSCAL exporters.
5. Policy-gated AI investigator with approval receipts.
6. Grafana engineering and executive dashboards.
7. Signed evidence reports, SBOM, provenance and public benchmark corpus.

## License

Apache-2.0.
