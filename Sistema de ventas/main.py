import tkinter as tk
from tkinter import ttk, messagebox

from config import APP_NAME, COLOR_FONDO, COLOR_SECUNDARIO, EMPRESA, NIT
from database import (
    actualizar_cliente,
    actualizar_cuenta,
    actualizar_producto,
    actualizar_proveedor,
    actualizar_venta,
    buscar_cliente_por_documento,
    buscar_producto,
    buscar_proveedor_por_nit,
    contar_tabla,
    crear_tablas,
    eliminar_cliente,
    eliminar_cuenta,
    eliminar_producto,
    eliminar_proveedor,
    eliminar_venta,
    guardar_cliente,
    guardar_cuenta,
    guardar_producto,
    guardar_proveedor,
    guardar_venta,
    listar_clientes,
    listar_cuentas,
    listar_productos,
    listar_proveedores,
    listar_ventas,
    reporte_general,
)


class DashboardView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.pack(fill="both", expand=True)
        self.crear_dashboard()

    def crear_tarjeta(self, parent, titulo, valor, color):
        card = tk.Frame(parent, bg=color, width=220, height=120)
        card.pack_propagate(False)
        tk.Label(card, text=titulo, bg=color, fg="white", font=("Segoe UI", 11, "bold")).pack(pady=(20, 5))
        tk.Label(card, text=str(valor), bg=color, fg="white", font=("Segoe UI", 24, "bold")).pack()
        return card

    def crear_dashboard(self):
        tk.Label(self, text="DASHBOARD", bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 26, "bold")).pack(pady=(20, 10))

        tarjetas = tk.Frame(self, bg=COLOR_FONDO)
        tarjetas.pack(pady=15)

        report = reporte_general()
        self.crear_tarjeta(tarjetas, "PRODUCTOS", report["productos"], "#2563EB").pack(side="left", padx=10)
        self.crear_tarjeta(tarjetas, "CLIENTES", report["clientes"], "#16A34A").pack(side="left", padx=10)
        self.crear_tarjeta(tarjetas, "PROVEEDORES", report["proveedores"], "#EA580C").pack(side="left", padx=10)
        self.crear_tarjeta(tarjetas, "VENTAS", report["ventas"], "#7C3AED").pack(side="left", padx=10)

        tk.Label(self, text="Bienvenido al ERP Empresarial", bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 15, "bold")).pack(pady=40)


