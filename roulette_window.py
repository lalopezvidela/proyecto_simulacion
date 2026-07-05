import math
import os
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from roulette_simulation import RouletteSimulator
from roulette_charts import build_capital_chart, build_frequency_chart, build_color_chart, build_wins_chart


class RouletteWindow(ctk.CTkToplevel):
    """Ventana principal para la simulación Monte Carlo de ruleta."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Simulación Monte Carlo - Ruleta")
        self.geometry("1320x860")
        self.configure(fg_color="#020617")
        self.grab_set()
        self.simulator = RouletteSimulator()
        self.canvas_frame = None
        self.wheel_angle = 0.0
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main = ctk.CTkFrame(self, fg_color="#0f172a", corner_radius=24)
        main.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)

        left = ctk.CTkFrame(main, fg_color="#111827", corner_radius=20)
        left.grid(row=0, column=0, padx=(18, 10), pady=18, sticky="nsew")
        left.grid_columnconfigure(0, weight=1)

        right = ctk.CTkFrame(main, fg_color="#111827", corner_radius=20)
        right.grid(row=0, column=1, padx=(10, 18), pady=18, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="Simulación Monte Carlo - Ruleta", font=("Segoe UI", 22, "bold"), text_color="#f8fafc").grid(row=0, column=0, padx=18, pady=(18, 4), sticky="w")
        ctk.CTkLabel(left, text="Interfaz moderna para simular apuestas y analizar resultados", font=("Segoe UI", 12), text_color="#94a3b8").grid(row=1, column=0, padx=18, pady=(0, 15), sticky="w")

        self.simulations_entry = ctk.CTkEntry(left, placeholder_text="Número de simulaciones", width=320, height=42)
        self.simulations_entry.grid(row=2, column=0, padx=18, pady=6)
        self.simulations_entry.insert(0, "100")

        self.capital_entry = ctk.CTkEntry(left, placeholder_text="Capital inicial", width=320, height=42)
        self.capital_entry.grid(row=3, column=0, padx=18, pady=6)
        self.capital_entry.insert(0, "100")

        self.bet_entry = ctk.CTkEntry(left, placeholder_text="Monto por apuesta", width=320, height=42)
        self.bet_entry.grid(row=4, column=0, padx=18, pady=6)
        self.bet_entry.insert(0, "10")

        self.bet_var = ctk.StringVar(value="Rojo")
        self.bet_option = ctk.CTkOptionMenu(left, values=["Rojo", "Negro", "Par", "Impar", "Número específico", "Docena", "Columna"], variable=self.bet_var, width=320, height=42)
        self.bet_option.grid(row=5, column=0, padx=18, pady=6)

        self.number_var = ctk.StringVar(value="0")
        self.number_combo = ctk.CTkComboBox(left, values=[str(n) for n in range(37)], variable=self.number_var, width=320, height=42)
        self.number_combo.grid(row=6, column=0, padx=18, pady=6)
        self.number_combo.grid_remove()

        self.docena_var = ctk.StringVar(value="1")
        self.docena_combo = ctk.CTkComboBox(left, values=["1", "2", "3"], variable=self.docena_var, width=320, height=42)
        self.docena_combo.grid(row=6, column=0, padx=18, pady=6)
        self.docena_combo.grid_remove()

        self.columna_var = ctk.StringVar(value="1")
        self.columna_combo = ctk.CTkComboBox(left, values=["1", "2", "3"], variable=self.columna_var, width=320, height=42)
        self.columna_combo.grid(row=6, column=0, padx=18, pady=6)
        self.columna_combo.grid_remove()

        self.bet_var.trace_add("write", self._toggle_extra_fields)

        buttons = ctk.CTkFrame(left, fg_color="transparent")
        buttons.grid(row=7, column=0, padx=18, pady=(12, 8), sticky="ew")
        buttons.grid_columnconfigure(0, weight=1)
        buttons.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(buttons, text="Iniciar simulación", command=self._run_simulation, height=42).grid(row=0, column=0, padx=(0, 6), sticky="ew")
        ctk.CTkButton(buttons, text="Reiniciar", command=self._reset, height=42, fg_color="#64748b", hover_color="#475569").grid(row=0, column=1, padx=(6, 0), sticky="ew")

        ctk.CTkButton(left, text="Exportar a Excel", command=self._export_excel, height=42, fg_color="#0f766e", hover_color="#115e59").grid(row=8, column=0, padx=18, pady=6)
        ctk.CTkButton(left, text="Exportar a PDF", command=self._export_pdf, height=42, fg_color="#7c3aed", hover_color="#6d28d9").grid(row=9, column=0, padx=18, pady=6)
        ctk.CTkButton(left, text="Volver al menú principal", command=self.destroy, height=42, fg_color="#ef4444", hover_color="#dc2626").grid(row=10, column=0, padx=18, pady=(6, 18))

        self.result_var = ctk.StringVar(value="Esperando simulación...")
        ctk.CTkLabel(left, textvariable=self.result_var, justify="left", text_color="#e2e8f0", wraplength=320).grid(row=11, column=0, padx=18, pady=(0, 18), sticky="w")

        ctk.CTkLabel(right, text="Ruleta y resultados", font=("Segoe UI", 18, "bold"), text_color="#f8fafc").grid(row=0, column=0, padx=18, pady=(18, 10), sticky="w")
        self.canvas = tk.Canvas(right, width=420, height=260, bg="#020617", highlightthickness=0)
        self.canvas.grid(row=1, column=0, padx=18, pady=8)

        self.summary_frame = ctk.CTkFrame(right, fg_color="#020617", corner_radius=16)
        self.summary_frame.grid(row=2, column=0, padx=18, pady=8, sticky="ew")
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(1, weight=1)

        self.stats_label = ctk.CTkLabel(self.summary_frame, text="", justify="left", text_color="#f8fafc")
        self.stats_label.grid(row=0, column=0, padx=12, pady=12, sticky="nw")

        self.table_frame = ctk.CTkFrame(right, fg_color="#020617", corner_radius=16)
        self.table_frame.grid(row=3, column=0, padx=18, pady=8, sticky="nsew")
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self.table_frame, columns=("spin", "number", "color", "bet", "won", "capital"), show="headings", height=8)
        self.tree.heading("spin", text="Giro")
        self.tree.heading("number", text="Número")
        self.tree.heading("color", text="Color")
        self.tree.heading("bet", text="Apuesta")
        self.tree.heading("won", text="¿Ganó?")
        self.tree.heading("capital", text="Capital")
        self.tree.column("spin", width=60, anchor="center")
        self.tree.column("number", width=80, anchor="center")
        self.tree.column("color", width=90, anchor="center")
        self.tree.column("bet", width=120, anchor="center")
        self.tree.column("won", width=80, anchor="center")
        self.tree.column("capital", width=100, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        self._draw_placeholder()

    def _toggle_extra_fields(self, *_args):
        selection = self.bet_var.get().lower()
        self.number_combo.grid_remove()
        self.docena_combo.grid_remove()
        self.columna_combo.grid_remove()
        if selection in {"número específico", "numero especifico", "number", "specific"}:
            self.number_combo.grid(row=6, column=0, padx=18, pady=6)
        elif selection in {"docena", "dozen"}:
            self.docena_combo.grid(row=6, column=0, padx=18, pady=6)
        elif selection in {"columna", "column"}:
            self.columna_combo.grid(row=6, column=0, padx=18, pady=6)

    def _draw_placeholder(self):
        self._draw_wheel(angle=0.0, result=None)

    def _draw_wheel(self, angle=0.0, result=None):
        self.canvas.delete("all")
        center_x = 210
        center_y = 130
        radius = 110

        self.canvas.create_oval(center_x - radius - 6, center_y - radius - 6, center_x + radius + 6, center_y + radius + 6, outline="#fbbf24", width=3)
        self.canvas.create_polygon(200, 35, 220, 35, 210, 70, fill="#fbbf24")

        sector_count = 37
        sector_size = 360 / sector_count
        for index in range(sector_count):
            start_angle = angle + (-90 + index * sector_size)
            end_angle = angle + (-90 + (index + 1) * sector_size)
            color = "#22c55e" if index == 0 else ("#ef4444" if index % 2 else "#111827")
            self.canvas.create_arc(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                start=start_angle,
                extent=sector_size,
                style="pieslice",
                outline="#f8fafc",
                width=1,
                fill=color,
            )

            mid_angle = math.radians(angle + (-90 + index * sector_size + sector_size / 2))
            label_x = center_x + math.cos(mid_angle) * (radius * 0.7)
            label_y = center_y + math.sin(mid_angle) * (radius * 0.7)
            self.canvas.create_text(label_x, label_y, text=str(index), fill="#f8fafc", font=("Segoe UI", 8, "bold"))

        self.canvas.create_oval(center_x - 26, center_y - 26, center_x + 26, center_y + 26, fill="#020617", outline="#64748b")

        ball_angle = angle + 25
        ball_x = center_x + math.cos(math.radians(ball_angle)) * (radius - 20)
        ball_y = center_y + math.sin(math.radians(ball_angle)) * (radius - 20)
        self.canvas.create_oval(ball_x - 7, ball_y - 7, ball_x + 7, ball_y + 7, fill="#f8fafc")

        if result is None:
            self.canvas.create_text(center_x, center_y + 145, text="Ruleta animada", fill="#94a3b8", font=("Segoe UI", 13, "bold"))
        else:
            self.canvas.create_text(center_x, center_y + 145, text=f"Número: {result['history'][-1]['number']} | {result['history'][-1]['color']}", fill="#38bdf8", font=("Segoe UI", 13, "bold"))

    def _run_simulation(self):
        try:
            simulations = int(self.simulations_entry.get())
            initial_capital = float(self.capital_entry.get())
            bet_amount = float(self.bet_entry.get())
            bet_type = self.bet_var.get().strip()
            selected_number = int(self.number_var.get()) if self.number_var.get().strip() else None
            docena = int(self.docena_var.get()) if self.docena_var.get().strip() else None
            column = int(self.columna_var.get()) if self.columna_var.get().strip() else None

            result = self.simulator.run_simulation(
                simulations=simulations,
                initial_capital=initial_capital,
                bet_amount=bet_amount,
                bet_type=bet_type,
                selected_number=selected_number,
                docena=docena,
                column=column,
            )
        except ValueError as exc:
            messagebox.showerror("Entrada inválida", str(exc))
            return

        self._populate_table(result["history"])
        self._update_results(result)
        self._animate_spin(result)

    def _populate_table(self, history):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in history:
            self.tree.insert("", "end", values=(
                item["spin"],
                item["number"],
                item["color"],
                item["bet_type"],
                "Sí" if item["won"] else "No",
                item["capital"],
            ))

    def _update_results(self, result):
        text = (
            f"Total de giros: {result['total_spins']}\n"
            f"Victorias: {result['wins']}\n"
            f"Derrotas: {result['losses']}\n"
            f"Capital inicial: {result['initial_capital']}\n"
            f"Capital final: {result['final_capital']}\n"
            f"Ganancia o pérdida: {result['profit']}\n"
            f"Probabilidad experimental de ganar: {result['experimental_probability']:.2%}\n"
            f"Porcentaje de victorias: {result['win_percentage']:.2f}%\n"
            f"Porcentaje de derrotas: {result['loss_percentage']:.2f}%"
        )
        self.result_var.set(text)
        self.stats_label.configure(text=text)

    def _animate_spin(self, result):
        last_number = result["history"][-1]["number"]
        sector_count = 37
        sector_size = 360 / sector_count
        sector_center = -90 + sector_size * (last_number + 0.5)
        target_angle = self.wheel_angle + 360 * 6 + (270 - sector_center)
        self._run_spin_animation(result, target_angle, 0, 30)

    def _run_spin_animation(self, result, target_angle, frame, total_frames):
        progress = frame / total_frames
        eased = progress * progress
        angle = self.wheel_angle + (target_angle - self.wheel_angle) * eased
        self._draw_wheel(angle=angle, result=None)
        if frame < total_frames:
            self.after(25, self._run_spin_animation, result, target_angle, frame + 1, total_frames)
        else:
            self.wheel_angle = target_angle
            self._draw_wheel(angle=self.wheel_angle, result=result)
            self._draw_results(result)

    def _draw_results(self, result):
        self._show_graphs(result)

    def _show_graphs(self, result):
        if self.canvas_frame is not None:
            self.canvas_frame.destroy()
        self.canvas_frame = ctk.CTkFrame(self, fg_color="#020617", corner_radius=16)
        self.canvas_frame.grid(row=4, column=0, padx=18, pady=8, sticky="ew")
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(1, weight=1)
        self.canvas_frame.grid_columnconfigure(2, weight=1)
        self.canvas_frame.grid_columnconfigure(3, weight=1)

        charts = [
            (build_capital_chart(result["capital_history"], result["initial_capital"]), 0),
            (build_frequency_chart(result["number_counts"]), 1),
            (build_color_chart(result["color_counts"]), 2),
            (build_wins_chart(result["wins"], result["losses"]), 3),
        ]
        for fig, col in charts:
            widget = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            widget.draw()
            widget.get_tk_widget().grid(row=0, column=col, padx=6, pady=6)

    def _reset(self):
        self.simulations_entry.delete(0, "end")
        self.simulations_entry.insert(0, "100")
        self.capital_entry.delete(0, "end")
        self.capital_entry.insert(0, "100")
        self.bet_entry.delete(0, "end")
        self.bet_entry.insert(0, "10")
        self.bet_var.set("Rojo")
        self.number_var.set("0")
        self.docena_var.set("1")
        self.columna_var.set("1")
        self.result_var.set("Esperando simulación...")
        self.stats_label.configure(text="")
        self.wheel_angle = 0.0
        for row in self.tree.get_children():
            self.tree.delete(row)
        self._draw_placeholder()

    def _export_excel(self):
        try:
            import csv
            path = os.path.join(os.getcwd(), "roulette_results.csv")
            with open(path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["Giro", "Número", "Color", "Apuesta", "Ganó", "Capital"])
                for item in self.tree.get_children():
                    values = self.tree.item(item, "values")
                    writer.writerow(values)
            messagebox.showinfo("Exportación completada", f"Resultados guardados en {path}")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _export_pdf(self):
        messagebox.showinfo("Exportación", "La exportación a PDF se dejará preparada para futuras versiones. Puede exportar los resultados en CSV desde el botón anterior.")
