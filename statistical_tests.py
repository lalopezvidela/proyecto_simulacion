import math
import statistics
from typing import Any

from random_generators import generate_sequence


def _normalize_values(values: list[float], modulus: int | None = None) -> list[float]:
    if not values:
        raise ValueError("No se recibieron valores para analizar")
    if modulus is not None and modulus > 0:
        return [value / modulus for value in values]
    max_value = max(values)
    if max_value <= 0:
        return [0.0 for _ in values]
    return [value / (max_value + 1) for value in values]


def _chi_square_critical_value(df: int, alpha: float = 0.05) -> float:
    table = {
        1: 3.8415,
        2: 5.9915,
        3: 7.8147,
        4: 9.4877,
        5: 11.0705,
        6: 12.5916,
        7: 14.0671,
        8: 15.5073,
        9: 16.9190,
        10: 18.3070,
    }
    return table.get(df, 18.3070)


def _runs_test(values: list[float]) -> dict[str, Any]:
    median = statistics.median(values)
    signs = [1 if value >= median else -1 for value in values]
    runs = 1
    for index in range(1, len(signs)):
        if signs[index] != signs[index - 1]:
            runs += 1
    n1 = sum(1 for sign in signs if sign > 0)
    n2 = sum(1 for sign in signs if sign < 0)
    if n1 == 0 or n2 == 0:
        return {"runs": runs, "z": 0.0, "pass": True}
    n = len(signs)
    mean_runs = 1 + (2 * n1 * n2) / n
    var_runs = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n * n * (n - 1))
    z_score = (runs - mean_runs) / math.sqrt(var_runs) if var_runs > 0 else 0.0
    return {"runs": runs, "z": z_score, "pass": abs(z_score) < 1.96}


def run_statistical_tests(values: list[float], modulus: int | None = None) -> list[dict[str, Any]]:
    if not values:
        raise ValueError("Se requiere al menos un valor para las pruebas estadísticas")

    normalized = _normalize_values(values, modulus=modulus)
    n = len(normalized)
    mean = statistics.fmean(normalized)
    variance = statistics.variance(normalized) if n > 1 else 0.0

    bins = 10
    counts = [0] * bins
    for value in normalized:
        index = min(int(value * bins), bins - 1)
        counts[index] += 1
    expected = n / bins
    chi_square = sum(((count - expected) ** 2) / expected for count in counts)

    sorted_values = sorted(normalized)
    ks_stat = 0.0
    for index, value in enumerate(sorted_values, start=1):
        empirical = index / n
        theoretical = value
        ks_stat = max(ks_stat, abs(empirical - theoretical))
    ks_critical = 1.36 / math.sqrt(n) if n > 0 else 0.0

    runs_result = _runs_test(normalized)

    reports = [
        {
            "name": "Prueba de la media",
            "description": "Evalúa si el promedio de la muestra se aproxima al valor esperado para una distribución uniforme en [0,1].",
            "formula": "μ = (1/n) Σ xi",
            "inputs": {"n": n, "valores": normalized[:10]},
            "calculation": f"Σxi = {sum(normalized):.4f}; n = {n}; μ = {mean:.4f}",
            "metric": mean,
            "expected": 0.5,
            "result": {
                "pass": abs(mean - 0.5) <= 0.1,
                "interpretation": "Pasa si el promedio se aproxima a 0.5." if abs(mean - 0.5) <= 0.1 else "No pasa porque el promedio se aleja demasiado de 0.5.",
            },
        },
        {
            "name": "Prueba de la varianza",
            "description": "Comprueba si la dispersión de los datos se aproxima a la varianza esperada de una distribución uniforme.",
            "formula": "s² = (1/(n-1)) Σ (xi - μ)²",
            "inputs": {"n": n, "valores": normalized[:10]},
            "calculation": f"μ = {mean:.4f}; s² = {variance:.4f}",
            "metric": variance,
            "expected": 1 / 12,
            "result": {
                "pass": abs(variance - (1 / 12)) <= max(0.04, 1.96 * math.sqrt(1 / (180 * max(1, n - 1)))),
                "interpretation": "Pasa si la varianza se aproxima a 1/12." if abs(variance - (1 / 12)) <= max(0.04, 1.96 * math.sqrt(1 / (180 * max(1, n - 1)))) else "No pasa porque la dispersión es demasiado alta o baja.",
            },
        },
        {
            "name": "Prueba Chi-cuadrado",
            "description": "Compara la frecuencia observada en intervalos con la frecuencia esperada en una distribución uniforme.",
            "formula": "χ² = Σ ((Oi - Ei)² / Ei)",
            "inputs": {"bins": bins, "observados": counts, "esperados": [expected] * bins},
            "calculation": f"χ² = {chi_square:.4f}; gl = {bins - 1}",
            "metric": chi_square,
            "expected": _chi_square_critical_value(bins - 1),
            "result": {
                "pass": chi_square < _chi_square_critical_value(bins - 1),
                "interpretation": "Pasa si χ² es menor que el valor crítico." if chi_square < _chi_square_critical_value(bins - 1) else "No pasa porque la distribución observada se aleja de la uniforme.",
            },
        },
        {
            "name": "Prueba de Kolmogorov-Smirnov",
            "description": "Compara la función de distribución empírica con la teórica uniforme para medir la distancia máxima.",
            "formula": "D = max |Fn(x) - F(x)|",
            "inputs": {"n": n, "valores_ordenados": sorted_values[:10]},
            "calculation": f"D = {ks_stat:.4f}; D_crit = {ks_critical:.4f}",
            "metric": ks_stat,
            "expected": ks_critical,
            "result": {
                "pass": ks_stat < ks_critical,
                "interpretation": "Pasa si la distancia máxima es menor que el valor crítico." if ks_stat < ks_critical else "No pasa porque la muestra se aleja de la distribución uniforme.",
            },
        },
        {
            "name": "Prueba de independencia",
            "description": "Evalúa si los valores cambian de manera aleatoria usando una prueba de corridas sobre la mediana.",
            "formula": "z = (R - μR) / σR",
            "inputs": {"n": n, "corridas": runs_result["runs"]},
            "calculation": f"R = {runs_result['runs']}; z = {runs_result['z']:.4f}",
            "metric": runs_result["z"],
            "expected": 1.96,
            "result": {
                "pass": runs_result["pass"],
                "interpretation": "Pasa si las corridas son compatibles con independencia." if runs_result["pass"] else "No pasa porque hay demasiadas o muy pocas corridas.",
            },
        },
    ]
    return reports


def generate_and_test_sequence(method: str, seed: int = 1, a: int | None = None, c: int | None = None, m: int | None = None, seed2: int | None = None, digits: int | None = None, count: int = 20) -> dict[str, Any]:
    values = generate_sequence(method=method, seed=seed, a=a, c=c, m=m, seed2=seed2, digits=digits, count=count)
    reports = run_statistical_tests(values, modulus=m)
    return {
        "values": values,
        "reports": reports,
        "summary": {
            "passed": sum(1 for item in reports if item["result"]["pass"]),
            "total": len(reports),
        },
    }
