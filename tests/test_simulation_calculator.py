import unittest

from simulation_calculator import analyze_sequence, simulate_binomial


class SimulationCalculatorTests(unittest.TestCase):
    def test_simulate_binomial_returns_expected_bounds(self):
        result = simulate_binomial(trials=100, probability=0.5, seed=42)
        self.assertEqual(result["trials"], 100)
        self.assertEqual(result["probability"], 0.5)
        self.assertGreaterEqual(result["successes"], 0)
        self.assertLessEqual(result["successes"], 100)
        self.assertAlmostEqual(result["expected_successes"], 50.0)
        self.assertAlmostEqual(result["expected_rate"], 0.5)

    def test_simulate_binomial_rejects_invalid_probability(self):
        with self.assertRaises(ValueError):
            simulate_binomial(trials=10, probability=1.2)

    def test_analyze_sequence_returns_summary_metrics(self):
        values = [1, 2, 3, 4, 5]
        result = analyze_sequence(values)
        self.assertEqual(result["count"], 5)
        self.assertGreater(result["mean"], 0)
        self.assertGreaterEqual(result["variance"], 0)
        self.assertIn("chi_squared", result)
        self.assertIn("uniformity", result)


if __name__ == "__main__":
    unittest.main()
