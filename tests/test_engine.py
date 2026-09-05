import json
import tempfile
import unittest
from pathlib import Path

from kube_ai_sre.cli import main
from kube_ai_sre.engine import evaluate_scenario


FIXTURE = Path(__file__).parents[1] / "scenarios" / "deployment-auth-regression.json"


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FIXTURE.read_text())

    def test_all_decision_gates_pass(self):
        report = evaluate_scenario(self.data)
        self.assertTrue(all(report["decision_gates"].values()))
        self.assertEqual(report["classification"], "synthetic_controlled_test")

    def test_kpis_are_calculated_with_denominators(self):
        report = evaluate_scenario(self.data)
        self.assertEqual(report["migration_kpis"]["ingestion_parity"], 0.9995)
        self.assertEqual(report["agent_kpis"]["unsafe_action_prevention_rate"], 1.0)
        self.assertEqual(report["grc_kpis"]["evidence_acceptance_rate"], 0.95)

    def test_unit_economics(self):
        economics = evaluate_scenario(self.data)["unit_economics"]
        self.assertEqual(economics["monthly_observability_cost_usd"], 8000.0)
        self.assertEqual(economics["verified_monthly_run_rate_savings_usd"], 12000.0)
        self.assertEqual(economics["migration_break_even_months"], 6.0)
        self.assertEqual(economics["agent_cost_per_safe_resolution_usd"], 39.0)
        self.assertEqual(economics["net_toil_value_saved_usd"], 4410.0)

    def test_cli_generates_report(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            self.assertEqual(main([str(FIXTURE), "--output", str(output)]), 0)
            self.assertTrue(output.exists())

    def test_unknown_classification_fails(self):
        self.data["classification"] = "production-ish"
        with self.assertRaises(ValueError):
            evaluate_scenario(self.data)


if __name__ == "__main__":
    unittest.main()
