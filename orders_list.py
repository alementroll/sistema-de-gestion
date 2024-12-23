from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class OrderListClass:
    def __init__(self, container):
        self.container = container
        self.container.config(bg="#bde3ff")        

        # Título
        self.title = Label(self.container, text="Lista de Pedidos", font=("goudy old style", 25, "bold"),
                           bg="#13278f", fg="white", bd=3)
        self.title.pack(side=TOP, fill=X)

        # Filtros
        self.filter_frame = Frame(self.container, bg="#bde3ff")
        self.filter_frame.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.08)

        self.filter_by = StringVar()
        self.filter_by.set("Nombre")

        self.filter_options = ["Nombre", "Equipo", "Servicio", "Estado"]
        self.cmb_filter_by = ttk.Combobox(self.filter_frame, textvariable=self.filter_by, values=self.filter_options, state="readonly", font=("goudy old style", 15))
        self.cmb_filter_by.place(relx=0.01, rely=0.1, relwidth=0.15)

        self.filter_value = StringVar()
        self.txt_filter_value = Entry(self.filter_frame, textvariable=self.filter_value, font=("goudy old style", 15))
        self.txt_filter_value.place(relx=0.17, rely=0.1, relwidth=0.2)

        self.cmb_filter_value = ttk.Combobox(self.filter_frame, textvariable=self.filter_value, state="readonly", font=("goudy old style", 15))
        self.cmb_filter_value.place_forget()

        self.cmb_filter_by.bind("<<ComboboxSelected>>", self.on_filter_by_change)

        self.btn_filter = Button(self.filter_frame, text="Filtrar", command=self.apply_filter, font=("goudy old style", 15, "bold"),
                                 bg="#13278f", fg="white", cursor="hand2")
        self.btn_filter.place(relx=0.38, rely=0.1, relwidth=0.1)

        self.btn_clear_filter = Button(self.filter_frame, text="Limpiar Filtro", command=self.clear_filter, font=("goudy old style", 15, "bold"),
                                       bg="#13278f", fg="white", cursor="hand2")
        self.btn_clear_filter.place(relx=0.5, rely=0.1, relwidth=0.15)

        # Frame para la lista de pedidos con scroll
        self.order_frame = Frame(self.container, bd=3, relief=RIDGE)
        self.order_frame.place(relx=0.01, rely=0.2, relwidth=0.98, relheight=0.75)

        self.canvas = Canvas(self.order_frame, bg="#bde3ff")
        self.scrollbar = Scrollbar(self.order_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="#bde3ff")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.show()

    def on_filter_by_change(self, event):
        filter_by = self.filter_by.get()
        if filter_by in ["Nombre", "Equipo"]:
            self.txt_filter_value.place(relx=0.17, rely=0.1, relwidth=0.2)
            self.cmb_filter_value.place_forget()
        else:
            self.txt_filter_value.place_forget()
            if filter_by == "Estado":
                self.cmb_filter_value["values"] = ["Por hacer", "En proceso", "Terminado"]
            elif filter_by == "Servicio":
                self.load_services()
            self.cmb_filter_value.place(relx=0.17, rely=0.1, relwidth=0.2)

    def load_services(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM services")
            rows = cur.fetchall()
            services = [row[0] for row in rows]
            self.cmb_filter_value["values"] = services
        except Exception as ex:
            messagebox.showerror("Error", f"Error al cargar servicios: {str(ex)}")
        finally:
            con.close()

    def apply_filter(self):
        filter_by = self.filter_by.get()
        filter_value = self.filter_value.get()

        query = """
            SELECT o.id, c.name AS client_name, o.device, o.status, o.details, GROUP_CONCAT(s.name, ', ') AS services
            FROM orders o
            JOIN client c ON o.client_id = c.eid
            LEFT JOIN order_services os ON o.id = os.order_id
            LEFT JOIN services s ON os.service_id = s.id
        """
        if filter_by == "Nombre":
            query += " WHERE c.name LIKE ?"
            params = (f"%{filter_value}%",)
        elif filter_by == "Equipo":
            query += " WHERE o.device LIKE ?"
            params = (f"%{filter_value}%",)
        elif filter_by == "Estado":
            query += " WHERE o.status = ?"
            params = (filter_value,)
        elif filter_by == "Servicio":
            query += " WHERE s.name = ?"
            params = (filter_value,)
        query += " GROUP BY o.id, c.name, o.device, o.status, o.details"

        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            cur.execute(query, params)
            rows = cur.fetchall()
            self.update_table(rows)
        except Exception as ex:
            messagebox.showerror("Error", f"Error al aplicar filtro: {str(ex)}")
        finally:
            con.close()

    def clear_filter(self):
        self.filter_value.set("")
        self.show()

    def show(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            # Consulta SQL
            cur.execute("""
                SELECT o.id, c.name AS client_name, o.device, o.status, o.details, GROUP_CONCAT(s.name, ', ') AS services
                FROM orders o
                JOIN client c ON o.client_id = c.eid
                LEFT JOIN order_services os ON o.id = os.order_id
                LEFT JOIN services s ON os.service_id = s.id
                GROUP BY o.id, c.name, o.device, o.status, o.details
            """)
            rows = cur.fetchall()

            self.update_table(rows)
        except Exception as ex:
            messagebox.showerror("Error", f"Error al mostrar datos: {str(ex)}")
        finally:
            con.close()

    def update_table(self, rows):

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()


        for row in rows:
            self.create_order_frame(row)

    def create_order_frame(self, order_data):
        order_id, client_name, device, status, details, services = order_data

        frame = Frame(self.scrollable_frame, bd=2, relief=RIDGE, bg="white")
        frame.pack(fill=X, pady=5, padx=10)

        lbl_client = Label(frame, text=client_name, font=("goudy old style", 15, "bold"), bg="white", anchor="w")
        lbl_client.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        lbl_device = Label(frame, text=device, font=("goudy old style", 12), bg="white", anchor="w")
        lbl_device.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        lbl_status = Label(frame, text=status, font=("goudy old style", 12), bg="white", anchor="w")
        lbl_status.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        lbl_details = Label(frame, text=details, font=("goudy old style", 12), bg="white", anchor="w")
        lbl_details.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Dividir los servicios en líneas de hasta 4 servicios cada una
        services_list = services.split(", ") if services else []
        services_text = ""
        for i in range(0, len(services_list), 4):
            services_text += ", ".join(services_list[i:i+4]) + "\n"

        lbl_services = Label(frame, text=f"Servicios: {services_text.strip()}", font=("goudy old style", 12), bg="white", anchor="w", justify=LEFT)
        lbl_services.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Crear un frame para los botones y colocarlo al final del bloque
        btn_frame = Frame(frame, bg="white")
        btn_frame.grid(row=5, column=0, columnspan=2, sticky="e")

        btn_edit = Button(btn_frame, text="Editar", command=lambda: self.update(order_id), font=("goudy old style", 12, "bold"),
                          bg="#13278f", fg="white", cursor="hand2")
        btn_edit.pack(side=LEFT, padx=5, pady=5)

        btn_delete = Button(btn_frame, text="Eliminar", command=lambda: self.delete(order_id), font=("goudy old style", 12, "bold"),
                            bg="#13278f", fg="white", cursor="hand2")
        btn_delete.pack(side=LEFT, padx=5, pady=5)

    def update(self, order_id):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT o.id, c.name AS client_name, o.device, o.status, o.details, GROUP_CONCAT(s.name, ', ') AS services
                FROM orders o
                JOIN client c ON o.client_id = c.eid
                LEFT JOIN order_services os ON o.id = os.order_id
                LEFT JOIN services s ON os.service_id = s.id
                WHERE o.id = ?
                GROUP BY o.id, c.name, o.device, o.status, o.details
            """, (order_id,))
            data = cur.fetchone()
            if not data:
                messagebox.showerror("Error", "Pedido no encontrado")
                return

            # Crear una nueva ventana para actualizar el pedido
            self.update_window = Toplevel(self.container)
            self.update_window.title("Modificar Pedido")
            self.update_window.geometry("600x600")

            # Variables para la ventana de actualización
            self.var_update_client = StringVar(value=data[1])
            self.var_update_device = StringVar(value=data[2])
            self.var_update_status = StringVar(value=data[3])
            self.var_update_details = StringVar(value=data[4])
            self.var_update_services = StringVar(value=data[5])

            # Campos de entrada en la ventana de actualización
            Label(self.update_window, text="Cliente", font=("goudy old style", 15)).place(relx=0.1, rely=0.1)
            Entry(self.update_window, textvariable=self.var_update_client, font=("goudy old style", 15), state="readonly").place(relx=0.4, rely=0.1, relwidth=0.5)

            Label(self.update_window, text="Aparato", font=("goudy old style", 15)).place(relx=0.1, rely=0.2)
            Entry(self.update_window, textvariable=self.var_update_device, font=("goudy old style", 15)).place(relx=0.4, rely=0.2, relwidth=0.5)

            Label(self.update_window, text="Estado", font=("goudy old style", 15)).place(relx=0.1, rely=0.3)
            self.cmb_update_status = ttk.Combobox(self.update_window, textvariable=self.var_update_status, values=("Por hacer", "En proceso", "Terminado"),
                                                  state="readonly", font=("goudy old style", 15))
            self.cmb_update_status.place(relx=0.4, rely=0.3, relwidth=0.5)

            Label(self.update_window, text="Detalles", font=("goudy old style", 15)).place(relx=0.1, rely=0.4)
            Entry(self.update_window, textvariable=self.var_update_details, font=("goudy old style", 15)).place(relx=0.4, rely=0.4, relwidth=0.5)

            Label(self.update_window, text="Servicios", font=("goudy old style", 15)).place(relx=0.1, rely=0.5)

            # Canvas y Scrollbar para los Checkbuttons de servicios
            self.services_canvas = Canvas(self.update_window, bg="white")
            self.services_scrollbar = Scrollbar(self.update_window, orient=VERTICAL, command=self.services_canvas.yview)
            self.services_frame = Frame(self.services_canvas, bg="white")

            self.services_frame.bind(
                "<Configure>",
                lambda e: self.services_canvas.configure(
                    scrollregion=self.services_canvas.bbox("all")
                )
            )

            self.services_canvas.create_window((0, 0), window=self.services_frame, anchor="nw")
            self.services_canvas.configure(yscrollcommand=self.services_scrollbar.set)

            self.services_canvas.place(relx=0.4, rely=0.5, relwidth=0.45, relheight=0.3)
            self.services_scrollbar.place(relx=0.85, rely=0.5, relheight=0.3)

            # Cargar servicios y crear Checkbuttons
            self.service_vars = {}
            cur.execute("SELECT id, name FROM services")
            services = cur.fetchall()
            selected_services = data[5].split(", ") if data[5] else []

            for service in services:
                var = IntVar(value=1 if service[1] in selected_services else 0)
                chk = Checkbutton(self.services_frame, text=service[1], variable=var, bg="white", font=("goudy old style", 12))
                chk.pack(anchor="w")
                self.service_vars[service[0]] = var

            Button(self.update_window, text="Guardar", command=lambda: self.save_update(order_id), font=("goudy old style", 15, "bold"),
                   bg="#13278f", fg="white", cursor="hand2").place(relx=0.3, rely=0.85, relwidth=0.4, height=35)
        except Exception as ex:
            messagebox.showerror("Error", f"Error al cargar datos del pedido: {str(ex)}")
        finally:
            con.close()

    def save_update(self, order_id):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            # Actualizar pedido
            cur.execute("""
                UPDATE orders
                SET device = ?, status = ?, details = ?
                WHERE id = ?
            """, (self.var_update_device.get(), self.var_update_status.get(), self.var_update_details.get(), order_id))

            # Actualizar servicios del pedido
            cur.execute("DELETE FROM order_services WHERE order_id = ?", (order_id,))
            for service_id, var in self.service_vars.items():
                if var.get() == 1:
                    cur.execute("INSERT INTO order_services (order_id, service_id) VALUES (?, ?)", (order_id, service_id))

            con.commit()
            messagebox.showinfo("Éxito", "Pedido actualizado correctamente")
            self.update_window.destroy()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error al actualizar pedido: {str(ex)}")
        finally:
            con.close()

    def delete(self, order_id):
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este pedido?"):
            con = sqlite3.connect(database=r'tbs.db')
            cur = con.cursor()
            try:
                cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
                con.commit()
                messagebox.showinfo("Éxito", "Pedido eliminado correctamente")
                self.show()
            except Exception as ex:
                messagebox.showerror("Error", f"Error al eliminar pedido: {str(ex)}")
            finally:
                con.close()

if __name__ == "__main__":
    root = Tk()
    obj = OrderListClass(root)
    root.mainloop()