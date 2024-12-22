from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class OrderListClass:
    def __init__(self, container):
        self.container = container

        # Título
        self.title = Label(self.container, text="Lista de Pedidos", font=("goudy old style", 25, "bold"),
                           bg="#13278f", fg="white", bd=3)
        self.title.pack(side=TOP, fill=X)

        # Frame para la lista de pedidos
        self.order_frame = Frame(self.container, bd=3, relief=RIDGE)
        self.order_frame.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.8)

        self.show()

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

            # Limpia el frame antes de llenarlo nuevamente
            for widget in self.order_frame.winfo_children():
                widget.destroy()

            # Rellena el frame con los datos obtenidos
            for row in rows:
                self.create_order_frame(row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error al mostrar datos: {str(ex)}")
        finally:
            con.close()

    def create_order_frame(self, order_data):
        order_id, client_name, device, status, service_name = order_data

        frame = Frame(self.order_frame, bd=2, relief=RIDGE, bg="white")
        frame.pack(fill=X, pady=5, padx=10)

        lbl_client = Label(frame, text=client_name, font=("goudy old style", 15, "bold"), bg="white", anchor="w")
        lbl_client.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        lbl_device = Label(frame, text=device, font=("goudy old style", 12), bg="white", anchor="w")
        lbl_device.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        btn_edit = Button(frame, text="Editar", command=lambda: self.update(order_id), font=("goudy old style", 12, "bold"),
                          bg="#13278f", fg="white", cursor="hand2")
        btn_edit.grid(row=0, column=1, padx=10, pady=5)

        btn_delete = Button(frame, text="Eliminar", command=lambda: self.delete(order_id), font=("goudy old style", 12, "bold"),
                            bg="#13278f", fg="white", cursor="hand2")
        btn_delete.grid(row=1, column=1, padx=10, pady=5)

    def update(self, order_id):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT o.id, c.name AS client_name, o.device, o.status, s.name AS service_name
                FROM orders o
                JOIN client c ON o.client_id = c.eid
                JOIN services s ON o.service_id = s.id
                WHERE o.id = ?
            """, (order_id,))
            data = cur.fetchone()
            if not data:
                messagebox.showerror("Error", "Pedido no encontrado")
                return

            # Crear una nueva ventana para actualizar el pedido
            self.update_window = Toplevel(self.container)
            self.update_window.title("Modificar Pedido")
            self.update_window.geometry("400x400")

            # Variables para la ventana de actualización
            self.var_update_client = StringVar(value=data[1])
            self.var_update_device = StringVar(value=data[2])
            self.var_update_status = StringVar(value=data[3])
            self.var_update_service = StringVar(value=data[4])

            # Campos de entrada en la ventana de actualización
            Label(self.update_window, text="Cliente", font=("goudy old style", 15)).place(relx=0.1, rely=0.1)
            Entry(self.update_window, textvariable=self.var_update_client, font=("goudy old style", 15), state="readonly").place(relx=0.4, rely=0.1, relwidth=0.5)

            Label(self.update_window, text="Aparato", font=("goudy old style", 15)).place(relx=0.1, rely=0.2)
            Entry(self.update_window, textvariable=self.var_update_device, font=("goudy old style", 15)).place(relx=0.4, rely=0.2, relwidth=0.5)

            Label(self.update_window, text="Estado", font=("goudy old style", 15)).place(relx=0.1, rely=0.3)
            ttk.Combobox(self.update_window, textvariable=self.var_update_status, values=("Por hacer", "En proceso", "Terminado"),
                         state="readonly", font=("goudy old style", 15)).place(relx=0.4, rely=0.3, relwidth=0.5)

            Label(self.update_window, text="Servicio", font=("goudy old style", 15)).place(relx=0.1, rely=0.4)
            Entry(self.update_window, textvariable=self.var_update_service, font=("goudy old style", 15), state="readonly").place(relx=0.4, rely=0.4, relwidth=0.5)

            Button(self.update_window, text="Guardar", command=lambda: self.save_update(order_id), font=("goudy old style", 15, "bold"),
                   bg="#13278f", fg="white", cursor="hand2").place(relx=0.3, rely=0.6, relwidth=0.4, height=35)
        except Exception as ex:
            messagebox.showerror("Error", f"Error al cargar datos del pedido: {str(ex)}")
        finally:
            con.close()

    def save_update(self, order_id):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE orders
                SET device = ?, status = ?
                WHERE id = ?
            """, (self.var_update_device.get(), self.var_update_status.get(), order_id))
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