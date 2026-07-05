import unittest

from statistical_tests import run_statistical_tests


class StatisticalTestsTests(unittest.TestCase):
    def test_run_statistical_tests_returns_all_reports(self):
        values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.0]
        reports = run_statistical_tests(values)

        self.assertEqual(len(reports), 5)
        self.assertTrue(all("name" in item for item in reports))
        self.assertTrue(all("result" in item for item in reports))
        self.assertTrue(all("pass" in item["result"] for item in reports))


if __name__ == "__main__":
    unittest.main()
