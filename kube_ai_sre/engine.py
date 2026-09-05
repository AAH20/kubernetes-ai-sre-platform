"""Synthetic, deterministic reliability and migration assurance engine."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


def _ratio(numerator: float, denominator: float) -> float | None:
    return round(numerator / denominator, 4) if denominator else None


def evaluate_scenario(data: dict[str, Any]) -> dict[str, Any]:
    classification = data.get("classification", "synthetic_controlled_test")
    if classification not in {
        "synthetic_controlled_test", "observed", "estimated", "insufficient_evidence"
    }:
        raise ValueError(f"Unsupported classification: {classification}")

    reliability = data["reliability"]
    migration = data["migration"]
    agent = data["agent"]
    grc = data["grc"]
    economics = data["economics"]

    source_events = float(migration["source_events"])
    target_events = float(migration["target_events"])
    queries_tested = float(migration["queries_tested"])
    detections_tested = float(migration["material_detections_tested"])
    actions = float(agent["governed_actions"])
    unauthorized = float(agent["unauthorized_attempts"])
    evidence_required = float(grc["evidence_required"])

    total_observability_cost = sum(float(economics[key]) for key in (
        "ingestion_compute_usd", "storage_usd", "query_compute_usd",
        "data_transfer_usd", "licensing_usd", "platform_engineering_usd",
        "on_call_support_usd",
    ))
    target_monthly_cost = float(economics["target_monthly_observability_cost_usd"])
    baseline_monthly_cost = float(economics["baseline_monthly_observability_cost_usd"])
    monthly_savings = baseline_monthly_cost - target_monthly_cost
    migration_investment = float(economics["migration_investment_usd"])
    reviewer_rate = float(economics["loaded_engineer_hourly_rate_usd"])
    hours_saved = max(0.0, float(economics["manual_hours_baseline"]) - float(economics["actual_human_hours"]))
    agent_cost = sum(float(economics[key]) for key in (
        "model_inference_cost_usd", "agent_runtime_cost_usd",
        "telemetry_query_cost_usd", "human_review_cost_usd",
        "failed_action_recovery_cost_usd",
    ))
    safe_resolutions = float(agent["validated_resolutions_without_harm"])

    result = {
        "classification": classification,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scenario_id": data["scenario_id"],
        "architecture": data["architecture"],
        "reliability_kpis": {
            "availability": _ratio(reliability["successful_service_minutes"], reliability["scheduled_service_minutes"]),
            "slo_attainment": _ratio(reliability["compliant_sli_windows"], reliability["total_sli_windows"]),
            "error_budget_consumption": _ratio(reliability["consumed_error_budget_minutes"], reliability["allocated_error_budget_minutes"]),
            "mttd_minutes": reliability["detected_at_minute"] - reliability["incident_start_minute"],
            "mtta_minutes": reliability["acknowledged_at_minute"] - reliability["alerted_at_minute"],
            "mttr_minutes": reliability["recovered_at_minute"] - reliability["incident_start_minute"],
            "change_failure_rate": _ratio(reliability["failed_changes"], reliability["production_changes"]),
            "rollback_success_rate": _ratio(reliability["successful_rollbacks"], reliability["rollback_attempts"]),
        },
        "migration_kpis": {
            "ingestion_parity": _ratio(target_events, source_events),
            "dropped_event_rate": _ratio(max(0, source_events - target_events), source_events),
            "required_field_preservation": _ratio(migration["required_fields_preserved"], migration["required_fields_evaluated"]),
            "query_equivalence": _ratio(migration["equivalent_queries"], queries_tested),
            "material_detection_parity": _ratio(migration["material_detections_reproduced"], detections_tested),
            "evidence_continuity": _ratio(migration["uninterrupted_evidence_streams"], migration["required_evidence_streams"]),
            "p95_ingestion_latency_seconds": migration["p95_ingestion_latency_seconds"],
            "p95_query_latency_seconds": migration["p95_query_latency_seconds"],
            "compression_efficiency": _ratio(migration["uncompressed_bytes"], migration["stored_bytes"]),
        },
        "agent_kpis": {
            "recommendation_acceptance_rate": _ratio(agent["approved_recommendations"], agent["recommendations_reviewed"]),
            "autonomous_resolution_rate": _ratio(agent["autonomous_resolutions"], agent["eligible_incidents"]),
            "unsafe_action_prevention_rate": _ratio(agent["unauthorized_actions_prevented"], unauthorized),
            "approval_bypass_rate": _ratio(agent["gated_actions_without_approval"], agent["approval_gated_attempts"]),
            "evidence_grounded_recommendation_rate": _ratio(agent["evidence_grounded_recommendations"], agent["recommendations_total"]),
            "agent_induced_incident_rate": _ratio(agent["agent_induced_incidents"], actions),
            "successful_reversal_rate": _ratio(agent["successful_reversals"], agent["reversal_attempts"]),
        },
        "grc_kpis": {
            "evidence_freshness_attainment": _ratio(grc["current_evidence"], evidence_required),
            "evidence_lineage_completeness": _ratio(grc["complete_lineage_evidence"], grc["evidence_collected"]),
            "control_automation_coverage": _ratio(grc["automated_controls"], grc["automation_eligible_controls"]),
            "operating_effectiveness_pass_rate": _ratio(grc["passing_control_tests"], grc["control_tests_executed"]),
            "evidence_acceptance_rate": _ratio(grc["accepted_evidence"], grc["reviewed_evidence"]),
            "stale_evidence_exposure_hours": grc["stale_evidence_exposure_hours"],
        },
        "unit_economics": {
            "monthly_observability_cost_usd": round(total_observability_cost, 2),
            "cost_per_ingested_gb_usd": round(total_observability_cost / economics["ingested_gb"], 4),
            "cost_per_monitored_service_usd": round(total_observability_cost / economics["monitored_services"], 2),
            "cost_per_valid_evidence_object_usd": round(economics["evidence_platform_cost_usd"] / grc["accepted_evidence"], 4),
            "verified_monthly_run_rate_savings_usd": round(monthly_savings, 2),
            "migration_break_even_months": round(migration_investment / monthly_savings, 2) if monthly_savings > 0 else None,
            "agent_cost_per_safe_resolution_usd": round(agent_cost / safe_resolutions, 2) if safe_resolutions else None,
            "net_toil_value_saved_usd": round(hours_saved * reviewer_rate - agent_cost, 2),
        },
        "decision_gates": {
            "ingestion_parity": _ratio(target_events, source_events) is not None and _ratio(target_events, source_events) >= 0.999,
            "required_field_preservation": migration["required_fields_preserved"] == migration["required_fields_evaluated"],
            "material_detection_parity": migration["material_detections_reproduced"] == migration["material_detections_tested"],
            "evidence_continuity": migration["uninterrupted_evidence_streams"] == migration["required_evidence_streams"],
            "unauthorized_actions_prevented": agent["unauthorized_actions_prevented"] == agent["unauthorized_attempts"],
            "rollback_validated": agent["successful_reversals"] == agent["reversal_attempts"],
            "economic_case": monthly_savings > 0,
        },
        "limitations": [
            "Synthetic results are not production outcomes.",
            "Detection parity is limited to material scenarios explicitly tested.",
            "The AI SRE engine recommends and simulates actions; it does not modify live infrastructure.",
            "Risk reduction requires a separately calibrated loss scenario."
        ],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["evidence_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result