class InventarioView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.pack(fill="both", expand=True)
        self.campos = {}
        self.construir()
        self.cargar_tabla()

    def construir(self):
        tk.Label(self, text="GESTIÓN DE INVENTARIO", bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 26, "bold")).pack(pady=(20, 10))
        panel = tk.Frame(self, bg=COLOR_FONDO)
        panel.pack(fill="x", padx=20)
        tk.Label(panel, text="DATOS DEL PRODUCTO", bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))

        fila1 = tk.Frame(panel, bg=COLOR_FONDO)
        fila1.pack(fill="x", pady=5)
        self.campos["codigo"] = self.crear_input(fila1, "Código", 20)
        self.campos["nombre"] = self.crear_input(fila1, "Nombre", 35, padx=(30, 0))
        self.campos["precio"] = self.crear_input(fila1, "Precio", 18, padx=(30, 0))
        self.campos["stock"] = self.crear_input(fila1, "Stock", 18, padx=(30, 0))

        acciones = tk.Frame(self, bg=COLOR_FONDO)
        acciones.pack(fill="x", padx=20, pady=15)
        for texto, color, cmd in [
            ("Guardar", "#2ecc71", self.guardar),
            ("Actualizar", "#3b82f6", self.actualizar),
            ("Eliminar", "#dc2626", self.eliminar),
            ("Limpiar", "#d1d5db", self.limpiar),
        ]:
            tk.Button(acciones, text=texto, bg=color, fg="white" if color != "#d1d5db" else "#111827", font=("Segoe UI", 10, "bold"), width=12, command=cmd).pack(side="left", padx=5)

        busqueda = tk.Frame(self, bg=COLOR_FONDO)
        busqueda.pack(fill="x", padx=20, pady=(0, 10))
        tk.Label(busqueda, text="Buscar:", bg=COLOR_FONDO, font=("Segoe UI", 10, "bold")).pack(side="left")
        entry = tk.Entry(busqueda, width=25, font=("Segoe UI", 10))
        entry.pack(side="left", padx=10)
        entry.bind("<KeyRelease>", self.buscar)

        tabla_frame = tk.Frame(self, bg="#f1f5f9")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        columnas = ("codigo", "nombre", "precio", "stock")
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        for col, titulo in [("codigo", "Código"), ("nombre", "Nombre"), ("precio", "Precio"), ("stock", "Stock")]:
            self.tree.heading(col, text=titulo)
        self.tree.column("codigo", width=120, anchor="center")
        self.tree.column("nombre", width=260)
        self.tree.column("precio", width=130, anchor="center")
        self.tree.column("stock", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.cargar_producto_seleccionado)

    def crear_input(self, parent, texto, width, padx=(0, 0)):
        frame = tk.Frame(parent, bg=COLOR_FONDO)
        frame.pack(side="left", padx=padx)
        tk.Label(frame, text=texto, bg=COLOR_FONDO, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        entry = tk.Entry(frame, width=width, font=("Segoe UI", 10))
        entry.pack(pady=4)
        return entry

    def limpiar(self):
        for campo in self.campos.values():
            campo.delete(0, tk.END)

    def guardar(self):
        codigo = self.campos["codigo"].get().strip()
        nombre = self.campos["nombre"].get().strip()
        precio = self.campos["precio"].get().strip()
        stock = self.campos["stock"].get().strip()
        if not all([codigo, nombre, precio, stock]):
            messagebox.showwarning("Advertencia", "Debe completar todos los campos.")
            return
        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            messagebox.showwarning("Advertencia", "Precio debe ser numérico y stock debe ser entero.")
            return
        if buscar_producto(codigo):
            messagebox.showwarning("Advertencia", "Ese código ya existe.")
            return
        guardar_producto(codigo, nombre, precio, stock)
        self.cargar_tabla(); self.limpiar()

    def actualizar(self):
        codigo = self.campos["codigo"].get().strip()
        if not codigo:
            messagebox.showwarning("Advertencia", "Seleccione un producto para actualizar.")
            return
        nombre = self.campos["nombre"].get().strip(); precio = self.campos["precio"].get().strip(); stock = self.campos["stock"].get().strip()
        try:
            precio = float(precio); stock = int(stock)
        except ValueError:
            messagebox.showwarning("Advertencia", "Precio y stock deben ser válidos.")
            return
        actualizar_producto(codigo, nombre, precio, stock)
        self.cargar_tabla(); self.limpiar()

    def eliminar(self):
        codigo = self.campos["codigo"].get().strip()
        if not codigo:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar.")
            return
        if messagebox.askyesno("Confirmar", f"¿Desea eliminar el producto {codigo}?"):
            eliminar_producto(codigo)
            self.cargar_tabla(); self.limpiar()

    def cargar_tabla(self, filtro=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for producto in listar_productos(filtro):
            self.tree.insert("", tk.END, values=(producto["codigo"], producto["nombre"], producto["precio"], producto["stock"]))

    def buscar(self, event):
        self.cargar_tabla(event.widget.get().strip())

    def cargar_producto_seleccionado(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        if not values: return
        codigo, nombre, precio, stock = values
        self.campos["codigo"].delete(0, tk.END); self.campos["codigo"].insert(0, codigo)
        self.campos["nombre"].delete(0, tk.END); self.campos["nombre"].insert(0, nombre)
        self.campos["precio"].delete(0, tk.END); self.campos["precio"].insert(0, precio)
        self.campos["stock"].delete(0, tk.END); self.campos["stock"].insert(0, stock)


class ClientesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.pack(fill="both", expand=True)
        self.campos = {}
        self.selected_id = None
        self.construir(); self.cargar_tabla()

    def crear_input(self, parent, texto, width, padx=(0, 0)):
        frame = tk.Frame(parent, bg=COLOR_FONDO)
        frame.pack(side="left", padx=padx)
        tk.Label(frame, text=texto, bg=COLOR_FONDO, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        entry = tk.Entry(frame, width=width, font=("Segoe UI", 10))
        entry.pack(pady=4)
        return entry

    def crear_combo(self, parent, texto, opciones, padx=(0, 0)):
        frame = tk.Frame(parent, bg=COLOR_FONDO)
        frame.pack(side="left", padx=padx)
        tk.Label(frame, text=texto, bg=COLOR_FONDO, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        combo = ttk.Combobox(frame, values=opciones, width=20, state="readonly")
        combo.pack(pady=4)
        return combo

    def construir(self):
        tk.Label(self, text="GESTIÓN DE CLIENTES", bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 26, "bold")).pack(pady=(20, 10))
        panel = tk.Frame(self, bg=COLOR_FONDO); panel.pack(fill="x", padx=20)
        tk.Label(panel, text="DATOS DEL CLIENTE", bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))
        fila1 = tk.Frame(panel, bg=COLOR_FONDO); fila1.pack(fill="x", pady=5)
        self.campos["nombre"] = self.crear_input(fila1, "Nombre completo", 32)
        self.campos["tipo_documento"] = self.crear_combo(fila1, "Tipo de documento", ["Cédula de Ciudadanía", "Tarjeta de Identidad", "Cédula de Extranjería", "Permiso Especial"])
        self.campos["documento"] = self.crear_input(fila1, "Número de documento", 20, padx=(30, 0))
        self.campos["sexo"] = self.crear_combo(fila1, "Sexo", ["Masculino", "Femenino"], padx=(30, 0))
        fila2 = tk.Frame(panel, bg=COLOR_FONDO); fila2.pack(fill="x", pady=5)
        self.campos["telefono"] = self.crear_input(fila2, "Teléfono", 24)
        self.campos["direccion"] = self.crear_input(fila2, "Dirección", 30, padx=(30, 0))
        self.campos["email"] = self.crear_input(fila2, "Email", 28, padx=(30, 0))

        acciones = tk.Frame(self, bg=COLOR_FONDO); acciones.pack(fill="x", padx=20, pady=15)
        for texto, color, cmd in [("Guardar", "#2ecc71", self.guardar), ("Actualizar", "#3b82f6", self.actualizar), ("Eliminar", "#dc2626", self.eliminar), ("Limpiar", "#d1d5db", self.limpiar)]:
            tk.Button(acciones, text=texto, bg=color, fg="white" if color != "#d1d5db" else "#111827", font=("Segoe UI", 10, "bold"), width=12, command=cmd).pack(side="left", padx=5)

        busqueda = tk.Frame(self, bg=COLOR_FONDO); busqueda.pack(fill="x", padx=20, pady=(0, 10))
        tk.Label(busqueda, text="Buscar:", bg=COLOR_FONDO, font=("Segoe UI", 10, "bold")).pack(side="left")
        entry = tk.Entry(busqueda, width=25, font=("Segoe UI", 10)); entry.pack(side="left", padx=10)
        entry.bind("<KeyRelease>", self.buscar)

        tabla_frame = tk.Frame(self, bg="#f1f5f9"); tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        columnas = ("id", "nombre", "tipo_documento", "documento", "sexo", "telefono", "direccion", "email")
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        for col, titulo in [("id", "ID"), ("nombre", "Nombre"), ("tipo_documento", "Tipo documento"), ("documento", "Documento"), ("sexo", "Sexo"), ("telefono", "Teléfono"), ("direccion", "Dirección"), ("email", "Email")]:
            self.tree.heading(col, text=titulo)
        self.tree.column("nombre", width=200); self.tree.column("direccion", width=160); self.tree.column("email", width=180)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.cargar_cliente_seleccionado)

    def limpiar(self):
        for campo in self.campos.values():
            if isinstance(campo, ttk.Combobox): campo.set("")
            else: campo.delete(0, tk.END)
        self.selected_id = None

    def guardar(self):
        nombre = self.campos["nombre"].get().strip(); tipo_documento = self.campos["tipo_documento"].get().strip(); documento = self.campos["documento"].get().strip(); sexo = self.campos["sexo"].get().strip(); telefono = self.campos["telefono"].get().strip(); direccion = self.campos["direccion"].get().strip(); email = self.campos["email"].get().strip()
        if not all([nombre, tipo_documento, documento, sexo, telefono, direccion, email]):
            messagebox.showwarning("Advertencia", "Complete todos los campos del cliente."); return
        if buscar_cliente_por_documento(documento):
            messagebox.showwarning("Advertencia", "El documento ya existe."); return
        guardar_cliente(nombre, tipo_documento, documento, sexo, telefono, direccion, email)
        self.cargar_tabla(); self.limpiar()

    def actualizar(self):
        if not self.selected_id:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para actualizar."); return
        nombre = self.campos["nombre"].get().strip(); tipo_documento = self.campos["tipo_documento"].get().strip(); documento = self.campos["documento"].get().strip(); sexo = self.campos["sexo"].get().strip(); telefono = self.campos["telefono"].get().strip(); direccion = self.campos["direccion"].get().strip(); email = self.campos["email"].get().strip()
        actualizar_cliente(self.selected_id, nombre, tipo_documento, documento, sexo, telefono, direccion, email)
        self.cargar_tabla(); self.limpiar()

    def eliminar(self):
        if not self.selected_id:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar."); return
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este cliente?"):
            eliminar_cliente(self.selected_id)
            self.cargar_tabla(); self.limpiar()

    def cargar_tabla(self, filtro=""):
        for item in self.tree.get_children(): self.tree.delete(item)
        for cliente in listar_clientes(filtro):
            self.tree.insert("", tk.END, values=(cliente["id"], cliente["nombre"], cliente["tipo_documento"], cliente["documento"], cliente["sexo"], cliente["telefono"], cliente["direccion"], cliente["email"]))

    def buscar(self, event):
        self.cargar_tabla(event.widget.get().strip())

    def cargar_cliente_seleccionado(self, event):
        item = self.tree.selection()[0]; values = self.tree.item(item, "values")
        if not values: return
        self.selected_id = values[0]
        self.campos["nombre"].delete(0, tk.END); self.campos["nombre"].insert(0, values[1])
        self.campos["tipo_documento"].set(values[2])
        self.campos["documento"].delete(0, tk.END); self.campos["documento"].insert(0, values[3])
        self.campos["sexo"].set(values[4])
        self.campos["telefono"].delete(0, tk.END); self.campos["telefono"].insert(0, values[5])
        self.campos["direccion"].delete(0, tk.END); self.campos["direccion"].insert(0, values[6])
        self.campos["email"].delete(0, tk.END); self.campos["email"].insert(0, values[7])


class ProveedoresView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.pack(fill="both", expand=True)
        self.campos = {}; self.selected_id=None; self.construir(); self.cargar_tabla()

    def crear_input(self, parent, texto, width, padx=(0,0)):
        frame = tk.Frame(parent, bg=COLOR_FONDO); frame.pack(side="left", padx=padx)
        tk.Label(frame, text=texto, bg=COLOR_FONDO, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        entry = tk.Entry(frame, width=width, font=("Segoe UI", 10)); entry.pack(pady=4)
        return entry

    def construir(self):
        tk.Label(self, text="GESTIÓN DE PROVEEDORES", bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 26, "bold")).pack(pady=(20,10))
        panel = tk.Frame(self, bg=COLOR_FONDO); panel.pack(fill="x", padx=20)
        tk.Label(panel, text="DATOS DEL PROVEEDOR", bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,10))
        fila = tk.Frame(panel, bg=COLOR_FONDO); fila.pack(fill="x", pady=5)
        self.campos["nombre"] = self.crear_input(fila, "Nombre", 32)
        self.campos["nit"] = self.crear_input(fila, "NIT", 20, padx=(30,0))
        self.campos["telefono"] = self.crear_input(fila, "Teléfono", 20, padx=(30,0))
        self.campos["direccion"] = self.crear_input(fila, "Dirección", 35, padx=(30,0))

        acciones = tk.Frame(self, bg=COLOR_FONDO); acciones.pack(fill="x", padx=20, pady=15)
        for texto, color, cmd in [("Guardar", "#2ecc71", self.guardar), ("Actualizar", "#3b82f6", self.actualizar), ("Eliminar", "#dc2626", self.eliminar), ("Limpiar", "#d1d5db", self.limpiar)]:
            tk.Button(acciones, text=texto, bg=color, fg="white" if color != "#d1d5db" else "#111827", font=("Segoe UI", 10, "bold"), width=12, command=cmd).pack(side="left", padx=5)

        busqueda = tk.Frame(self, bg=COLOR_FONDO); busqueda.pack(fill="x", padx=20, pady=(0,10))
        tk.Label(busqueda, text="Buscar:", bg=COLOR_FONDO, font=("Segoe UI", 10, "bold")).pack(side="left")
        entry = tk.Entry(busqueda, width=25, font=("Segoe UI", 10)); entry.pack(side="left", padx=10)
        entry.bind("<KeyRelease>", self.buscar)

        tabla_frame = tk.Frame(self, bg="#f1f5f9"); tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
        self.tree = ttk.Treeview(tabla_frame, columns=("id", "nombre", "nit", "telefono", "direccion"), show="headings", height=12)
        for col, titulo in [("id", "ID"), ("nombre", "Nombre"), ("nit", "NIT"), ("telefono", "Teléfono"), ("direccion", "Dirección")]:
            self.tree.heading(col, text=titulo)
        self.tree.column("nombre", width=230); self.tree.column("direccion", width=250)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.cargar_proveedor_seleccionado)

    def limpiar(self):
        for campo in self.campos.values(): campo.delete(0, tk.END)
        self.selected_id = None

    def guardar(self):
        nombre = self.campos["nombre"].get().strip(); nit = self.campos["nit"].get().strip(); telefono = self.campos["telefono"].get().strip(); direccion = self.campos["direccion"].get().strip()
        if not all([nombre, nit, telefono, direccion]):
            messagebox.showwarning("Advertencia", "Complete todos los campos del proveedor."); return
        if buscar_proveedor_por_nit(nit):
            messagebox.showwarning("Advertencia", "Ese NIT ya existe."); return
        guardar_proveedor(nombre, nit, telefono, direccion)
        self.cargar_tabla(); self.limpiar()

    def actualizar(self):
        if not self.selected_id:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para actualizar."); return
        nombre = self.campos["nombre"].get().strip(); nit = self.campos["nit"].get().strip(); telefono = self.campos["telefono"].get().strip(); direccion = self.campos["direccion"].get().strip()
        actualizar_proveedor(self.selected_id, nombre, nit, telefono, direccion)
        self.cargar_tabla(); self.limpiar()

    def eliminar(self):
        if not self.selected_id:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para eliminar."); return
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este proveedor?"):
            eliminar_proveedor(self.selected_id); self.cargar_tabla(); self.limpiar()

    def cargar_tabla(self, filtro=""):
        for item in self.tree.get_children(): self.tree.delete(item)
        for prov in listar_proveedores(filtro):
            self.tree.insert("", tk.END, values=(prov["id"], prov["nombre"], prov["nit"], prov["telefono"], prov["direccion"]))

    def buscar(self, event):
        self.cargar_tabla(event.widget.get().strip())

    def cargar_proveedor_seleccionado(self, event):
        item = self.tree.selection()[0]; values = self.tree.item(item, "values")
        if not values: return
        self.selected_id = values[0]
        self.campos["nombre"].delete(0, tk.END); self.campos["nombre"].insert(0, values[1])
        self.campos["nit"].delete(0, tk.END); self.campos["nit"].insert(0, values[2])
        self.campos["telefono"].delete(0, tk.END); self.campos["telefono"].insert(0, values[3])
        self.campos["direccion"].delete(0, tk.END); self.campos["direccion"].insert(0, values[4])


