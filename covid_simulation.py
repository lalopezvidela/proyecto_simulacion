import random


def simulate_covid(
    size: int,
    infected: int,
    steps: int,
    infection_probability: float = 0.35,
    death_probability: float = 0.05,
    recovery_time: int = 5,
    speed: int = 1,
) -> dict:

    # Validaciones
    if size <= 0 or infected <= 0 or steps <= 0:
        raise ValueError("Los valores deben ser mayores a cero")

    if infected > size * size:
        raise ValueError("Los infectados iniciales no pueden superar la población total")

    if not 0 <= infection_probability <= 1:
        raise ValueError("La probabilidad de contagio debe estar entre 0 y 1")

    if not 0 <= death_probability <= 1:
        raise ValueError("La probabilidad de fallecimiento debe estar entre 0 y 1")

    # 0 = susceptible
    # 1 = infectado
    # 2 = recuperado
    # 3 = fallecido

    grid = [[0 for _ in range(size)] for _ in range(size)]

    positions = random.sample(
        [(i, j) for i in range(size) for j in range(size)],
        infected,
    )

    # Guarda cuántos días lleva infectada cada persona
    infection_days = {}

    for row, col in positions:
        grid[row][col] = 1
        infection_days[(row, col)] = 0

    history = []
    max_infected = infected
    peak_step = 0
    total_population = size * size

    def count_states():
        susceptible = 0
        infected_count = 0
        recovered = 0
        deceased = 0

        for row in grid:
            for cell in row:
                if cell == 0:
                    susceptible += 1
                elif cell == 1:
                    infected_count += 1
                elif cell == 2:
                    recovered += 1
                else:
                    deceased += 1

        return susceptible, infected_count, recovered, deceased

    susceptible, infected_count, recovered, deceased = count_states()

    history.append({
        "step": 0,
        "susceptible": susceptible,
        "infected": infected_count,
        "recovered": recovered,
        "deceased": deceased,
    })

    # =========================
    # Simulación
    # =========================


    for step in range(1, steps + 1):
        next_grid = [row[:] for row in grid]
        new_days = infection_days.copy()

        for row in range(size):
            for col in range(size):

                state = grid[row][col]

                # -------------------
                # INFECTADO
                # -------------------
                if state == 1:

                    new_days[(row, col)] = new_days.get((row, col), 0) + 1

                    # Puede fallecer
                    if random.random() < death_probability:
                        next_grid[row][col] = 3

                        if (row, col) in new_days:
                            del new_days[(row, col)]

                    # Se recupera
                    elif new_days[(row, col)] >= recovery_time:
                        next_grid[row][col] = 2

                        if (row, col) in new_days:
                            del new_days[(row, col)]

                # -------------------
                # SUSCEPTIBLE
                # -------------------
                elif state == 0:

                    infected_neighbors = 0

                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):

                            if dr == 0 and dc == 0:
                                continue

                            nr = row + dr
                            nc = col + dc

                            if 0 <= nr < size and 0 <= nc < size:
                                if grid[nr][nc] == 1:
                                    infected_neighbors += 1

                    probability = infection_probability * infected_neighbors / 8

                    if random.random() < probability:
                        next_grid[row][col] = 1
                        new_days[(row, col)] = 0
        grid = next_grid
        infection_days = new_days

        susceptible, infected_count, recovered, deceased = count_states()
        if infected_count > max_infected:
          max_infected = infected_count
          peak_step = step
        history.append({
            "step": step,
            "susceptible": susceptible,
            "infected": infected_count,
            "recovered": recovered,
            "deceased": deceased,
        })

    # =========================
    # Coordenadas del gráfico
    # =========================

    width = 560
    height = 220

    margin_left = 30
    margin_right = 20
    margin_top = 20
    margin_bottom = 20

    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom

    max_value = total_population

    for index, item in enumerate(history):

        x = margin_left + chart_width * index / max(1, len(history) - 1)

        item["x"] = round(x, 2)

        item["y_susceptible"] = round(
            margin_top + chart_height - chart_height * item["susceptible"] / max_value,
            2,
        )

        item["y_infected"] = round(
            margin_top + chart_height - chart_height * item["infected"] / max_value,
            2,
        )

        item["y_recovered"] = round(
            margin_top + chart_height - chart_height * item["recovered"] / max_value,
            2,
        )

        item["y_deceased"] = round(
            margin_top + chart_height - chart_height * item["deceased"] / max_value,
            2,
        )

    return {
        "total": total_population,
        "susceptible": susceptible,
        "infected": infected_count,
        "recovered": recovered,
        "deceased": deceased,
        "history": history,
        "grid": grid,
        "max_infected": max_infected,
        "peak_step": peak_step,
    }