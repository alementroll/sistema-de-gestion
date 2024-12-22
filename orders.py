from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class OrderClass:
    def __init__(self, container, show_orders_list_callback, reload_clients_callback):
        self.container = container
        self.show_orders_list_callback = show_orders_list_callback
        self.reload_clients_callback = reload_clients_callback

        # Variables
        self.var_client_type = StringVar(value="Cliente Existente")
        self.var_client = StringVar()
        self.var_device = StringVar()
        self.var_status = StringVar()
        self.var_details = StringVar()
        self.var_new_client_name = StringVar()
        self.var_new_client_email = StringVar()
        self.var_new_client_contact = StringVar()

        # Título
        self.title = Label(self.container, text="Gestión de Pedidos", font=("goudy old style", 25, "bold"),
                           bg="#13278f", fg="white", bd=3)
        self.title.pack(side=TOP, fill=X)

        # Selección de tipo de cliente
        self.lbl_client_type = Label(self.container, text="Tipo de Cliente", font=("goudy old style", 15), bg="white")
        self.lbl_client_type.place(relx=0.05, rely=0.1)
        self.cmb_client_type = ttk.Combobox(self.container, textvariable=self.var_client_type, state="readonly",
                                            values=["Cliente Existente", "Cliente Nuevo"], justify=CENTER, font=("goudy old style", 12))
        self.cmb_client_type.place(relx=0.25, rely=0.1, relwidth=0.4)
        self.cmb_client_type.bind("<<ComboboxSelected>>", self.on_client_type_change)

        # Campos de entrada para Cliente Existente
        self.lbl_client = Label(self.container, text="Cliente", font=("goudy old style", 15), bg="white")
        self.lbl_client.place(relx=0.05, rely=0.14)
        self.cmb_client = ttk.Combobox(self.container, textvariable=self.var_client, state="readonly",
                                       justify=CENTER, font=("goudy old style", 12))
        self.cmb_client.place(relx=0.25, rely=0.14, relwidth=0.4)
        self.load_clients()

        # Campos de entrada para Cliente Nuevo
        self.lbl_new_client_name = Label(self.container, text="Nombre", font=("goudy old style", 15), bg="white")
        self.txt_new_client_name = Entry(self.container, textvariable=self.var_new_client_name, font=("goudy old style", 15), bg="white", bd=3)

        self.lbl_new_client_email = Label(self.container, text="Correo", font=("goudy old style", 15), bg="white")
        self.txt_new_client_email = Entry(self.container, textvariable=self.var_new_client_email, font=("goudy old style", 15), bg="white", bd=3)

        self.lbl_new_client_contact = Label(self.container, text="Teléfono", font=("goudy old style", 15), bg="white")
        self.txt_new_client_contact = Entry(self.container, textvariable=self.var_new_client_contact, font=("goudy old style", 15), bg="white", bd=3)

        # Campos de entrada comunes
        self.lbl_device = Label(self.container, text="Aparato", font=("goudy old style", 15), bg="white")
        self.lbl_device.place(relx=0.05, rely=0.3)
        self.txt_device = Entry(self.container, textvariable=self.var_device, font=("goudy old style", 15), bg="white", bd=3)
        self.txt_device.place(relx=0.25, rely=0.3, relwidth=0.4)

        self.lbl_status = Label(self.container, text="Estado", font=("goudy old style", 15), bg="white")
        self.lbl_status.place(relx=0.05, rely=0.36)
        self.cmb_status = ttk.Combobox(self.container, textvariable=self.var_status,
                                        values=("Por hacer", "En proceso", "Terminado"),
                                        state="readonly", justify=CENTER, font=("goudy old style", 12))
        self.cmb_status.place(relx=0.25, rely=0.36, relwidth=0.4)
        self.cmb_status.current(0)

        self.lbl_details = Label(self.container, text="Detalles", font=("goudy old style", 15), bg="white")
        self.lbl_details.place(relx=0.05, rely=0.42)
        self.txt_details = Entry(self.container, textvariable=self.var_details, font=("goudy old style", 15), bg="white", bd=3)
        self.txt_details.place(relx=0.25, rely=0.42, relwidth=0.4)

        self.lbl_services = Label(self.container, text="Servicios", font=("goudy old style", 15), bg="white")
        self.lbl_services.place(relx=0.05, rely=0.48)
        self.lst_services = Listbox(self.container, selectmode=MULTIPLE, font=("goudy old style", 12), bg="white", bd=3)
        self.lst_services.place(relx=0.25, rely=0.48, relwidth=0.4, relheight=0.1)
        self.load_services()

        self.lbl_products = Label(self.container, text="Productos", font=("goudy old style", 15), bg="white")
        self.lbl_products.place(relx=0.05, rely=0.6)
        self.lst_products = Listbox(self.container, selectmode=MULTIPLE, font=("goudy old style", 12), bg="white", bd=3)
        self.lst_products.place(relx=0.25, rely=0.6, relwidth=0.4, relheight=0.1)
        self.load_products()

        # Botón Agregar
        self.btn_add = Button(self.container, text="Agregar", command=self.add, font=("goudy old style", 15, "bold"),
                                bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_add.place(relx=0.25, rely=0.72, relwidth=0.2, height=35)

        # Botón para cambiar a la lista de pedidos
        self.btn_show_list = Button(self.container, text="Ver Lista de Pedidos", command=self.show_orders_list_callback, font=("goudy old style", 15, "bold"),
                                bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_show_list.place(relx=0.5, rely=0.72, relwidth=0.3, height=35)

        # Vinculación de redimensionado
        self.container.bind("<Configure>", self.on_resize)

        # Inicializar la vista según el tipo de cliente
        self.on_client_type_change()

    def on_client_type_change(self, event=None):
        """Muestra u oculta los campos según el tipo de cliente seleccionado."""
        if self.var_client_type.get() == "Cliente Nuevo":
            self.lbl_client.place_forget()
            self.cmb_client.place_forget()

            self.lbl_new_client_name.place(relx=0.05, rely=0.14)
            self.txt_new_client_name.place(relx=0.25, rely=0.14, relwidth=0.4)

            self.lbl_new_client_email.place(relx=0.05, rely=0.2)
            self.txt_new_client_email.place(relx=0.25, rely=0.2, relwidth=0.4)

            self.lbl_new_client_contact.place(relx=0.05, rely=0.26)
            self.txt_new_client_contact.place(relx=0.25, rely=0.26, relwidth=0.4)
        else:
            self.lbl_client.place(relx=0.05, rely=0.14)
            self.cmb_client.place(relx=0.25, rely=0.14, relwidth=0.4)

            self.lbl_new_client_name.place_forget()
            self.txt_new_client_name.place_forget()

            self.lbl_new_client_email.place_forget()
            self.txt_new_client_email.place_forget()

            self.lbl_new_client_contact.place_forget()
            self.txt_new_client_contact.place_forget()

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
        for widget in [self.lbl_client_type, self.cmb_client_type, self.lbl_client, self.cmb_client,
                       self.lbl_new_client_name, self.txt_new_client_name, self.lbl_new_client_email, self.txt_new_client_email,
                       self.lbl_new_client_contact, self.txt_new_client_contact, self.lbl_device, self.txt_device,
                       self.lbl_status, self.cmb_status, self.lbl_details, self.txt_details, self.lbl_services, self.lst_services,
                       self.lbl_products, self.lst_products, self.btn_add, self.btn_show_list]:
            widget.config(font=("goudy old style", font_size))

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
            for row in rows:
                self.lst_services.insert(END, f"{row[0]} - {row[1]}")
        except Exception as ex:
            messagebox.showerror("Error", f"Error al cargar servicios: {str(ex)}")

    def load_products(self):
        """Carga los productos desde la tabla 'stock' en la base de datos."""
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT pid, itemname FROM stock")
            rows = cur.fetchall()
            for row in rows:
                self.lst_products.insert(END, f"{row[0]} - {row[1]}")
        except Exception as ex:
            messagebox.showerror("Error", f"Error al cargar productos: {str(ex)}")

    def add(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            if self.var_client_type.get() == "Cliente Nuevo":
                # Validar campos de cliente nuevo
                if not self.var_new_client_name.get() or not self.var_new_client_email.get() or not self.var_new_client_contact.get():
                    messagebox.showerror("Error", "Todos los campos de cliente nuevo son obligatorios")
                    return

                # Insertar nuevo cliente
                cur.execute("""
                    INSERT INTO client (name, email, contact, pass, utype)
                    VALUES (?, ?, ?, ?, ?)
                """, (self.var_new_client_name.get(), self.var_new_client_email.get(), self.var_new_client_contact.get(), "", "Cliente"))
                con.commit()

                # Obtener el ID del nuevo cliente
                cur.execute("SELECT eid FROM client WHERE email = ?", (self.var_new_client_email.get(),))
                client_id = cur.fetchone()[0]

                # Recargar la lista de clientes en otras vistas
                self.reload_clients_callback()
            else:
                client_id = int(self.var_client.get().split(" - ")[0])  # Extraer ID del cliente existente

            device = self.var_device.get()
            status = self.var_status.get()
            details = self.var_details.get()

            if not device:
                messagebox.showerror("Error", "El campo Aparato es obligatorio")
                return

            # Insertar pedido
            cur.execute("""
                INSERT INTO orders (client_id, device, status, details, order_date, total_price)
                VALUES (?, ?, ?, ?, date('now'), 0)
            """, (client_id, device, status, details))
            con.commit()

            # Obtener el ID del nuevo pedido
            cur.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
            order_id = cur.fetchone()[0]

            # Insertar servicios del pedido
            selected_services = self.lst_services.curselection()
            for i in selected_services:
                service_id = int(self.lst_services.get(i).split(" - ")[0])
                cur.execute("INSERT INTO order_services (order_id, service_id) VALUES (?, ?)", (order_id, service_id))

            # Insertar productos del pedido
            selected_products = self.lst_products.curselection()
            for i in selected_products:
                product_id = int(self.lst_products.get(i).split(" - ")[0])
                cur.execute("INSERT INTO order_products (order_id, product_id) VALUES (?, ?)", (order_id, product_id))

            con.commit()
            messagebox.showinfo("Éxito", "Pedido agregado correctamente")
        except Exception as ex:
            messagebox.showerror("Error", f"Error al agregar pedido: {str(ex)}")
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = OrderClass(root, lambda: print("Callback no definido"), lambda: print("Recargar clientes no definido"))
    root.mainloop()