class VentasView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO); self.pack(fill="both", expand=True)
        self.campos = {}; self.selected_id=None; self.construir(); self.cargar_tabla()

    def crear_input(self,parent,texto,width,padx=(0,0)):
        frame = tk.Frame(parent, bg=COLOR_FONDO); frame.pack(side="left", padx=padx)
        tk.Label(frame, text=texto, bg=COLOR_FONDO, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        entry = tk.Entry(frame, width=width, font=("Segoe UI", 10)); entry.pack(pady=4)
        return entry

    def construir(self):
        tk.Label(self, text="GESTIÓN DE VENTAS", bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 26, "bold")).pack(pady=(20,10))
        panel = tk.Frame(self, bg=COLOR_FONDO); panel.pack(fill="x", padx=20)
        tk.Label(panel, text="DATOS DE LA VENTA", bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,10))
        fila1 = tk.Frame(panel, bg=COLOR_FONDO); fila1.pack(fill="x", pady=5)
        self.campos["numero_venta"] = self.crear_input(fila1, "Número de venta", 18)
        self.campos["fecha"] = self.crear_input(fila1, "Fecha", 18, padx=(30,0))
        self.campos["vendedor"] = self.crear_input(fila1, "Vendedor", 22, padx=(30,0))
        self.campos["metodo_pago"] = self.crear_input(fila1, "Método de pago", 20, padx=(30,0))
        fila2 = tk.Frame(panel, bg=COLOR_FONDO); fila2.pack(fill="x", pady=5)
        self.campos["subtotal"] = self.crear_input(fila2, "Subtotal", 18)
        self.campos["descuento"] = self.crear_input(fila2, "Descuento", 18, padx=(30,0))
        self.campos["iva"] = self.crear_input(fila2, "IVA", 18, padx=(30,0))
        self.campos["total"] = self.crear_input(fila2, "Total", 18, padx=(30,0))

        acciones = tk.Frame(self, bg=COLOR_FONDO); acciones.pack(fill="x", padx=20, pady=15)
        for texto,color,cmd in [("Guardar", "#2ecc71", self.guardar), ("Actualizar", "#3b82f6", self.actualizar), ("Eliminar", "#dc2626", self.eliminar), ("Limpiar", "#d1d5db", self.limpiar)]:
            tk.Button(acciones, text=texto, bg=color, fg="white" if color != "#d1d5db" else "#111827", font=("Segoe UI", 10, "bold"), width=12, command=cmd).pack(side="left", padx=5)

        busqueda = tk.Frame(self, bg=COLOR_FONDO); busqueda.pack(fill="x", padx=20, pady=(0,10))
        tk.Label(busqueda, text="Buscar:", bg=COLOR_FONDO, font=("Segoe UI", 10, "bold")).pack(side="left")
        entry = tk.Entry(busqueda, width=25, font=("Segoe UI", 10)); entry.pack(side="left", padx=10)
        entry.bind("<KeyRelease>", self.buscar)

        tabla_frame = tk.Frame(self, bg="#f1f5f9"); tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
        self.tree = ttk.Treeview(tabla_frame, columns=("id","numero_venta","fecha","vendedor","subtotal","descuento","iva","total","metodo_pago"), show="headings", height=12)
        for col, titulo in [("id","ID"),("numero_venta","Venta"),("fecha","Fecha"),("vendedor","Vendedor"),("subtotal","Subtotal"),("descuento","Descuento"),("iva","IVA"),("total","Total"),("metodo_pago","Pago")]:
            self.tree.heading(col, text=titulo)
        self.tree.column("numero_venta", width=120); self.tree.column("vendedor", width=140); self.tree.column("fecha", width=100); self.tree.column("total", width=100)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.cargar_venta_seleccionada)

    def limpiar(self):
        for campo in self.campos.values(): campo.delete(0, tk.END); self.selected_id=None

    def guardar(self):
        numero_venta = self.campos["numero_venta"].get().strip(); fecha = self.campos["fecha"].get().strip(); vendedor = self.campos["vendedor"].get().strip(); metodo_pago = self.campos["metodo_pago"].get().strip(); subtotal = self.campos["subtotal"].get().strip(); descuento = self.campos["descuento"].get().strip(); iva = self.campos["iva"].get().strip(); total = self.campos["total"].get().strip()
        if not all([numero_venta, fecha, vendedor, metodo_pago, subtotal, descuento, iva, total]):
            messagebox.showwarning("Advertencia", "Complete todos los campos de la venta."); return
        try:
            subtotal=float(subtotal); descuento=float(descuento); iva=float(iva); total=float(total)
        except ValueError:
            messagebox.showwarning("Advertencia", "Los valores numéricos deben ser válidos."); return
        guardar_venta(numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago)
        self.cargar_tabla(); self.limpiar()

    def actualizar(self):
        if not self.selected_id:
            messagebox.showwarning("Advertencia", "Seleccione una venta para actualizar."); return
        numero_venta = self.campos["numero_venta"].get().strip(); fecha = self.campos["fecha"].get().strip(); vendedor = self.campos["vendedor"].get().strip(); metodo_pago = self.campos["metodo_pago"].get().strip(); subtotal = self.campos["subtotal"].get().strip(); descuento = self.campos["descuento"].get().strip(); iva = self.campos["iva"].get().strip(); total = self.campos["total"].get().strip()
        try:
            subtotal=float(subtotal); descuento=float(descuento); iva=float(iva); total=float(total)
        except ValueError:
            messagebox.showwarning("Advertencia", "Los valores numéricos deben ser válidos."); return
        actualizar_venta(self.selected_id, numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago)
        self.cargar_tabla(); self.limpiar()

    def eliminar(self):
        if not self.selected_id:
            messagebox.showwarning("Advertencia", "Seleccione una venta para eliminar."); return
        if messagebox.askyesno("Confirmar", "¿Desea eliminar esta venta?"):
            eliminar_venta(self.selected_id); self.cargar_tabla(); self.limpiar()

    def cargar_tabla(self, filtro=""):
        for item in self.tree.get_children(): self.tree.delete(item)
        for venta in listar_ventas(filtro):
            self.tree.insert("", tk.END, values=(venta["id"], venta["numero_venta"], venta["fecha"], venta["vendedor"], venta["subtotal"], venta["descuento"], venta["iva"], venta["total"], venta["metodo_pago"]))

    def buscar(self, event):
        self.cargar_tabla(event.widget.get().strip())

    def cargar_venta_seleccionada(self, event):
        item = self.tree.selection()[0]; values = self.tree.item(item, "values")
        if not values: return
        self.selected_id = values[0]
        self.campos["numero_venta"].delete(0, tk.END); self.campos["numero_venta"].insert(0, values[1])
        self.campos["fecha"].delete(0, tk.END); self.campos["fecha"].insert(0, values[2])
        self.campos["vendedor"].delete(0, tk.END); self.campos["vendedor"].insert(0, values[3])
        self.campos["subtotal"].delete(0, tk.END); self.campos["subtotal"].insert(0, values[4])
        self.campos["descuento"].delete(0, tk.END); self.campos["descuento"].insert(0, values[5])
        self.campos["iva"].delete(0, tk.END); self.campos["iva"].insert(0, values[6])
        self.campos["total"].delete(0, tk.END); self.campos["total"].insert(0, values[7])
        self.campos["metodo_pago"].delete(0, tk.END); self.campos["metodo_pago"].insert(0, values[8])


