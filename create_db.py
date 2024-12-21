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
            Supplier TEXT,
            itemname TEXT,
            hsncode TEXT,
            price REAL,
            qty INTEGER,
            discount REAL
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
            service_id INTEGER,
            order_date TEXT,
            total_price REAL,
            FOREIGN KEY(client_id) REFERENCES client(id),
            FOREIGN KEY(service_id) REFERENCES services(id)
        )
    """)
    con.commit()

    # Cerrar conexión
    con.close()

# Llamar a la función para crear la base de datos y las tablas
create_db()