from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class OrderClass:
    def __init__(self, container):
        self.container = container

        # Variables
        self.var_client = StringVar()
        self.var_device = StringVar()
        self.var_status = StringVar()
        self.var_service = StringVar()

        # Título
        self.title = Label(self.container, text="Gestión de Pedidos", font=("goudy old style", 25, "bold"),
                           bg="#13278f", fg="white", bd=3)
        self.title.pack(side=TOP, fill=X)

        # Campos de entrada
        self.lbl_client = Label(self.container, text="Cliente", font=("goudy old style", 15), bg="white")
        self.lbl_client.place(relx=0.05, rely=0.14)
        self.cmb_client = ttk.Combobox(self.container, textvariable=self.var_client, state="readonly",
                                       justify=CENTER, font=("goudy old style", 12))
        self.cmb_client.place(relx=0.25, rely=0.14, relwidth=0.4)
        self.load_clients()

        self.lbl_device = Label(self.container, text="Aparato", font=("goudy old style", 15), bg="white")
        self.lbl_device.place(relx=0.05, rely=0.2)
        self.txt_device = Entry(self.container, textvariable=self.var_device, font=("goudy old style", 15), bg="white", bd=3)
        self.txt_device.place(relx=0.25, rely=0.2, relwidth=0.4)

        self.lbl_status = Label(self.container, text="Estado", font=("goudy old style", 15), bg="white")
        self.lbl_status.place(relx=0.05, rely=0.26)
        self.cmb_status = ttk.Combobox(self.container, textvariable=self.var_status,
                                        values=("Por hacer", "En proceso", "Terminado"),
                                        state="readonly", justify=CENTER, font=("goudy old style", 12))
        self.cmb_status.place(relx=0.25, rely=0.26, relwidth=0.4)
        self.cmb_status.current(0)

        self.lbl_service = Label(self.container, text="Servicio", font=("goudy old style", 15), bg="white")
        self.lbl_service.place(relx=0.05, rely=0.32)
        self.cmb_service = ttk.Combobox(self.container, textvariable=self.var_service, state="readonly",
                                        justify=CENTER, font=("goudy old style", 12))
        self.cmb_service.place(relx=0.25, rely=0.32, relwidth=0.4)
        self.load_services()

        # Botón Agregar
        self.btn_add = Button(self.container, text="Agregar", command=self.add, font=("goudy old style", 15, "bold"),
                              bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_add.place(relx=0.25, rely=0.38, relwidth=0.2, height=35)

        # Tabla de Pedidos
        self.order_frame = Frame(self.container, bd=3, relief=RIDGE)
        self.order_frame.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.45)

        self.scrolly = Scrollbar(self.order_frame, orient=VERTICAL)
        self.scrollx = Scrollbar(self.order_frame, orient=HORIZONTAL)
        self.OrderTable = ttk.Treeview(self.order_frame, columns=("id", "name", "device", "status", "service"),
                                       yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)

        self.scrolly.pack(side=RIGHT, fill=Y)
        self.scrollx.pack(side=BOTTOM, fill=X)
        self.scrolly.config(command=self.OrderTable.yview)
        self.scrollx.config(command=self.OrderTable.xview)

        self.OrderTable.heading("id", text="ID")
        self.OrderTable.heading("name", text="Cliente")
        self.OrderTable.heading("device", text="Aparato")
        self.OrderTable.heading("status", text="Estado")
        self.OrderTable.heading("service", text="Servicio")

        self.OrderTable["show"] = "headings"

        self.OrderTable.column("id", width=50)
        self.OrderTable.column("name", width=200)
        self.OrderTable.column("device", width=200)
        self.OrderTable.column("status", width=150)
        self.OrderTable.column("service", width=200)

        self.OrderTable.pack(fill=BOTH, expand=1)

        # Vinculación de redimensionado
        self.container.bind("<Configure>", self.on_resize)
        self.show()

    def on_resize(self, event):
        """Ajusta las fuentes y tamaños de los elementos al tamaño del contenedor."""
        width = self.container.winfo_width()
        height = self.container.winfo_height()

        scale_width = width / 1200  # Escala de referencia para el ancho
        scale_height = height / 700  # Escala de referencia para la altura
        font_size = int(12 * min(scale_width, scale_height))

        font_size = max(8, font_size)  # Asegura un tamaño mínimo
        self.title.config(font=("goudy old style", font_size + 6, "bold"))

        # Ajuste de tamaño de los elementos
        for widget in [self.lbl_client, self.lbl_device, self.lbl_status, self.lbl_service, self.btn_add]:
            widget.config(font=("goudy old style", font_size))

        # Ajuste de tamaño de la tabla
        for col in self.OrderTable["columns"]:
            self.OrderTable.column(col, width=int(100 * scale_width))

    def load_clients(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT eid, name FROM client")
            rows = cur.fetchall()
            client = [f"{row[0]} - {row[1]}" for row in rows]
            self.cmb_client["values"] = client
            if client:
                self.cmb_client.current(0)
        except Exception as ex:
            messagebox.showerror("Error", f"Error al cargar clientes: {str(ex)}")

    def load_services(self):
        """Carga los servicios desde la tabla 'services' en la base de datos."""
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT id, name FROM services")
            rows = cur.fetchall()
            services = [f"{row[0]} - {row[1]}" for row in rows]
            self.cmb_service["values"] = services
            if services:
                self.cmb_service.current(0)
        except Exception as ex:
            messagebox.showerror("Error", f"Error al cargar servicios: {str(ex)}", parent=self.root)

    def add(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            client_id = int(self.var_client.get().split(" - ")[0])  # Extraer ID del cliente
            service_id = int(self.var_service.get().split(" - ")[0])  # Extraer ID del servicio
            device = self.var_device.get()
            status = self.var_status.get()

            if not device:
                messagebox.showerror("Error", "El campo Aparato es obligatorio")
                return

            # Consultar el precio del servicio
            cur.execute("SELECT price FROM services WHERE id = ?", (service_id,))
            service_price = cur.fetchone()
            if not service_price:
                messagebox.showerror("Error", "Servicio no encontrado")
                return

            total_price = service_price[0]  # Usar el precio del servicio como total (puedes calcular más si necesitas)

            # Insertar pedido
            cur.execute("""
                INSERT INTO orders (client_id, device, status, service_id, order_date, total_price)
                VALUES (?, ?, ?, ?, date('now'), ?)
            """, (client_id, device, status, service_id, total_price))
            con.commit()
            messagebox.showinfo("Éxito", "Pedido agregado correctamente")
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error al agregar pedido: {str(ex)}")
        finally:
            con.close()

    def clear(self):
        """Limpia los campos de entrada."""
        self.var_client.set("")
        self.var_device.set("")
        self.var_status.set("Terminado")
        self.var_service.set("")
        if self.cmb_service["values"]:
            self.cmb_service.current(0)

    def show(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            # Consulta SQL para obtener los datos con nombres en lugar de IDs
            cur.execute("""
                SELECT o.id, c.name AS client_name, o.device, o.status, s.name AS service_name
                FROM orders o
                JOIN client c ON o.client_id = c.eid
                JOIN services s ON o.service_id = s.id
            """)
            rows = cur.fetchall()

            # Limpia la tabla antes de llenarla nuevamente
            self.OrderTable.delete(*self.OrderTable.get_children())

            # Rellena la tabla con los datos obtenidos
            for row in rows:
                self.OrderTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error al mostrar datos: {str(ex)}")
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = OrderClass(root)
    root.mainloop()