class CuentaViewBase(tk.Frame):
    def __init__(self, parent, titulo, nombre_campo, tipo):
        super().__init__(parent, bg=COLOR_FONDO); self.pack(fill="both", expand=True)
        self.tipo = tipo; self.campos={}; self.selected_id=None; self.titulo=titulo; self.nombre_campo=nombre_campo
        self.construir(); self.cargar_tabla()

    def crear_input(self,parent,texto,width,padx=(0,0)):
        frame = tk.Frame(parent, bg=COLOR_FONDO); frame.pack(side="left", padx=padx)
        tk.Label(frame, text=texto, bg=COLOR_FONDO, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        entry = tk.Entry(frame, width=width, font=("Segoe UI", 10)); entry.pack(pady=4)
        return entry

    def construir(self):
        tk.Label(self, text=self.titulo, bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 26, "bold")).pack(pady=(20, 10))
        panel = tk.Frame(self, bg=COLOR_FONDO); panel.pack(fill="x", padx=20)
        tk.Label(panel, text="INFORMACIÓN", bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,10))
        fila = tk.Frame(panel, bg=COLOR_FONDO); fila.pack(fill="x", pady=5)
        self.campos[self.nombre_campo] = self.crear_input(fila, self.nombre_campo.title(), 28)
        self.campos["valor"] = self.crear_input(fila, "Valor", 18, padx=(30,0))
        self.campos["fecha"] = self.crear_input(fila, "Fecha", 18, padx=(30,0))
        self.campos["estado"] = self.crear_input(fila, "Estado", 18, padx=(30,0))
        self.campos["descripcion"] = self.crear_input(fila, "Descripción", 30, padx=(30,0))

        acciones = tk.Frame(self, bg=COLOR_FONDO); acciones.pack(fill="x", padx=20, pady=15)
        for texto,color,cmd in [("Guardar", "#2ecc71", self.guardar), ("Actualizar", "#3b82f6", self.actualizar), ("Eliminar", "#dc2626", self.eliminar), ("Limpiar", "#d1d5db", self.limpiar)]:
            tk.Button(acciones, text=texto, bg=color, fg="white" if color != "#d1d5db" else "#111827", font=("Segoe UI", 10, "bold"), width=12, command=cmd).pack(side="left", padx=5)

        busqueda = tk.Frame(self, bg=COLOR_FONDO); busqueda.pack(fill="x", padx=20, pady=(0,10))
        tk.Label(busqueda, text="Buscar:", bg=COLOR_FONDO, font=("Segoe UI", 10, "bold")).pack(side="left")
        entry = tk.Entry(busqueda, width=25, font=("Segoe UI", 10)); entry.pack(side="left", padx=10)
        entry.bind("<KeyRelease>", self.buscar)

        tabla_frame = tk.Frame(self, bg="#f1f5f9"); tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
        self.tree = ttk.Treeview(tabla_frame, columns=("id", self.nombre_campo, "valor", "fecha", "estado", "descripcion"), show="headings", height=12)
        for col, titulo in [("id","ID"), (self.nombre_campo, self.nombre_campo.title()), ("valor","Valor"), ("fecha","Fecha"), ("estado","Estado"), ("descripcion","Descripción")]:
            self.tree.heading(col, text=titulo)
        self.tree.column(self.nombre_campo, width=200); self.tree.column("descripcion", width=220)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.cargar_seleccionado)

    def limpiar(self):
        for campo in self.campos.values(): campo.delete(0, tk.END); self.selected_id=None

    def guardar(self):
        nombre = self.campos[self.nombre_campo].get().strip(); valor = self.campos["valor"].get().strip(); fecha = self.campos["fecha"].get().strip(); estado = self.campos["estado"].get().strip(); descripcion = self.campos["descripcion"].get().strip()
        if not all([nombre, valor, fecha, estado]):
            messagebox.showwarning("Advertencia", "Complete los campos obligatorios."); return
        try: valor=float(valor)
        except ValueError:
            messagebox.showwarning("Advertencia", "Valor debe ser numérico."); return
        guardar_cuenta(self.tipo, nombre, valor, fecha, estado, descripcion)
        self.cargar_tabla(); self.limpiar()

    def actualizar(self):
        if not self.selected_id:
            messagebox.showwarning("Advertencia", "Seleccione un registro para actualizar."); return
        nombre = self.campos[self.nombre_campo].get().strip(); valor = self.campos["valor"].get().strip(); fecha = self.campos["fecha"].get().strip(); estado = self.campos["estado"].get().strip(); descripcion = self.campos["descripcion"].get().strip()
        try: valor=float(valor)
        except ValueError: messagebox.showwarning("Advertencia", "Valor debe ser numérico."); return
        actualizar_cuenta(self.tipo, self.selected_id, nombre, valor, fecha, estado, descripcion)
        self.cargar_tabla(); self.limpiar()

    def eliminar(self):
        if not self.selected_id:
            messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar."); return
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este registro?"):
            eliminar_cuenta(self.tipo, self.selected_id); self.cargar_tabla(); self.limpiar()

    def cargar_tabla(self, filtro=""):
        for item in self.tree.get_children(): self.tree.delete(item)
        for row in listar_cuentas(self.tipo, filtro):
            self.tree.insert("", tk.END, values=(row["id"], row[self.nombre_campo], row["valor"], row["fecha"], row["estado"], row["descripcion"]))

    def buscar(self, event):
        self.cargar_tabla(event.widget.get().strip())

    def cargar_seleccionado(self, event):
        item = self.tree.selection()[0]; values = self.tree.item(item, "values")
        if not values: return
        self.selected_id = values[0]
        self.campos[self.nombre_campo].delete(0, tk.END); self.campos[self.nombre_campo].insert(0, values[1])
        self.campos["valor"].delete(0, tk.END); self.campos["valor"].insert(0, values[2])
        self.campos["fecha"].delete(0, tk.END); self.campos["fecha"].insert(0, values[3])
        self.campos["estado"].delete(0, tk.END); self.campos["estado"].insert(0, values[4])
        self.campos["descripcion"].delete(0, tk.END); self.campos["descripcion"].insert(0, values[5] or "")


