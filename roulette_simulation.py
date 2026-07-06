import random
from collections import Counter


class RouletteSimulator:
    """Modelo simple de ruleta para simulación Monte Carlo."""

    def __init__(self):
        self.numbers = list(range(37))

        red_numbers = {
            1, 3, 5, 7, 9,
            12, 14, 16, 18,
            19, 21, 23, 25, 27,
            30, 32, 34, 36
        }

        self.colors = {}

        for n in self.numbers:
            if n == 0:
                self.colors[n] = "Verde"
            elif n in red_numbers:
                self.colors[n] = "Rojo"
            else:
                self.colors[n] = "Negro"

    def _get_color(self, number: int) -> str:
        return self.colors[number]

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

    def _wins_bet(
        self,
        number: int,
        bet_type: str,
        selected_number=None,
        docena=None,
        column=None,
    ) -> bool:

        bet_type = (bet_type or "").strip().lower()

        if bet_type in ("red", "rojo"):
            return self._get_color(number) == "Rojo"

        elif bet_type in ("black", "negro"):
            return self._get_color(number) == "Negro"

        elif bet_type in ("even", "par"):
            return self._is_par(number)

        elif bet_type in ("odd", "impar"):
            return self._is_impar(number)

        elif bet_type in ("number", "numero", "specific", "especifico"):
            return number == selected_number

        elif bet_type in ("dozen", "docena"):
            return self._is_docena(number, docena)

        elif bet_type in ("column", "columna"):
            return self._is_columna(number, column)

        return False

    def run_simulation(
        self,
        simulations,
        initial_capital,
        bet_amount,
        bet_type,
        selected_number=None,
        docena=None,
        column=None,
    ):

        if simulations <= 0:
            raise ValueError("El número de simulaciones debe ser mayor a cero")

        capital = float(initial_capital)

        history = []
        number_counts = Counter()
        color_counts = Counter()

        even_count = 0
        odd_count = 0

        for spin in range(1, simulations + 1):

            number = random.choice(self.numbers)
            color = self._get_color(number)

            win = self._wins_bet(
                number,
                bet_type,
                selected_number,
                docena,
                column,
            )

            if win:

                if bet_type.lower() in (
                    "rojo", "red",
                    "negro", "black",
                    "par", "even",
                    "impar", "odd"
                ):
                    capital += bet_amount

                elif bet_type.lower() in (
                    "docena", "dozen",
                    "columna", "column"
                ):
                    capital += bet_amount * 2

                elif bet_type.lower() in (
                    "numero", "number",
                    "specific", "especifico"
                ):
                    capital += bet_amount * 35

            else:
                capital -= bet_amount

            if number != 0:
                if number % 2 == 0:
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

        wins = sum(1 for h in history if h["won"])
        losses = simulations - wins

        experimental_probability = wins / simulations
        win_percentage = wins / simulations * 100
        loss_percentage = losses / simulations * 100

        most_frequent_number = number_counts.most_common(1)[0][0]
        most_frequent_color = color_counts.most_common(1)[0][0]

        return {
            "total_spins": simulations,
            "wins": wins,
            "losses": losses,
            "draws": 0,
            "initial_capital": round(initial_capital, 2),
            "final_capital": round(capital, 2),
            "profit": round(capital - initial_capital, 2),
            "experimental_probability": round(experimental_probability, 4),
            "win_percentage": round(win_percentage, 2),
            "loss_percentage": round(loss_percentage, 2),
            "most_frequent_number": most_frequent_number,
            "most_frequent_color": most_frequent_color,
            "number_counts": dict(number_counts),
            "color_counts": dict(color_counts),
            "even_count": even_count,
            "odd_count": odd_count,
            "capital_history": [h["capital"] for h in history],
            "history": history,
        }