import sqlite3

from config import DB_PATH


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_documento TEXT,
            documento TEXT,
            telefono TEXT,
            direccion TEXT,
            sexo TEXT,
            email TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            nit TEXT,
            telefono TEXT,
            direccion TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_venta TEXT NOT NULL,
            fecha TEXT NOT NULL,
            vendedor TEXT NOT NULL,
            subtotal REAL NOT NULL,
            descuento REAL NOT NULL,
            iva REAL NOT NULL,
            total REAL NOT NULL,
            metodo_pago TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            codigo_producto TEXT NOT NULL,
            producto TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (venta_id) REFERENCES ventas(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cuentas_cobrar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            valor REAL NOT NULL,
            fecha TEXT NOT NULL,
            estado TEXT NOT NULL,
            descripcion TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cuentas_pagar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proveedor TEXT NOT NULL,
            valor REAL NOT NULL,
            fecha TEXT NOT NULL,
            estado TEXT NOT NULL,
            descripcion TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def listar_productos(filtro=""):
    conn = conectar()
    cursor = conn.cursor()
    if filtro:
        cursor.execute(
            "SELECT codigo, nombre, precio, stock FROM productos WHERE codigo LIKE ? OR nombre LIKE ? ORDER BY nombre",
            (f"%{filtro}%", f"%{filtro}%"),
        )
    else:
        cursor.execute("SELECT codigo, nombre, precio, stock FROM productos ORDER BY nombre")
    filas = cursor.fetchall()
    conn.close()
    return [dict(row) for row in filas]


def guardar_producto(codigo, nombre, precio, stock):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (codigo, nombre, precio, stock) VALUES (?, ?, ?, ?)",
        (codigo, nombre, precio, stock),
    )
    conn.commit()
    conn.close()


def actualizar_producto(codigo, nombre, precio, stock):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE codigo = ?",
        (nombre, precio, stock, codigo),
    )
    conn.commit()
    conn.close()


def eliminar_producto(codigo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))
    conn.commit()
    conn.close()


def buscar_producto(codigo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT codigo, nombre, precio, stock FROM productos WHERE codigo = ?",
        (codigo,),
    )
    producto = cursor.fetchone()
    conn.close()
    return dict(producto) if producto else None