class CuentasCobrarView(CuentaViewBase):
    def __init__(self, parent):
        super().__init__(parent, "CUENTAS POR COBRAR", "cliente", "cobrar")


class CuentasPagarView(CuentaViewBase):
    def __init__(self, parent):
        super().__init__(parent, "CUENTAS POR PAGAR", "proveedor", "pagar")


class ReportesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO); self.pack(fill="both", expand=True)
        self.construir()

    def construir(self):
        tk.Label(self, text="REPORTES Y AUDITORÍA", bg=COLOR_FONDO, fg="#1f2937", font=("Segoe UI", 26, "bold")).pack(pady=(20, 10))
        report = reporte_general()
        contenedor = tk.Frame(self, bg=COLOR_FONDO); contenedor.pack(pady=15)
        for titulo, valor, color in [("Productos", report["productos"], "#2563EB"), ("Clientes", report["clientes"], "#16A34A"), ("Proveedores", report["proveedores"], "#EA580C"), ("Ventas", report["ventas"], "#7C3AED")]:
            card = tk.Frame(contenedor, bg=color, width=200, height=110); card.pack_propagate(False); card.pack(side="left", padx=12)
            tk.Label(card, text=titulo, bg=color, fg="white", font=("Segoe UI", 11, "bold")).pack(pady=(20,5))
            tk.Label(card, text=str(valor), bg=color, fg="white", font=("Segoe UI", 24, "bold")).pack()

        resumen = tk.Frame(self, bg=COLOR_FONDO); resumen.pack(pady=30)
        tk.Label(resumen, text=f"Total ventas: $ {report['total_ventas']:,.0f}", bg=COLOR_FONDO, fg="#111827", font=("Segoe UI", 18, "bold")).pack()


