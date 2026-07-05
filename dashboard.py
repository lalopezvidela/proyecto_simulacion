import datetime

import customtkinter as ctk
from tkinter import messagebox

from calculator_window import CalculatorWindow
from covid_window import CovidWindow
from roulette_window import RouletteWindow
from statistical_tests_window import StatisticalTestsWindow


class DashboardApp(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Dashboard - Sistema de Simulación")
        self.geometry("1024x700")
        self.configure(fg_color="#020617")
        self.grab_set()
        self._build_ui()
        self._update_clock()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main = ctk.CTkFrame(self, fg_color="#0f172a", corner_radius=24)
        main.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(main, fg_color="#111827", corner_radius=18)
        header.grid(row=0, column=0, padx=18, pady=18, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        self.welcome_var = ctk.StringVar(value="Bienvenido")
        self.date_var = ctk.StringVar(value="")
        self.time_var = ctk.StringVar(value="")

        ctk.CTkLabel(header, textvariable=self.welcome_var, font=("Segoe UI", 22, "bold"), text_color="#f8fafc").grid(row=0, column=0, padx=18, pady=(16, 2), sticky="w")
        ctk.CTkLabel(header, textvariable=self.date_var, font=("Segoe UI", 13), text_color="#94a3b8").grid(row=1, column=0, padx=18, pady=(0, 2), sticky="w")
        ctk.CTkLabel(header, textvariable=self.time_var, font=("Segoe UI", 13, "bold"), text_color="#38bdf8").grid(row=2, column=0, padx=18, pady=(0, 16), sticky="w")

        body = ctk.CTkFrame(main, fg_color="#020617", corner_radius=18)
        body.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="nsew")
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        body.grid_columnconfigure(2, weight=1)

        cards = [
            ("Calculadora de simulación", "Analiza modelos probabilísticos y métricas de simulación.", self._open_calculator),
            ("Simulación COVID", "Explora un modelo epidemiológico con estados dinámicos.", self._open_covid),
            ("Generadores pseudoaleatorios", "Configura y analiza secuencias con distintos métodos de generación.", self._open_statistical_tests),
            ("Simulación Monte Carlo - Ruleta", "Prueba una ruleta con apuestas y resultados estadísticos.", self._open_roulette),
            ("Acerca del proyecto", "Conoce la finalidad y alcance del sistema.", self._show_about),
        ]

        for index, (title, description, action) in enumerate(cards):
            card = ctk.CTkFrame(body, fg_color="#111827", corner_radius=20)
            card.grid(row=0, column=index, padx=10, pady=10, sticky="nsew")
            card.grid_columnconfigure(0, weight=1)
            card.grid_rowconfigure(0, weight=1)

            ctk.CTkLabel(card, text=title, font=("Segoe UI", 17, "bold"), text_color="#f8fafc").grid(row=0, column=0, padx=18, pady=(18, 8), sticky="w")
            ctk.CTkLabel(card, text=description, font=("Segoe UI", 12), text_color="#cbd5e1", wraplength=220).grid(row=1, column=0, padx=18, pady=(0, 16), sticky="w")
            ctk.CTkButton(card, text="Abrir", width=180, height=40, command=action).grid(row=2, column=0, padx=18, pady=(0, 18))

        footer = ctk.CTkFrame(main, fg_color="#111827", corner_radius=18)
        footer.grid(row=2, column=0, padx=18, pady=(0, 18), sticky="ew")
        footer.grid_columnconfigure(0, weight=1)
        ctk.CTkButton(footer, text="Cerrar sesión", width=220, height=42, fg_color="#ef4444", hover_color="#dc2626", command=self._logout).grid(row=0, column=0, padx=18, pady=16)

    def _update_clock(self):
        now = datetime.datetime.now()
        self.welcome_var.set(f"Bienvenido, {self.parent.username_entry.get().strip() or 'usuario'}")
        self.date_var.set(now.strftime("%d/%m/%Y"))
        self.time_var.set(now.strftime("%H:%M:%S"))
        self.after(1000, self._update_clock)

    def _open_calculator(self):
        CalculatorWindow(self)

    def _open_covid(self):
        CovidWindow(self)

    def _open_statistical_tests(self):
        StatisticalTestsWindow(self)

    def _open_roulette(self):
        RouletteWindow(self)

    def _show_about(self):
        messagebox.showinfo("Acerca del proyecto", "Sistema de simulación académico con login, registro, calculadora y simulación COVID.")

    def _logout(self):
        self.destroy()
        self.parent.deiconify()
        self.parent.password_entry.delete(0, "end")
        self.parent.username_entry.delete(0, "end")
        self.parent.status_var.set("")
