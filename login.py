from pathlib import Path

import tkinter

try:
    import customtkinter as ctk
except ModuleNotFoundError as exc:
    raise SystemExit("No se pudo importar customtkinter. Instala las dependencias con: pip install -r requirements.txt") from exc

from PIL import Image
from tkinter import messagebox

from database import authenticate_user, get_default_db_path
from register import RegisterWindow
from dashboard import DashboardApp


class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Sistema de Simulación")
        self.geometry("640x380")
        self.overrideredirect(True)
        self.configure(fg_color="#020617")
        self.resizable(False, False)
        self._center_window()

        self.logo_image = self._load_logo_image()
        self._build_ui()
        self._start_progress()

    def _load_logo_image(self):
        candidates = [
            Path(__file__).resolve().parent / "images" / "images.png",
            Path(__file__).resolve().parent / "assets" / "logo.png",
        ]
        for logo_path in candidates:
            if logo_path.exists():
                try:
                    image = Image.open(logo_path)
                    image = image.resize((120, 120))
                    return ctk.CTkImage(light_image=image, dark_image=image, size=(120, 120))
                except Exception:
                    continue
        return None

    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        if width == 1 and height == 1:
            width, height = 640, 380
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color="#0f172a", corner_radius=24)
        container.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(container, text="", image=self.logo_image, compound="top").pack(pady=(24, 10))
        ctk.CTkLabel(container, text="Sistema de Simulación", font=("Segoe UI", 24, "bold"), text_color="#f8fafc").pack()
        ctk.CTkLabel(container, text="Preparando el entorno de autenticación...", font=("Segoe UI", 13), text_color="#94a3b8").pack(pady=(6, 18))

        self.progress_bar = ctk.CTkProgressBar(container, width=320, height=10)
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(container, text="Cargando módulos...", font=("Segoe UI", 12), text_color="#cbd5e1")
        self.status_label.pack()

    def _start_progress(self):
        self._update_progress(0)

    def _update_progress(self, value):
        if value >= 1:
            self.after(200, self._open_login)
            return
        self.progress_bar.set(value)
        self.status_label.configure(text="Cargando módulos..." if value < 0.5 else "Listo. Abriendo inicio de sesión...")
        self.after(80, lambda: self._update_progress(value + 0.08))

    def _open_login(self):
        self.destroy()
        LoginApp().mainloop()


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Sistema de Simulación - Inicio de sesión")
        self.geometry("980x620")
        self.minsize(900, 600)
        self.configure(fg_color="#0f172a")

        self.db_path = get_default_db_path()
        self.logo_image = self._load_logo_image()
        self._build_ui()

    def _load_logo_image(self):
        candidates = [
            Path(__file__).resolve().parent / "images" / "images.png",
            Path(__file__).resolve().parent / "assets" / "logo.png",
        ]
        for logo_path in candidates:
            if logo_path.exists():
                try:
                    image = Image.open(logo_path)
                    image = image.resize((140, 140))
                    return ctk.CTkImage(light_image=image, dark_image=image, size=(140, 140))
                except Exception:
                    continue
        return None

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        left_panel = ctk.CTkFrame(self, fg_color="#111827", corner_radius=0)
        left_panel.grid(row=0, column=0, sticky="nsew")
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(0, weight=1)

        right_panel = ctk.CTkFrame(self, fg_color="#0f172a", corner_radius=0)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            left_panel,
            text="",
            image=self.logo_image,
            compound="top",
        ).place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(
            right_panel,
            text="Bienvenido al sistema",
            font=("Segoe UI", 24, "bold"),
            text_color="#f8fafc",
        )
        title.grid(row=0, column=0, padx=20, pady=(40, 5))

        subtitle = ctk.CTkLabel(
            right_panel,
            text="Inicia sesión para entrar al proyecto de simulación",
            font=("Segoe UI", 13),
            text_color="#cbd5e1",
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 25))

        self.username_entry = ctk.CTkEntry(right_panel, placeholder_text="Usuario", width=320, height=42)
        self.username_entry.grid(row=2, column=0, padx=20, pady=10)

        self.password_entry = ctk.CTkEntry(right_panel, placeholder_text="Contraseña", show="●", width=320, height=42)
        self.password_entry.grid(row=3, column=0, padx=20, pady=10)

        self.status_var = ctk.StringVar(value="")
        self.status_label = ctk.CTkLabel(right_panel, textvariable=self.status_var, font=("Segoe UI", 12), text_color="#fbbf24")
        self.status_label.grid(row=4, column=0, padx=20, pady=(4, 8))

        self.show_password_var = ctk.StringVar(value="off")
        self.show_password_toggle = ctk.CTkSwitch(
            right_panel,
            text="Mostrar contraseña",
            variable=self.show_password_var,
            onvalue="on",
            offvalue="off",
            command=self._toggle_password_visibility,
        )
        self.show_password_toggle.grid(row=5, column=0, padx=20, pady=(5, 20))

        login_button = ctk.CTkButton(right_panel, text="Iniciar sesión", width=320, height=42, command=self._handle_login)
        login_button.grid(row=6, column=0, padx=20, pady=8)

        register_button = ctk.CTkButton(right_panel, text="Registrarse", width=320, height=42, fg_color="#2563eb", hover_color="#1d4ed8", command=self._open_register)
        register_button.grid(row=7, column=0, padx=20, pady=8)

        exit_button = ctk.CTkButton(right_panel, text="Salir", width=320, height=42, fg_color="#ef4444", hover_color="#dc2626", command=self.destroy)
        exit_button.grid(row=8, column=0, padx=20, pady=8)

        right_panel.grid_rowconfigure(9, weight=1)

    def _toggle_password_visibility(self):
        if self.show_password_var.get() == "on":
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="●")

    def _handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username:
            self.status_var.set("Ingresa tu usuario para continuar.")
            return

        if not password:
            self.status_var.set("Ingresa tu contraseña para continuar.")
            return

        if len(password) < 4:
            self.status_var.set("La contraseña debe tener al menos 4 caracteres.")
            return

        if authenticate_user(username, password, db_path=self.db_path):
            self.status_var.set("Acceso correcto. Cargando panel...")
            self.withdraw()
            DashboardApp(self)
        else:
            self.status_var.set("Usuario o contraseña incorrectos.")
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")

    def _open_register(self):
        RegisterWindow(self)


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
