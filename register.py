import customtkinter as ctk
from tkinter import messagebox

from database import create_tables, register_user


class RegisterWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Crear cuenta")
        self.geometry("480x640")
        self.configure(fg_color="#111827")
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Registro de usuario",
            font=("Segoe UI", 22, "bold"),
            text_color="#f8fafc",
        ).grid(row=0, column=0, padx=20, pady=(24, 8))

        self.full_name_entry = ctk.CTkEntry(self, placeholder_text="Nombre completo", width=320, height=42)
        self.full_name_entry.grid(row=1, column=0, padx=20, pady=8)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Usuario", width=320, height=42)
        self.username_entry.grid(row=2, column=0, padx=20, pady=8)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Correo electrónico (opcional)", width=320, height=42)
        self.email_entry.grid(row=3, column=0, padx=20, pady=8)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="●", width=320, height=42)
        self.password_entry.grid(row=4, column=0, padx=20, pady=8)

        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text="Confirmar contraseña", show="●", width=320, height=42)
        self.confirm_password_entry.grid(row=5, column=0, padx=20, pady=8)

        create_button = ctk.CTkButton(self, text="Crear cuenta", width=320, height=42, command=self._handle_register)
        create_button.grid(row=6, column=0, padx=20, pady=(16, 8))

        close_button = ctk.CTkButton(self, text="Cancelar", width=320, height=42, fg_color="#64748b", hover_color="#475569", command=self.destroy)
        close_button.grid(row=7, column=0, padx=20, pady=8)

    def _handle_register(self):
        full_name = self.full_name_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not full_name or not username or not password or not confirm_password:
            messagebox.showwarning("Campos incompletos", "Completa todos los campos obligatorios.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        create_tables()
        success = register_user(full_name, username, email, password)
        if success:
            messagebox.showinfo("Éxito", "Cuenta creada correctamente.")
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear la cuenta. El usuario ya existe o los datos son inválidos.")
