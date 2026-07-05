import customtkinter as ctk
from tkinter import messagebox

from simulation_calculator import analyze_sequence, simulate_binomial


class CalculatorWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Calculadora de simulación")
        self.geometry("900x640")
        self.configure(fg_color="#020617")
        self.grab_set()
        self.history = []
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

        ctk.CTkLabel(left, text="Calculadora de simulación", font=("Segoe UI", 20, "bold"), text_color="#f8fafc").grid(row=0, column=0, padx=18, pady=(18, 6), sticky="w")
        ctk.CTkLabel(left, text="Ingresa parámetros y revisa métricas", font=("Segoe UI", 12), text_color="#94a3b8").grid(row=1, column=0, padx=18, pady=(0, 10), sticky="w")

        self.trials_entry = ctk.CTkEntry(left, placeholder_text="Número de ensayos", width=320, height=42)
        self.trials_entry.grid(row=2, column=0, padx=18, pady=8)

        self.probability_entry = ctk.CTkEntry(left, placeholder_text="Probabilidad (0 a 1)", width=320, height=42)
        self.probability_entry.grid(row=3, column=0, padx=18, pady=8)

        self.seed_entry = ctk.CTkEntry(left, placeholder_text="Semilla (opcional)", width=320, height=42)
        self.seed_entry.grid(row=4, column=0, padx=18, pady=8)

        self.values_entry = ctk.CTkEntry(left, placeholder_text="Valores (separados por coma)", width=320, height=42)
        self.values_entry.grid(row=5, column=0, padx=18, pady=8)

        ctk.CTkButton(left, text="Simular", width=320, height=42, command=self._run_simulation).grid(row=6, column=0, padx=18, pady=(10, 8))
        ctk.CTkButton(left, text="Cerrar", width=320, height=42, fg_color="#64748b", hover_color="#475569", command=self.destroy).grid(row=7, column=0, padx=18, pady=8)

        self.result_var = ctk.StringVar(value="")
        ctk.CTkLabel(left, textvariable=self.result_var, justify="left", text_color="#e2e8f0", wraplength=320).grid(row=8, column=0, padx=18, pady=(12, 18))

        ctk.CTkLabel(right, text="Métricas y resultados", font=("Segoe UI", 18, "bold"), text_color="#f8fafc").grid(row=0, column=0, padx=18, pady=(18, 10), sticky="w")
        self.metric_var = ctk.StringVar(value="")
        ctk.CTkLabel(right, textvariable=self.metric_var, justify="left", text_color="#e2e8f0", wraplength=360).grid(row=1, column=0, padx=18, pady=(0, 10), sticky="w")

        self.history_box = ctk.CTkTextbox(right, height=220, fg_color="#0f172a", text_color="#f8fafc")
        self.history_box.grid(row=2, column=0, padx=18, pady=8, sticky="nsew")
        self.history_box.insert("end", "Sin resultados aún.\n")

    def _run_simulation(self):
        try:
            trials = int(self.trials_entry.get())
            probability = float(self.probability_entry.get())
            seed = int(self.seed_entry.get()) if self.seed_entry.get().strip() else None
            result = simulate_binomial(trials=trials, probability=probability, seed=seed)

            values_text = self.values_entry.get().strip()
            analysis = None
            if values_text:
                values = [float(item.strip()) for item in values_text.split(",") if item.strip()]
                analysis = analyze_sequence(values)

            self.result_var.set(
                f"Ensayos: {result['trials']}\n"
                f"Probabilidad: {result['probability']}\n"
                f"Éxitos obtenidos: {result['successes']}\n"
                f"Éxitos esperados: {result['expected_successes']}\n"
                f"Tasa esperada: {result['expected_rate']:.2f}"
            )

            if analysis is None:
                self.metric_var.set("Ingresa valores separados por coma para ver promedio, varianza, chi-cuadrada y uniformidad.")
            else:
                self.metric_var.set(
                    f"Promedio: {analysis['mean']:.3f}\n"
                    f"Varianza: {analysis['variance']:.3f}\n"
                    f"Chi-cuadrada: {analysis['chi_squared']:.3f}\n"
                    f"Uniformidad: {analysis['uniformity']:.3f}"
                )

            self.history.append(
                f"Ensayos={result['trials']} | Éxitos={result['successes']} | Prob={probability}"
            )
            self.history_box.delete("1.0", "end")
            self.history_box.insert("end", "\n".join(self.history[-8:]) + "\n")
        except ValueError as exc:
            messagebox.showerror("Entrada inválida", str(exc))
