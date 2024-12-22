from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class ServiceClass:
    def __init__(self, container):
        self.container = container
        self.container.config(bg="#bde3ff")

        # All Variables
        self.var_searchtxt = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_estimated_time = StringVar()

        self.font_sizes = {
            "title_font": 20,
            "label_font": 14,
            "entry_font": 14,
            "button_font": 12,
            "table_font": 12
        }

        # Título
        self.lbl_title = Label(self.container, text="Detalles del Servicio", font=("goudy old style", self.font_sizes["title_font"], "bold"),
                               bg="#13278f", fg="white")
        self.lbl_title.place(relx=0.05, rely=0.02, relwidth=0.9, relheight=0.08)

        # Buscar servicio
        self.lbl_search = Label(self.container, text="Buscar Servicio por nombre", bg="#bde3ff",
                        font=("goudy old style", self.font_sizes["label_font"]))
        self.lbl_search.place(relx=0.55, rely=0.12, relwidth=0.25, relheight=0.05)
        self.txt_search = Entry(self.container, textvariable=self.var_searchtxt, font=("goudy old style", self.font_sizes["entry_font"]), bg="white", bd=3)
        self.txt_search.place(relx=0.76, rely=0.12, relwidth=0.1, relheight=0.05)
        self.btn_search = Button(self.container, text="Buscar", command=self.search, font=("goudy old style", self.font_sizes["button_font"], "bold"),
                                  bg="#13278f", fg="white", cursor="hand2")
        self.btn_search.place(relx=0.87, rely=0.12, relwidth=0.08, relheight=0.05)

        # Formulario
        self.lbl_name = Label(self.container, text="Nombre", font=self.font_sizes["label_font"], bg="#bde3ff")
        self.lbl_name.place(relx=0.05, rely=0.2)
        self.txt_name = Entry(self.container, textvariable=self.var_name, font=self.font_sizes["entry_font"], bg="white")
        self.txt_name.place(relx=0.15, rely=0.2, relwidth=0.25)

        self.lbl_price = Label(self.container, text="Precio", font=self.font_sizes["label_font"], bg="#bde3ff")
        self.lbl_price.place(relx=0.05, rely=0.3)
        self.txt_price = Entry(self.container, textvariable=self.var_price, font=self.font_sizes["entry_font"], bg="white")
        self.txt_price.place(relx=0.15, rely=0.3, relwidth=0.25)

        self.lbl_duration = Label(self.container, text="Duración", font=self.font_sizes["label_font"], bg="#bde3ff")
        self.lbl_duration.place(relx=0.05, rely=0.4)
        self.txt_duration = Entry(self.container, textvariable=self.var_estimated_time, font=self.font_sizes["entry_font"], bg="white")
        self.txt_duration.place(relx=0.15, rely=0.4, relwidth=0.25)

        # Botones
        self.btn_save = Button(self.container, text="Guardar", command=self.add, font=("goudy old style", self.font_sizes["button_font"]),
                               bg="#13278f", fg="white", cursor="hand2")
        self.btn_save.place(relx=0.05, rely=0.5, relwidth=0.1, relheight=0.06)
        self.btn_update = Button(self.container, text="Actualizar", command=self.update, font=("goudy old style", self.font_sizes["button_font"]),
                                 bg="#13278f", fg="white", cursor="hand2")
        self.btn_update.place(relx=0.17, rely=0.5, relwidth=0.1, relheight=0.06)
        self.btn_delete = Button(self.container, text="Eliminar", command=self.delete, font=("goudy old style", self.font_sizes["button_font"]),
                                 bg="#13278f", fg="white", cursor="hand2")
        self.btn_delete.place(relx=0.29, rely=0.5, relwidth=0.1, relheight=0.06)
        self.btn_clear = Button(self.container, text="Limpiar", command=self.clear, font=("goudy old style", self.font_sizes["button_font"]),
                                bg="#13278f", fg="white", cursor="hand2")
        self.btn_clear.place(relx=0.41, rely=0.5, relwidth=0.1, relheight=0.06)

        # Detalles de Servicios
        services_frame = Frame(self.container, bd=3, relief=RIDGE)
        services_frame.place(relx=0.6, rely=0.2, relwidth=0.35, relheight=0.6)

        scrolly = Scrollbar(services_frame, orient=VERTICAL)
        scrollx = Scrollbar(services_frame, orient=HORIZONTAL)

        self.servicesTable = ttk.Treeview(services_frame, columns=("id", "name", "price", "estimated_time"),
                                        yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.servicesTable.xview)
        scrolly.config(command=self.servicesTable.yview)

        self.servicesTable.heading("id", text="ID")
        self.servicesTable.heading("name", text="Nombre")
        self.servicesTable.heading("price", text="Precio")
        self.servicesTable.heading("estimated_time", text="Tiempo Estimado")

        self.servicesTable["show"] = "headings"
        self.servicesTable.pack(fill=BOTH, expand=1)
        self.servicesTable.bind("<ButtonRelease-1>", self.get_data)

        # Ajustar el tamaño de las columnas
        self.servicesTable.column("id", width=50)
        self.servicesTable.column("name", width=150)
        self.servicesTable.column("price", width=100)
        self.servicesTable.column("estimated_time", width=150)

        # Cargar los servicios 
        self.show_services()

        # Vincular evento de redimensionamiento
        self.container.bind("<Configure>", self.on_resize)

    def create_label_entry(self, label_text, variable, relx, rely):
        """Crea un par de Label y Entry de forma dinámica."""
        Label(self.container, text=label_text, font=("goudy old style", self.font_sizes["label_font"]), bg="white"
            ).place(relx=relx, rely=rely, relwidth=0.15, relheight=0.05)
        Entry(self.container, textvariable=variable, font=("ARIEL", self.font_sizes["entry_font"]), bg="white"
            ).place(relx=relx + 0.15, rely=rely, relwidth=0.35, relheight=0.05)

    def on_resize(self, event):
        """Ajusta dinámicamente las fuentes y el diseño al redimensionar el contenedor."""
        new_width = event.width

        # Escalar tamaños de fuente proporcionalmente
        self.font_sizes["title_font"] = int(new_width / 50)
        self.font_sizes["label_font"] = int(new_width / 80)
        self.font_sizes["entry_font"] = int(new_width / 90)
        self.font_sizes["button_font"] = int(new_width / 100)
        self.font_sizes["table_font"] = int(new_width / 110)

        # Actualizar fuentes
        self.lbl_title.config(font=("goudy old style", self.font_sizes["title_font"], "bold"))
        self.txt_search.config(font=("goudy old style", self.font_sizes["entry_font"]))
        self.btn_search.config(font=("goudy old style", self.font_sizes["button_font"], "bold"))
        self.btn_save.config(font=("goudy old style", self.font_sizes["button_font"]))
        self.btn_update.config(font=("goudy old style", self.font_sizes["button_font"]))
        self.btn_delete.config(font=("goudy old style", self.font_sizes["button_font"]))
        self.btn_clear.config(font=("goudy old style", self.font_sizes["button_font"]))
        self.lbl_search.config(font=("goudy old style", self.font_sizes["label_font"]))
        self.lbl_name.config(font=("goudy old style", self.font_sizes["label_font"]))
        self.lbl_price.config(font=("goudy old style", self.font_sizes["label_font"]))
        self.lbl_duration.config(font=("goudy old style", self.font_sizes["label_font"]))

        self.txt_name.config(font=("goudy old style", self.font_sizes["entry_font"]))
        self.txt_price.config(font=("goudy old style", self.font_sizes["entry_font"]))
        self.txt_duration.config(font=("goudy old style", self.font_sizes["entry_font"]))

    def get_data(self, event):
        """Rellena los campos de texto al seleccionar un registro de la tabla."""
        selected_row = self.servicesTable.focus()
        data = self.servicesTable.item(selected_row)["values"]
        if data:
            self.var_searchtxt.set(data[0])
            self.var_name.set(data[1])
            self.var_price.set(data[2])
            self.var_estimated_time.set(data[3])

    def add(self):
        conn = sqlite3.connect("tbs.db")
        cur = conn.cursor()

        if self.var_name.get() == "" or self.var_price.get() == "" or self.var_estimated_time.get() == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios", parent=self.container)
            return
        # Verificar si el nombre ya existe
        cur.execute("SELECT * FROM services WHERE name = ?", (self.var_name.get(),))
        existing_service = cur.fetchone()

        if existing_service:
            messagebox.showerror("Error", "El nombre del servicio ya existe. Por favor, use uno diferente.", parent=self.container)
            return

        try:
            cur.execute("INSERT INTO services (name, price, estimated_time) VALUES (?, ?, ?)", (
                
                self.var_name.get(), 
                float(self.var_price.get()), 
                self.var_estimated_time.get()

            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Servicio agregado con éxito", parent=self.container)
            self.show_services()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Ocurrió un error: {str(ex)}", parent=self.container)
        finally:
            conn.close()

    def update(self):
        if self.var_searchtxt.get() == "":
            messagebox.showerror("Error", "Por favor, busca el servicio que deseas actualizar", parent=self.container)
            return
        try:
            conn = sqlite3.connect("tbs.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE services SET name=?, price=?, estimated_time=? WHERE id=?", 
                           (self.var_name.get(), float(self.var_price.get()), self.var_estimated_time.get(), self.var_searchtxt.get()))
            conn.commit()
            messagebox.showinfo("Éxito", "Servicio actualizado con éxito", parent=self.container)
            self.show_services()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Ocurrió un error: {str(ex)}", parent=self.container)
        finally:
            conn.close()

    def delete(self):
        if self.var_searchtxt.get() == "":
            messagebox.showerror("Error", "Por favor, busca el servicio que deseas eliminar", parent=self.container)
            return
        try:
            conn = sqlite3.connect("tbs.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM services WHERE id=?", (self.var_searchtxt.get(),))
            conn.commit()
            messagebox.showinfo("Éxito", "Servicio eliminado con éxito", parent=self.container)
            self.show_services()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Ocurrió un error: {str(ex)}", parent=self.container)
        finally:
            conn.close()

    def clear(self):
        self.var_searchtxt.set("")
        self.var_name.set("")
        self.var_price.set("")
        self.var_estimated_time.set("")

    def search(self):
        if self.var_searchtxt.get() == "":
            # Si el campo de búsqueda está vacío, mostrar todos los servicios
            self.show_services()
            return
        
        try:
            conn = sqlite3.connect("tbs.db")
            cursor = conn.cursor()
            # Usamos LIKE para buscar coincidencias parciales y LOWER para hacerlo insensible al caso
            cursor.execute("SELECT * FROM services WHERE LOWER(name) LIKE LOWER(?)", ('%' + self.var_searchtxt.get() + '%',))
            rows = cursor.fetchall()  # Obtener todas las coincidencias
            if rows:
                self.update_table(rows)  # Actualizamos la tabla con los resultados encontrados
            else:
                # Si no se encuentran coincidencias, mostrar un mensaje y cargar todos los servicios
                messagebox.showerror("Error", "No se encontraron coincidencias", parent=self.container)
                self.show_services()
        except Exception as ex:
            messagebox.showerror("Error", f"Ocurrió un error: {str(ex)}", parent=self.container)
        finally:
            conn.close()

    def update_table(self, rows):
        # Limpiar la tabla antes de insertar nuevas filas
        for row in self.servicesTable.get_children():
            self.servicesTable.delete(row)
        
        # Insertar las filas obtenidas de la búsqueda en la tabla
        for row in rows:
            self.servicesTable.insert("", "end", values=row)

    def show_services(self):
        # Limpiar la tabla antes de insertar todas las filas
        for row in self.servicesTable.get_children():
            self.servicesTable.delete(row)
        
        try:
            conn = sqlite3.connect("tbs.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM services")
            rows = cursor.fetchall()
            for row in rows:
                self.servicesTable.insert("", "end", values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Ocurrió un error: {str(ex)}", parent=self.container)
        finally:
            conn.close()


if __name__ == "__main__":
    root = Tk()
    obj = ServiceClass(root)
    root.mainloop()
