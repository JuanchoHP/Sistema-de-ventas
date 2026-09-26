import tkinter as tk

from config import COLOR_FONDO
from database import contar_tabla


class DashboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.crear_dashboard()

    def crear_tarjeta(self, parent, titulo, valor, color):
        card = tk.Frame(parent, bg=color, width=220, height=120)
        card.pack_propagate(False)

        tk.Label(card, text=titulo, bg=color, fg="white", font=("Segoe UI", 11, "bold")).pack(
            pady=(20, 5)
        )
        tk.Label(card, text=str(valor), bg=color, fg="white", font=("Segoe UI", 24, "bold")).pack()
        return card

    def crear_dashboard(self):
        titulo = tk.Label(
            self,
            text="DASHBOARD",
            bg=COLOR_FONDO,
            font=("Segoe UI", 18, "bold"),
        )
        titulo.pack(pady=20)

        tarjetas = tk.Frame(self, bg=COLOR_FONDO)
        tarjetas.pack(pady=15)

        p_tot = contar_tabla("productos")
        c_tot = contar_tabla("clientes")
        pr_tot = contar_tabla("proveedores")
        v_tot = contar_tabla("ventas")

        self.crear_tarjeta(tarjetas, "PRODUCTOS", p_tot, "#2563EB").pack(side="left", padx=10)
        self.crear_tarjeta(tarjetas, "CLIENTES", c_tot, "#16A34A").pack(side="left", padx=10)
        self.crear_tarjeta(tarjetas, "PROVEEDORES", pr_tot, "#EA580C").pack(side="left", padx=10)
        self.crear_tarjeta(tarjetas, "VENTAS", v_tot, "#7C3AED").pack(side="left", padx=10)

        mensaje = tk.Label(
            self,
            text="Bienvenido al ERP Empresarial",
            bg=COLOR_FONDO,
            fg="#1f2937",
            font=("Segoe UI", 16, "bold"),
        )
        mensaje.pack(pady=40)
