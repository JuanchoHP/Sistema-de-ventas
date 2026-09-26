import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import conectar
from config import *

class ProveedoresFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.proveedor_id = None
        self.crear_interfaz()
        self.cargar_proveedores()

    # ==========================================
    # INTERFAZ
    # ==========================================
    def crear_interfaz(self):
        titulo = tk.Label(
            self,
            text="GESTIÓN DE PROVEEDORES",
            font=("Segoe UI", 18, "bold"),
            bg=COLOR_FONDO
        )
        titulo.pack(pady=10)

        form = tk.LabelFrame(
            self,
            text="DATOS DEL PROVEEDOR",
            bg=COLOR_BLANCO,
            padx=10,
            pady=10
        )
        form.pack(fill="x", padx=10, pady=10)

        # Razón Social
        tk.Label(form, text="Razón Social", bg=COLOR_BLANCO).grid(row=0, column=0, sticky="w")
        self.ent_nombre = tk.Entry(form, width=40)
        self.ent_nombre.grid(row=1, column=0, padx=5, pady=5)

        # NIT
        tk.Label(form, text="NIT", bg=COLOR_BLANCO).grid(row=0, column=1, sticky="w")
        self.ent_nit = tk.Entry(form, width=20)
        self.ent_nit.grid(row=1, column=1, padx=5, pady=5)

        # Teléfono
        tk.Label(form, text="Teléfono", bg=COLOR_BLANCO).grid(row=0, column=2, sticky="w")
        self.ent_telefono = tk.Entry(form, width=20)
        self.ent_telefono.grid(row=1, column=2, padx=5, pady=5)

        # Dirección
        tk.Label(form, text="Dirección", bg=COLOR_BLANCO).grid(row=2, column=0, sticky="w")
        self.ent_direccion = tk.Entry(form, width=50)
        self.ent_direccion.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Botones de Acción
        barra = tk.Frame(self, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=10)

        tk.Button(barra, text="Guardar", bg="#16A34A", fg="white", command=self.guardar_proveedor).pack(side="left", padx=5)
        tk.Button(barra, text="Actualizar", bg="#2563EB", fg="white", command=self.actualizar_proveedor).pack(side="left", padx=5)
        tk.Button(barra, text="Eliminar", bg="#DC2626", fg="white", command=self.eliminar_proveedor).pack(side="left", padx=5)
        tk.Button(barra, text="Limpiar", bg="#EA580C", fg="white", command=self.limpiar_formulario).pack(side="left", padx=5)

        # Buscador
        frame_busqueda = tk.Frame(self, bg=COLOR_FONDO)
        frame_busqueda.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_busqueda, text="Buscar:", bg=COLOR_FONDO).pack(side="left")
        self.ent_buscar = tk.Entry(frame_busqueda, width=40)
        self.ent_buscar.pack(side="left", padx=5)
        tk.Button(frame_busqueda, text="Buscar", command=self.buscar_proveedor).pack(side="left")

        # Treeview (Tabla)
        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=10, pady=10)

        columnas = ("id", "nombre", "nit", "telefono", "direccion")
        self.tree = ttk.Treeview(frame_tree, columns=columnas, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="RAZÓN SOCIAL")
        self.tree.heading("nit", text="NIT")
        self.tree.heading("telefono", text="TELÉFONO")
        self.tree.heading("direccion", text="DIRECCIÓN")

        self.tree.column("id", width=60)
        self.tree.column("nombre", width=250)
        self.tree.column("nit", width=150)
        self.tree.column("telefono", width=150)
        self.tree.column("direccion", width=250)

        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)

    # ==========================================
    # CRUD Y FUNCIONES
    # ==========================================
    def guardar_proveedor(self):
        nombre = self.ent_nombre.get().strip()
        nit = self.ent_nit.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "La razón social es obligatoria.")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO proveedores (nombre, nit, telefono, direccion) VALUES (?, ?, ?, ?)",
            (nombre, nit, self.ent_telefono.get().strip(), self.ent_direccion.get().strip())
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Proveedor registrado correctamente")
        self.cargar_proveedores()
        self.limpiar_formulario()

    def actualizar_proveedor(self):
        if not self.proveedor_id:
            messagebox.showwarning("Selección", "Seleccione un proveedor de la tabla.")
            return
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE proveedores SET nombre=?, nit=?, telefono=?, direccion=? WHERE id=?",
            (self.ent_nombre.get().strip(), self.ent_nit.get().strip(), self.ent_telefono.get().strip(), self.ent_direccion.get().strip(), self.proveedor_id)
        )
        conn.commit()
        conn.close()
        self.cargar_proveedores()
        messagebox.showinfo("Actualizado", "Proveedor actualizado correctamente")

    def eliminar_proveedor(self):
        if not self.proveedor_id:
            messagebox.showwarning("Selección", "Seleccione un proveedor de la tabla.")
            return
        
        if not messagebox.askyesno("Confirmar", "¿Desea eliminar el proveedor?"):
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM proveedores WHERE id=?", (self.proveedor_id,))
        conn.commit()
        conn.close()
        self.cargar_proveedores()
        self.limpiar_formulario()

    def cargar_proveedores(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proveedores ORDER BY nombre")
        datos = cursor.fetchall()
        conn.close()

        for fila in datos:
            self.tree.insert("", tk.END, values=fila)

    def buscar_proveedor(self):
        texto = self.ent_buscar.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM proveedores WHERE nombre LIKE ? OR nit LIKE ?",
            (f"%{texto}%", f"%{texto}%")
        )
        resultados = cursor.fetchall()
        conn.close()

        for fila in resultados:
            self.tree.insert("", tk.END, values=fila)

    def seleccionar_proveedor(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        datos = self.tree.item(seleccion[0])["values"]
        self.proveedor_id = datos[0]
        self.limpiar_formulario(reset_id=False)
        self.ent_nombre.insert(0, datos[1])
        self.ent_nit.insert(0, datos[2])
        self.ent_telefono.insert(0, datos[3])
        self.ent_direccion.insert(0, datos[4])

    def limpiar_formulario(self, reset_id=True):
        self.ent_nombre.delete(0, tk.END)
        self.ent_nit.delete(0, tk.END)
        self.ent_telefono.delete(0, tk.END)
        self.ent_direccion.delete(0, tk.END)
        if reset_id:
            self.proveedor_id = None