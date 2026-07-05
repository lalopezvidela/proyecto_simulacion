import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

from covid_simulation import simulate_covid


class CovidWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Simulación COVID")
        self.geometry("980x720")
        self.configure(fg_color="#020617")
        self.grab_set()
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main = ctk.CTkFrame(self, fg_color="#0f172a", corner_radius=24)
        main.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)

        left = ctk.CTkFrame(main, fg_color="#111827", corner_radius=18)
        left.grid(row=0, column=0, padx=(18, 9), pady=18, sticky="nsew")
        left.grid_columnconfigure(0, weight=1)

        right = ctk.CTkFrame(main, fg_color="#111827", corner_radius=18)
        right.grid(row=0, column=1, padx=(9, 18), pady=18, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="Simulación COVID", font=("Segoe UI", 20, "bold"), text_color="#f8fafc").grid(row=0, column=0, padx=18, pady=(18, 8), sticky="w")
        ctk.CTkLabel(left, text="Configura los parámetros del modelo", font=("Segoe UI", 12), text_color="#94a3b8").grid(row=1, column=0, padx=18, pady=(0, 10), sticky="w")

        self.size_entry = ctk.CTkEntry(left, placeholder_text="Tamaño de la cuadrícula", width=320, height=42)
        self.size_entry.grid(row=2, column=0, padx=18, pady=8)

        self.infected_entry = ctk.CTkEntry(left, placeholder_text="Infectados iniciales", width=320, height=42)
        self.infected_entry.grid(row=3, column=0, padx=18, pady=8)

        self.steps_entry = ctk.CTkEntry(left, placeholder_text="Iteraciones", width=320, height=42)
        self.steps_entry.grid(row=4, column=0, padx=18, pady=8)

        self.infection_entry = ctk.CTkEntry(left, placeholder_text="Probabilidad de contagio", width=320, height=42)
        self.infection_entry.grid(row=5, column=0, padx=18, pady=8)

        self.death_entry = ctk.CTkEntry(left, placeholder_text="Probabilidad de fallecimiento", width=320, height=42)
        self.death_entry.grid(row=6, column=0, padx=18, pady=8)

        self.recovery_entry = ctk.CTkEntry(left, placeholder_text="Tiempo de recuperación", width=320, height=42)
        self.recovery_entry.grid(row=7, column=0, padx=18, pady=8)

        self.speed_entry = ctk.CTkEntry(left, placeholder_text="Velocidad", width=320, height=42)
        self.speed_entry.grid(row=8, column=0, padx=18, pady=8)

        ctk.CTkButton(left, text="Simular", width=320, height=42, command=self._run_simulation).grid(row=9, column=0, padx=18, pady=(12, 8))
        ctk.CTkButton(left, text="Cerrar", width=320, height=42, fg_color="#64748b", hover_color="#475569", command=self.destroy).grid(row=10, column=0, padx=18, pady=8)

        self.summary_var = ctk.StringVar(value="")
        ctk.CTkLabel(left, textvariable=self.summary_var, justify="left", text_color="#e2e8f0", wraplength=320).grid(row=11, column=0, padx=18, pady=(12, 18))

        ctk.CTkLabel(right, text="Evolución", font=("Segoe UI", 18, "bold"), text_color="#f8fafc").grid(row=0, column=0, padx=18, pady=(18, 10), sticky="w")
        self.canvas = tk.Canvas(right, width=420, height=220, bg="#020617", highlightthickness=0)
        self.canvas.grid(row=1, column=0, padx=18, pady=8)

        self.history_box = ctk.CTkTextbox(right, height=180, fg_color="#0f172a", text_color="#f8fafc")
        self.history_box.grid(row=2, column=0, padx=18, pady=8, sticky="nsew")

    def _run_simulation(self):
        try:
            size = int(self.size_entry.get())
            infected = int(self.infected_entry.get())
            steps = int(self.steps_entry.get())
            infection_probability = float(self.infection_entry.get()) if self.infection_entry.get().strip() else 0.35
            death_probability = float(self.death_entry.get()) if self.death_entry.get().strip() else 0.05
            recovery_time = int(self.recovery_entry.get()) if self.recovery_entry.get().strip() else 2
            speed = int(self.speed_entry.get()) if self.speed_entry.get().strip() else 1

            result = simulate_covid(
                size=size,
                infected=infected,
                steps=steps,
                infection_probability=infection_probability,
                death_probability=death_probability,
                recovery_time=recovery_time,
                speed=speed,
            )

            self.summary_var.set(
                f"Sanos: {result['susceptible']}\n"
                f"Infectados: {result['infected']}\n"
                f"Recuperados: {result['recovered']}\n"
                f"Fallecidos: {result['deceased']}"
            )

            lines = []
            for item in result.get("history", []):
                lines.append(
                    f"Paso {item['step']}: sanos={item['susceptible']}, infectados={item['infected']}, recuperados={item['recovered']}, fallecidos={item['deceased']}"
                )
            self._draw_chart(result.get("history", []))
            self.history_box.delete("1.0", "end")
            self.history_box.insert("end", "\n".join(lines))
        except ValueError as exc:
            messagebox.showerror("Entrada inválida", str(exc))

    def _draw_chart(self, history):
        self.canvas.delete("all")
        if not history:
            return

        width = 420
        height = 220
        margin = 24
        chart_width = width - margin * 2
        chart_height = height - margin * 2
        max_value = max(item["susceptible"] + item["infected"] + item["recovered"] + item["deceased"] for item in history)

        self.canvas.create_line(margin, height - margin, width - margin, height - margin, fill="#475569", width=1)
        self.canvas.create_line(margin, margin, margin, height - margin, fill="#475569", width=1)

        colors = {
            "susceptible": "#38bdf8",
            "infected": "#f87171",
            "recovered": "#34d399",
            "deceased": "#facc15",
        }

        for key in ["susceptible", "infected", "recovered", "deceased"]:
            points = []
            for index, item in enumerate(history):
                x = margin + (chart_width * index / max(1, len(history) - 1))
                y = height - margin - (chart_height * item[key] / max(1, max_value))
                points.append((x, y))
            if len(points) > 1:
                self.canvas.create_line(points, fill=colors[key], width=2, smooth=True)

        legend_y = 16
        self.canvas.create_text(24, legend_y, text="Sanos", fill=colors["susceptible"], anchor="w")
        self.canvas.create_text(96, legend_y, text="Infectados", fill=colors["infected"], anchor="w")
        self.canvas.create_text(180, legend_y, text="Recuperados", fill=colors["recovered"], anchor="w")
        self.canvas.create_text(270, legend_y, text="Fallecidos", fill=colors["deceased"], anchor="w")
