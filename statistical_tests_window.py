import customtkinter as ctk
from tkinter import messagebox

from statistical_tests import generate_and_test_sequence


class StatisticalTestsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Pruebas estadísticas")
        self.geometry("1080x760")
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

        ctk.CTkLabel(left, text="Pruebas estadísticas", font=("Segoe UI", 20, "bold"), text_color="#f8fafc").grid(row=0, column=0, padx=18, pady=(18, 6), sticky="w")
        ctk.CTkLabel(left, text="Reutiliza los generadores pseudoaleatorios para analizar secuencias", font=("Segoe UI", 12), text_color="#94a3b8").grid(row=1, column=0, padx=18, pady=(0, 10), sticky="w")

        self.method_var = ctk.StringVar(value="lineal")
        ctk.CTkOptionMenu(left, values=["lineal", "mixto", "multiplicativo", "cuadrado_medio", "fibonacci", "automata_celular"], variable=self.method_var, width=320, height=42).grid(row=2, column=0, padx=18, pady=8)

        self.seed_entry = ctk.CTkEntry(left, placeholder_text="Semilla", width=320, height=42)
        self.seed_entry.grid(row=3, column=0, padx=18, pady=8)
        self.seed_entry.insert(0, "1")

        self.a_entry = ctk.CTkEntry(left, placeholder_text="Parámetro a", width=320, height=42)
        self.a_entry.grid(row=4, column=0, padx=18, pady=8)

        self.c_entry = ctk.CTkEntry(left, placeholder_text="Parámetro c", width=320, height=42)
        self.c_entry.grid(row=5, column=0, padx=18, pady=8)

        self.m_entry = ctk.CTkEntry(left, placeholder_text="Parámetro m", width=320, height=42)
        self.m_entry.grid(row=6, column=0, padx=18, pady=8)

        self.count_entry = ctk.CTkEntry(left, placeholder_text="Cantidad de valores", width=320, height=42)
        self.count_entry.grid(row=7, column=0, padx=18, pady=8)
        self.count_entry.insert(0, "20")

        ctk.CTkButton(left, text="Ejecutar pruebas", width=320, height=42, command=self._run_tests).grid(row=8, column=0, padx=18, pady=(10, 8))
        ctk.CTkButton(left, text="Cerrar", width=320, height=42, fg_color="#64748b", hover_color="#475569", command=self.destroy).grid(row=9, column=0, padx=18, pady=8)

        ctk.CTkLabel(right, text="Resultados", font=("Segoe UI", 18, "bold"), text_color="#f8fafc").grid(row=0, column=0, padx=18, pady=(18, 10), sticky="w")
        self.result_box = ctk.CTkTextbox(right, fg_color="#0f172a", text_color="#f8fafc")
        self.result_box.grid(row=1, column=0, padx=18, pady=8, sticky="nsew")
        self.result_box.insert("end", "Aún no se ejecutan pruebas.\n")

    def _run_tests(self):
        try:
            method = self.method_var.get()
            seed = int(self.seed_entry.get()) if self.seed_entry.get().strip() else 1
            a = int(self.a_entry.get()) if self.a_entry.get().strip() else None
            c = int(self.c_entry.get()) if self.c_entry.get().strip() else None
            m = int(self.m_entry.get()) if self.m_entry.get().strip() else None
            count = int(self.count_entry.get()) if self.count_entry.get().strip() else 20
            result = generate_and_test_sequence(method=method, seed=seed, a=a, c=c, m=m, count=count)
            lines = []
            lines.append(f"Método: {method}")
            lines.append(f"Valores generados: {result['values']}")
            for report in result["reports"]:
                lines.append(f"- {report['name']}: {'Aprobada' if report['result']['pass'] else 'No aprobada'}")
                lines.append(f"  Resultado={report['metric']:.4f}; {report['result']['interpretation']}")
            self.result_box.delete("1.0", "end")
            self.result_box.insert("end", "\n".join(lines))
        except ValueError as exc:
            messagebox.showerror("Entrada inválida", str(exc))
