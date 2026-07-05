import matplotlib.pyplot as plt


def build_capital_chart(capital_history, initial_capital):
    """Crea la gráfica de evolución del capital."""
    fig, ax = plt.subplots(figsize=(5.2, 3.2), dpi=110)
    steps = list(range(1, len(capital_history) + 1))
    ax.plot(steps, capital_history, color="#38bdf8", linewidth=2)
    ax.axhline(initial_capital, color="#fbbf24", linestyle="--", linewidth=1)
    ax.set_title("Evolución del capital")
    ax.set_xlabel("Giro")
    ax.set_ylabel("Capital")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    return fig


def build_frequency_chart(number_counts):
    """Crea un histograma con la frecuencia de los números."""
    fig, ax = plt.subplots(figsize=(5.2, 3.2), dpi=110)
    numbers = sorted(number_counts.keys())
    values = [number_counts[n] for n in numbers]
    ax.bar(numbers, values, color="#f59e0b", alpha=0.9)
    ax.set_title("Frecuencia de números")
    ax.set_xlabel("Número")
    ax.set_ylabel("Veces")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    return fig


def build_color_chart(color_counts):
    """Crea un gráfico de barras para colores."""
    fig, ax = plt.subplots(figsize=(5.2, 3.2), dpi=110)
    colors = ["Rojo", "Negro", "Verde"]
    values = [color_counts.get(color, 0) for color in colors]
    ax.bar(colors, values, color=["#ef4444", "#111827", "#22c55e"], alpha=0.95)
    ax.set_title("Frecuencia por color")
    ax.set_xlabel("Color")
    ax.set_ylabel("Veces")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    return fig


def build_wins_chart(wins, losses):
    """Crea un gráfico circular de victorias y derrotas."""
    fig, ax = plt.subplots(figsize=(5.2, 3.2), dpi=110)
    labels = ["Victorias", "Derrotas"]
    sizes = [wins, losses]
    colors = ["#22c55e", "#ef4444"]
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
    ax.set_title("Victorias vs derrotas")
    fig.tight_layout()
    return fig
