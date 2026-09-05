"""CLI for the Kubernetes AI SRE Platform."""

import argparse
import json
from pathlib import Path

from .engine import evaluate_scenario


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="kube-ai-sre",
        description="Evaluate AWS EKS reliability, AI SRE safety, compliance evidence, and VictoriaLogs migration economics.",
    )
    parser.add_argument("scenario")
    parser.add_argument("--output", default="kubernetes-ai-sre-report.json")
    args = parser.parse_args(argv)
    data = json.loads(Path(args.scenario).read_text(encoding="utf-8"))
    report = evaluate_scenario(data)
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": report["classification"],
        "decision_gates": report["decision_gates"],
        "reliability_kpis": report["reliability_kpis"],
        "migration_kpis": report["migration_kpis"],
        "unit_economics": report["unit_economics"],
        "output": args.output,
        "evidence_sha256": report["evidence_sha256"],
    }, indent=2))
    return 0 if all(report["decision_gates"].values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
