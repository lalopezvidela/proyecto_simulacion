import unittest

from roulette_simulation import RouletteSimulator


class RouletteSimulationTests(unittest.TestCase):
    def test_run_simulation_returns_summary_and_history(self):
        simulator = RouletteSimulator()
        result = simulator.run_simulation(
            simulations=3,
            initial_capital=100,
            bet_amount=10,
            bet_type="red",
            selected_number=None,
        )

        self.assertEqual(result["total_spins"], 3)
        self.assertEqual(len(result["history"]), 3)
        self.assertIn("final_capital", result)
        self.assertIn("wins", result)
        self.assertIn("losses", result)
        self.assertIn("capital_history", result)


if __name__ == "__main__":
    unittest.main()