class ERPApp(tk.Tk):
    def __init__(self):
        super().__init__(); self.title(APP_NAME); self.geometry("1280x720"); self.configure(bg="#dfe8ef"); self.minsize(1100,650)
        self.sidebar = tk.Frame(self, width=220, bg=COLOR_SECUNDARIO); self.sidebar.pack(side="left", fill="y"); self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar, text=APP_NAME, bg=COLOR_SECUNDARIO, fg="white", font=("Segoe UI", 18, "bold")).pack(pady=(15,5))
        tk.Label(self.sidebar, text="Versión 1.0", bg=COLOR_SECUNDARIO, fg="#d1d5db", font=("Segoe UI", 10)).pack(pady=(0,20))

        self.nav_items = ["Dashboard", "Ventas", "Inventario", "Clientes", "Proveedores", "Cuentas por Cobrar", "Cuentas por Pagar", "ReportesAuditoría", "Cerrar Sesión"]
        self.nav_buttons = {}
        for item in self.nav_items:
            btn = tk.Button(self.sidebar, text=item, bg=COLOR_SECUNDARIO, fg="white", bd=0, font=("Segoe UI", 11), width=20, anchor="w", justify="left", command=lambda nombre=item: self.cambiar_pagina(nombre))
            btn.pack(fill="x", pady=2, padx=10); self.nav_buttons[item] = btn

        self.footer = tk.Frame(self.sidebar, bg=COLOR_SECUNDARIO); self.footer.pack(side="bottom", fill="x", pady=(0,20))
        tk.Label(self.footer, text=EMPRESA, bg=COLOR_SECUNDARIO, fg="#f3f4f6", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10)
        tk.Label(self.footer, text=f"NIT: {NIT}", bg=COLOR_SECUNDARIO, fg="#d1d5db", font=("Segoe UI", 10)).pack(anchor="w", padx=10)

        self.main = tk.Frame(self, bg=COLOR_FONDO); self.main.pack(side="left", fill="both", expand=True)
        self.pages = {
            "Dashboard": DashboardView(self.main),
            "Ventas": VentasView(self.main),
            "Inventario": InventarioView(self.main),
            "Clientes": ClientesView(self.main),
            "Proveedores": ProveedoresView(self.main),
            "Cuentas por Cobrar": CuentasCobrarView(self.main),
            "Cuentas por Pagar": CuentasPagarView(self.main),
            "ReportesAuditoría": ReportesView(self.main),
            "Cerrar Sesión": tk.Frame(self.main, bg=COLOR_FONDO),
        }
        for frame in self.pages.values():
            if isinstance(frame, tk.Frame): frame.pack_forget()
        self.cambiar_pagina("Dashboard")

    def cambiar_pagina(self, nombre):
        if nombre == "Cerrar Sesión":
            if messagebox.askyesno("Cerrar sesión", "¿Desea cerrar la sesión?"):
                self.destroy(); return
            return
        for key, page in self.pages.items():
            if key == nombre:
                page.pack(fill="both", expand=True)
            else:
                page.pack_forget()
        for n, btn in self.nav_buttons.items():
            btn.configure(bg=COLOR_SECUNDARIO if n != nombre else "#2d3c4d")


def main():
    crear_tablas(); app = ERPApp(); app.mainloop()


if __name__ == "__main__":
    main()
