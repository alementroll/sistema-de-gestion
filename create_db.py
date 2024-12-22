import sqlite3

def create_db():
    # Conexión a la base de datos
    con = sqlite3.connect(database=r'tbs.db')
    cur = con.cursor()

    # Tabla clientes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            eid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            contact TEXT,
            pass TEXT,
            utype TEXT
        )
    """)
    con.commit()

    # Tabla servicios
    cur.execute("""
        CREATE TABLE IF NOT EXISTS services(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            estimated_time TEXT
        )
    """)
    con.commit()

    # Tabla productos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock(
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            itemname TEXT,
            price REAL,
            qty INTEGER
        )
    """)
    con.commit()

    # Tabla pedidos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            device TEXT,
            status TEXT,
            details TEXT,
            order_date TEXT,
            total_price REAL,
            FOREIGN KEY(client_id) REFERENCES client(eid)
        )
    """)
    con.commit()

    # Tabla de relación pedidos-servicios
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_services(
            order_id INTEGER,
            service_id INTEGER,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(service_id) REFERENCES services(id)
        )
    """)
    con.commit()

    # Tabla de relación pedidos-productos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_products(
            order_id INTEGER,
            product_id INTEGER,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES stock(pid)
        )
    """)
    con.commit()

    # Cerrar conexión
    con.close()

# Llamar a la función para crear la base de datos y las tablas
create_db()