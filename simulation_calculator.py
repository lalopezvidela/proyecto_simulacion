import math
import random
from typing import Dict, List


def simulate_binomial(trials: int, probability: float, seed: int | None = None) -> Dict[str, float | int]:
    if trials <= 0:
        raise ValueError("El número de ensayos debe ser mayor a cero")
    if not 0 <= probability <= 1:
        raise ValueError("La probabilidad debe estar entre 0 y 1")

    if seed is not None:
        random.seed(seed)

    successes = sum(1 for _ in range(trials) if random.random() < probability)
    expected_successes = trials * probability
    expected_rate = expected_successes / trials if trials else 0

    return {
        "trials": trials,
        "probability": probability,
        "successes": successes,
        "expected_successes": expected_successes,
        "expected_rate": expected_rate,
    }


def analyze_sequence(values: List[float]) -> Dict[str, float | int]:
    if not values:
        raise ValueError("La lista de valores no puede estar vacía")

    values = [float(value) for value in values]
    count = len(values)
    mean = sum(values) / count
    variance = sum((value - mean) ** 2 for value in values) / count
    std_dev = math.sqrt(variance)

    expected = [mean for _ in values]
    chi_squared = sum((value - expected_value) ** 2 / expected_value for value, expected_value in zip(values, expected) if expected_value != 0)
    uniformity = 1.0 - min(1.0, std_dev / max(abs(mean), 1.0))

    return {
        "count": count,
        "mean": mean,
        "variance": variance,
        "std_dev": std_dev,
        "chi_squared": chi_squared,
        "uniformity": uniformity,
    }
