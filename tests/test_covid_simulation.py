import unittest

from covid_simulation import simulate_covid


class CovidSimulationTests(unittest.TestCase):
    def test_simulate_covid_supports_extended_parameters(self):
        result = simulate_covid(
            size=5,
            infected=2,
            steps=3,
            infection_probability=0.8,
            death_probability=0.1,
            recovery_time=1,
            speed=2,
        )
        self.assertEqual(result["total"], 25)
        self.assertIn("deceased", result)
        self.assertIn("history", result)
        self.assertEqual(result["history"][0]["step"], 0)
        self.assertGreaterEqual(result["infected"], 0)


if __name__ == "__main__":
    unittest.main()