def contar_tabla(nombre_tabla):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla}")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def listar_clientes(filtro=""):
    conn = conectar()
    cursor = conn.cursor()
    if filtro:
        cursor.execute(
            """
            SELECT id, nombre, tipo_documento, documento, sexo, telefono, direccion, email
            FROM clientes
            WHERE nombre LIKE ? OR documento LIKE ? OR email LIKE ?
            ORDER BY nombre
            """,
            (f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"),
        )
    else:
        cursor.execute(
            "SELECT id, nombre, tipo_documento, documento, sexo, telefono, direccion, email FROM clientes ORDER BY nombre"
        )
    filas = cursor.fetchall()
    conn.close()
    return [dict(row) for row in filas]


def guardar_cliente(nombre, tipo_documento, documento, sexo, telefono, direccion, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO clientes (nombre, tipo_documento, documento, sexo, telefono, direccion, email)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (nombre, tipo_documento, documento, sexo, telefono, direccion, email),
    )
    conn.commit()
    conn.close()


def actualizar_cliente(id_cliente, nombre, tipo_documento, documento, sexo, telefono, direccion, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE clientes
        SET nombre = ?, tipo_documento = ?, documento = ?, sexo = ?, telefono = ?, direccion = ?, email = ?
        WHERE id = ?
        """,
        (nombre, tipo_documento, documento, sexo, telefono, direccion, email, id_cliente),
    )
    conn.commit()
    conn.close()


def eliminar_cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    conn.commit()
    conn.close()


def buscar_cliente_por_documento(documento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre, tipo_documento, documento, sexo, telefono, direccion, email FROM clientes WHERE documento = ?",
        (documento,),
    )
    cliente = cursor.fetchone()
    conn.close()
    return dict(cliente) if cliente else None


def listar_proveedores(filtro=""):
    conn = conectar()
    cursor = conn.cursor()
    if filtro:
        cursor.execute(
            "SELECT id, nombre, nit, telefono, direccion FROM proveedores WHERE nombre LIKE ? OR nit LIKE ? ORDER BY nombre",
            (f"%{filtro}%", f"%{filtro}%"),
        )
    else:
        cursor.execute("SELECT id, nombre, nit, telefono, direccion FROM proveedores ORDER BY nombre")
    filas = cursor.fetchall()
    conn.close()
    return [dict(row) for row in filas]


def guardar_proveedor(nombre, nit, telefono, direccion):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO proveedores (nombre, nit, telefono, direccion) VALUES (?, ?, ?, ?)",
        (nombre, nit, telefono, direccion),
    )
    conn.commit()
    conn.close()


def actualizar_proveedor(id_proveedor, nombre, nit, telefono, direccion):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE proveedores SET nombre = ?, nit = ?, telefono = ?, direccion = ? WHERE id = ?",
        (nombre, nit, telefono, direccion, id_proveedor),
    )
    conn.commit()
    conn.close()


def eliminar_proveedor(id_proveedor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM proveedores WHERE id = ?", (id_proveedor,))
    conn.commit()
    conn.close()


def buscar_proveedor_por_nit(nit):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, nit, telefono, direccion FROM proveedores WHERE nit = ?", (nit,))
    proveedor = cursor.fetchone()
    conn.close()
    return dict(proveedor) if proveedor else None


def listar_ventas(filtro=""):
    conn = conectar()
    cursor = conn.cursor()
    if filtro:
        cursor.execute(
            "SELECT id, numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago FROM ventas WHERE numero_venta LIKE ? OR vendedor LIKE ? ORDER BY fecha DESC",
            (f"%{filtro}%", f"%{filtro}%"),
        )
    else:
        cursor.execute("SELECT id, numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago FROM ventas ORDER BY fecha DESC")
    filas = cursor.fetchall()
    conn.close()
    return [dict(row) for row in filas]


def guardar_venta(numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ventas (numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago),
    )
    conn.commit()
    conn.close()


def actualizar_venta(id_venta, numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE ventas SET numero_venta = ?, fecha = ?, vendedor = ?, subtotal = ?, descuento = ?, iva = ?, total = ?, metodo_pago = ? WHERE id = ?",
        (numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago, id_venta),
    )
    conn.commit()
    conn.close()


def eliminar_venta(id_venta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ventas WHERE id = ?", (id_venta,))
    conn.commit()
    conn.close()


def listar_cuentas(tipo, filtro=""):
    tabla = "cuentas_cobrar" if tipo == "cobrar" else "cuentas_pagar"
    campo = "cliente" if tipo == "cobrar" else "proveedor"
    conn = conectar()
    cursor = conn.cursor()
    if filtro:
        cursor.execute(
            f"SELECT id, {campo}, valor, fecha, estado, descripcion FROM {tabla} WHERE {campo} LIKE ? OR descripcion LIKE ? ORDER BY fecha DESC",
            (f"%{filtro}%", f"%{filtro}%"),
        )
    else:
        cursor.execute(f"SELECT id, {campo}, valor, fecha, estado, descripcion FROM {tabla} ORDER BY fecha DESC")
    filas = cursor.fetchall()
    conn.close()
    return [dict(row) for row in filas]


def guardar_cuenta(tipo, nombre, valor, fecha, estado, descripcion):
    tabla = "cuentas_cobrar" if tipo == "cobrar" else "cuentas_pagar"
    campo = "cliente" if tipo == "cobrar" else "proveedor"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO {tabla} ({campo}, valor, fecha, estado, descripcion) VALUES (?, ?, ?, ?, ?)",
        (nombre, valor, fecha, estado, descripcion),
    )
    conn.commit()
    conn.close()


def actualizar_cuenta(tipo, id_cuenta, nombre, valor, fecha, estado, descripcion):
    tabla = "cuentas_cobrar" if tipo == "cobrar" else "cuentas_pagar"
    campo = "cliente" if tipo == "cobrar" else "proveedor"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE {tabla} SET {campo} = ?, valor = ?, fecha = ?, estado = ?, descripcion = ? WHERE id = ?",
        (nombre, valor, fecha, estado, descripcion, id_cuenta),
    )
    conn.commit()
    conn.close()


def eliminar_cuenta(tipo, id_cuenta):
    tabla = "cuentas_cobrar" if tipo == "cobrar" else "cuentas_pagar"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {tabla} WHERE id = ?", (id_cuenta,))
    conn.commit()
    conn.close()


def reporte_general():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    productos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM clientes")
    clientes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM proveedores")
    proveedores = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ventas")
    ventas = cursor.fetchone()[0]
    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas")
    total_ventas = cursor.fetchone()[0]
    conn.close()
    return {
        "productos": productos,
        "clientes": clientes,
        "proveedores": proveedores,
        "ventas": ventas,
        "total_ventas": total_ventas,
    }


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos inicializada correctamente.")
