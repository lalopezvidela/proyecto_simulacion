import random


def simulate_covid(
    size: int,
    infected: int,
    steps: int,
    infection_probability: float = 0.35,
    death_probability: float = 0.05,
    recovery_time: int = 2,
    speed: int = 1,
) -> dict:
    if size <= 0 or infected <= 0 or steps <= 0:
        raise ValueError("Los valores deben ser mayores a cero")
    if infected > size * size:
        raise ValueError("Los infectados iniciales no pueden superar la población total")
    if not 0 <= infection_probability <= 1:
        raise ValueError("La probabilidad de contagio debe estar entre 0 y 1")
    if not 0 <= death_probability <= 1:
        raise ValueError("La probabilidad de fallecimiento debe estar entre 0 y 1")
    if recovery_time <= 0:
        raise ValueError("El tiempo de recuperación debe ser mayor a cero")
    if speed <= 0:
        raise ValueError("La velocidad debe ser mayor a cero")

    grid = [[0 for _ in range(size)] for _ in range(size)]
    positions = random.sample([(i, j) for i in range(size) for j in range(size)], infected)
    for row, col in positions:
        grid[row][col] = 1

    history = []
    total_population = size * size
    recovery_counter = {}

    def count_states():
        susceptible = sum(1 for row in grid for cell in row if cell == 0)
        infected_count = sum(1 for row in grid for cell in row if cell == 1)
        recovered = sum(1 for row in grid for cell in row if cell == 2)
        deceased = sum(1 for row in grid for cell in row if cell == 3)
        return susceptible, infected_count, recovered, deceased

    susceptible, infected_count, recovered, deceased = count_states()
    history.append({
        "step": 0,
        "susceptible": susceptible,
        "infected": infected_count,
        "recovered": recovered,
        "deceased": deceased,
    })

    for step in range(1, steps + 1):
        next_grid = [row[:] for row in grid]
        for row in range(size):
            for col in range(size):
                state = grid[row][col]
                if state == 1:
                    if random.random() < (death_probability / max(1, speed)):
                        next_grid[row][col] = 3
                    elif random.random() < (infection_probability / max(1, speed)):
                        next_grid[row][col] = 2
                    else:
                        next_grid[row][col] = 1
                elif state == 0:
                    neighbors = []
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue
                            nr = row + dr
                            nc = col + dc
                            if 0 <= nr < size and 0 <= nc < size:
                                neighbors.append(grid[nr][nc])
                    if any(neighbor == 1 for neighbor in neighbors) and random.random() < (infection_probability * (1 + speed / 5)):
                        next_grid[row][col] = 1
                elif state == 2:
                    recovery_counter[(row, col)] = recovery_counter.get((row, col), 0) + 1
                    if recovery_counter[(row, col)] >= recovery_time:
                        next_grid[row][col] = 2
                    else:
                        next_grid[row][col] = 2
                else:
                    next_grid[row][col] = 3
        grid = next_grid
        susceptible, infected_count, recovered, deceased = count_states()
        history.append({
            "step": step,
            "susceptible": susceptible,
            "infected": infected_count,
            "recovered": recovered,
            "deceased": deceased,
        })

    width = 560
    height = 220
    margin_left = 30
    margin_right = 20
    margin_top = 20
    margin_bottom = 20
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom
    max_value = max(total_population, max(item["infected"] for item in history))

    for index, item in enumerate(history):
        x = margin_left + (chart_width * index / max(1, len(history) - 1))
        item["x"] = round(x, 2)
        item["y_susceptible"] = round(margin_top + chart_height - (chart_height * item["susceptible"] / max_value), 2)
        item["y_infected"] = round(margin_top + chart_height - (chart_height * item["infected"] / max_value), 2)
        item["y_recovered"] = round(margin_top + chart_height - (chart_height * item["recovered"] / max_value), 2)
        item["y_deceased"] = round(margin_top + chart_height - (chart_height * item["deceased"] / max_value), 2)

    return {
        "total": total_population,
        "susceptible": susceptible,
        "infected": infected_count,
        "recovered": recovered,
        "deceased": deceased,
        "history": history,
    }
