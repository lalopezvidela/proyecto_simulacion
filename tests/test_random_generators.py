import unittest

from random_generators import generate_sequence


class RandomGeneratorsTests(unittest.TestCase):
    def test_mixed_congruential_sequence(self):
        result = generate_sequence("mixto", seed=5, a=7, c=3, m=16, count=5)
        self.assertEqual(len(result), 5)
        self.assertTrue(all(0 <= value < 16 for value in result))

    def test_middle_square_sequence(self):
        result = generate_sequence("cuadrado_medio", seed=1234, digits=4, count=3)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(0 <= value < 10000 for value in result))

    def test_fibonacci_sequence(self):
        result = generate_sequence("fibonacci", seed=1, seed2=1, m=100, count=4)
        self.assertEqual(len(result), 4)
        self.assertTrue(all(0 <= value < 100 for value in result))

    def test_cellular_automaton_sequence(self):
        result = generate_sequence("automata_celular", seed=15, count=6)
        self.assertEqual(len(result), 6)
        self.assertTrue(all(value in (0, 1) for value in result))


if __name__ == "__main__":
    unittest.main()
