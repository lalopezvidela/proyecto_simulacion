import random
from collections import Counter


class RouletteSimulator:
    """Modelo simple de ruleta para simulación Monte Carlo."""

    def __init__(self):
        self.numbers = list(range(37))
        self.colors = {n: "Verde" if n == 0 else ("Rojo" if n % 2 else "Negro") for n in self.numbers}

    def _get_color(self, number: int) -> str:
        return self.colors[number]

    def _is_even(self, number: int) -> bool:
        return number % 2 == 0

    def _is_odd(self, number: int) -> bool:
        return number % 2 != 0

    def _is_par(self, number: int) -> bool:
        return number != 0 and number % 2 == 0

    def _is_impar(self, number: int) -> bool:
        return number != 0 and number % 2 != 0

    def _is_docena(self, number: int, docena: int) -> bool:
        if number == 0:
            return False
        if docena == 1:
            return 1 <= number <= 12
        if docena == 2:
            return 13 <= number <= 24
        return 25 <= number <= 36

    def _is_columna(self, number: int, column: int) -> bool:
        if number == 0:
            return False
        return (number - 1) % 3 == (column - 1)

    def _wins_bet(self, number: int, bet_type: str, selected_number: int | None = None, docena: int | None = None, column: int | None = None) -> bool:
        bet_type = (bet_type or "").strip().lower()
        if bet_type in {"red", "rojo"}:
            return self._get_color(number) == "Rojo"
        if bet_type in {"black", "negro"}:
            return self._get_color(number) == "Negro"
        if bet_type in {"even", "par"}:
            return self._is_par(number)
        if bet_type in {"odd", "impar"}:
            return self._is_impar(number)
        if bet_type in {"number", "numero", "specific", "especifico"}:
            return number == (selected_number if selected_number is not None else -1)
        if bet_type in {"dozen", "docena"}:
            return self._is_docena(number, docena or 1)
        if bet_type in {"column", "columna"}:
            return self._is_columna(number, column or 1)
        return False

    def run_simulation(self, simulations: int, initial_capital: float, bet_amount: float, bet_type: str, selected_number: int | None = None, docena: int | None = None, column: int | None = None) -> dict:
        if simulations <= 0:
            raise ValueError("El número de simulaciones debe ser mayor a cero")
        if initial_capital <= 0:
            raise ValueError("El capital inicial debe ser mayor a cero")
        if bet_amount <= 0:
            raise ValueError("El monto por apuesta debe ser mayor a cero")

        capital = float(initial_capital)
        history = []
        number_counts = Counter()
        color_counts = Counter()
        even_count = 0
        odd_count = 0

        for spin in range(1, simulations + 1):
            number = random.randint(0, 36)
            color = self._get_color(number)
            win = self._wins_bet(number, bet_type, selected_number=selected_number, docena=docena, column=column)
            if win:
                capital += bet_amount
            else:
                capital -= bet_amount

            if number != 0:
                if self._is_even(number):
                    even_count += 1
                else:
                    odd_count += 1

            number_counts[number] += 1
            color_counts[color] += 1
            history.append({
                "spin": spin,
                "number": number,
                "color": color,
                "bet_type": bet_type,
                "won": win,
                "capital": round(capital, 2),
            })

        wins = sum(1 for item in history if item["won"])
        losses = sum(1 for item in history if not item["won"])
        experimental_probability = wins / simulations if simulations else 0.0
        win_percentage = (wins / simulations * 100) if simulations else 0.0
        loss_percentage = (losses / simulations * 100) if simulations else 0.0
        most_frequent_number = max(number_counts.items(), key=lambda item: (item[1], -item[0]))[0] if number_counts else 0
        most_frequent_color = max(color_counts.items(), key=lambda item: (item[1], item[0]))[0] if color_counts else "Verde"

        return {
            "total_spins": simulations,
            "wins": wins,
            "losses": losses,
            "draws": 0,
            "initial_capital": round(float(initial_capital), 2),
            "final_capital": round(capital, 2),
            "profit": round(capital - float(initial_capital), 2),
            "experimental_probability": round(experimental_probability, 4),
            "win_percentage": round(win_percentage, 2),
            "loss_percentage": round(loss_percentage, 2),
            "most_frequent_number": most_frequent_number,
            "most_frequent_color": most_frequent_color,
            "number_counts": dict(number_counts),
            "color_counts": dict(color_counts),
            "even_count": even_count,
            "odd_count": odd_count,
            "capital_history": [item["capital"] for item in history],
            "history": history,
        }
