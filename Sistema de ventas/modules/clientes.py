import tkinter as tk
from tkinter import ttk, messagebox
from config import *
from database import conectar

class ClientesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.cliente_id = None
        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):
        titulo = tk.Label(self, text="GESTIÓN DE CLIENTES", bg=COLOR_FONDO, font=("Segoe UI", 18, "bold"))
        titulo.pack(pady=10)

        form = tk.LabelFrame(self, text="DATOS DEL CLIENTE", bg=COLOR_BLANCO, padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Nombre completo", bg=COLOR_BLANCO).grid(row=0, column=0, sticky="w")
        self.ent_nombre = tk.Entry(form, width=35)
        self.ent_nombre.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form, text="Documento", bg=COLOR_BLANCO).grid(row=0, column=1, sticky="w")
        self.ent_documento = tk.Entry(form, width=25)
        self.ent_documento.grid(row=1, column=1, padx=5, pady=5)

        # Botones de acción CRUD
        barra = tk.Frame(self, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=10, pady=5)

        tk.Button(barra, text="Guardar", bg="#16A34A", fg="white", command=self.guardar_cliente).pack(side="left", padx=5)
        tk.Button(barra, text="Actualizar", bg="#2563EB", fg="white", command=self.actualizar_cliente).pack(side="left", padx=5)
        tk.Button(barra, text="Eliminar", bg="#DC2626", fg="white", command=self.eliminar_cliente).pack(side="left", padx=5)

    def guardar_cliente(self):
        nombre = self.ent_nombre.get().strip()
        documento = self.ent_documento.get().strip()
        if not nombre or not documento:
            messagebox.showwarning("Validación", "Nombre y documento obligatorios.")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (nombre, documento) VALUES (?, ?)", (nombre, documento))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente guardado.")
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_clientes(self):
        if not hasattr(self, "tree_clientes"):
            self.tree_clientes = ttk.Treeview(self, columns=("id", "nombre", "documento"), show="headings")
            self.tree_clientes.heading("id", text="ID")
            self.tree_clientes.heading("nombre", text="NOMBRE")
            self.tree_clientes.heading("documento", text="DOCUMENTO")
            self.tree_clientes.pack(fill="both", expand=True, padx=10, pady=10)