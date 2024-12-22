from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class ClientClass:
    def __init__(self, container):
        self.container = container
        self.container.config(bg="#bde3ff")
        
        # All Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()

        # Estilo base de las fuentes
        self.base_font_size = 14
        self.font_styles = {
            "title": ("goudy old style", self.base_font_size + 11, "bold"),
            "label": ("goudy old style", self.base_font_size),
            "entry": ("goudy old style", self.base_font_size),
            "button": ("goudy old style", self.base_font_size),
            "combo": ("goudy old style", self.base_font_size)
        }

        # BUSCAR
        SearchFrame = LabelFrame(self.container, text="Buscar Usuario", font=self.font_styles["label"], bg="#bde3ff", bd=3)
        SearchFrame.place(relx=0.25, rely=0.06, relwidth=0.5, relheight=0.12)

        # OPCIONES DE BUSCAR
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,
                                  values=("Seleccionar", "Correo Electrónico", "Nombre", "Telefono"),
                                  state='readonly', justify=CENTER, font=self.font_styles["combo"])
        cmb_search.place(relx=0.02, rely=0.2, relwidth=0.3)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=self.font_styles["entry"], bg="white", bd=3)
        txt_search.place(relx=0.35, rely=0.15, relwidth=0.32, relheight=0.55)

        btn_search = Button(SearchFrame, text="Buscar", command=self.search, font=self.font_styles["button"],
                            bg="#13278f", fg="#bde3ff", bd=3, cursor="hand2")
        btn_search.place(relx=0.7, rely=0.1, relwidth=0.12, relheight=0.6)
        btn_search.bind("<Enter>", self.on_enter)
        btn_search.bind("<Leave>", self.on_leave)

        # Botón Limpiar
        btn_clear_search = Button(SearchFrame, text="Limpiar", command=self.clear_search, font=self.font_styles["button"],
                                bg="#13278f", fg="#bde3ff", bd=3, cursor="hand2")
        btn_clear_search.place(relx=0.85, rely=0.1, relwidth=0.12, relheight=0.6)
        btn_clear_search.bind("<Enter>", self.on_enter)
        btn_clear_search.bind("<Leave>", self.on_leave)

        # MENU DE CLIENTES (PARTE DE ARRIBA)
        title = Label(self.container, text="Clientes/Usuarios", font=self.font_styles["title"],
                      bg="#13278f", fg="#bde3ff", bd=3)
        title.place(relx=0.2, rely=0.01, relwidth=0.6, relheight=0.05)

        # Formulario
        lbl_name = Label(self.container, text="Nombre", font=self.font_styles["label"], bg="#bde3ff")
        lbl_name.place(relx=0.05, rely=0.2)
        txt_name = Entry(self.container, textvariable=self.var_name, font=self.font_styles["entry"], bg="white")
        txt_name.place(relx=0.15, rely=0.2, relwidth=0.25)

        lbl_contact = Label(self.container, text="Teléfono", font=self.font_styles["label"], bg="#bde3ff")
        lbl_contact.place(relx=0.45, rely=0.2)
        txt_contact = Entry(self.container, textvariable=self.var_contact, font=self.font_styles["entry"], bg="white")
        txt_contact.place(relx=0.55, rely=0.2, relwidth=0.25)

        lbl_email = Label(self.container, text="Email", font=self.font_styles["label"], bg="#bde3ff")
        lbl_email.place(relx=0.05, rely=0.27)
        txt_email = Entry(self.container, textvariable=self.var_email, font=self.font_styles["entry"], bg="white")
        txt_email.place(relx=0.15, rely=0.27, relwidth=0.25)

        lbl_pass = Label(self.container, text="Clave", font=self.font_styles["label"], bg="#bde3ff")
        lbl_pass.place(relx=0.45, rely=0.27)
        txt_pass = Entry(self.container, textvariable=self.var_pass, font=self.font_styles["entry"], bg="white")
        txt_pass.place(relx=0.55, rely=0.27, relwidth=0.25)

        lbl_utype = Label(self.container, text="Rol", font=self.font_styles["label"], bg="#bde3ff")
        lbl_utype.place(relx=0.05, rely=0.34)
        cmb_utype = ttk.Combobox(self.container, textvariable=self.var_utype, values=("Cliente", "Administrador"),
                                  state='readonly', justify=CENTER, font=self.font_styles["combo"])
        cmb_utype.place(relx=0.15, rely=0.34, relwidth=0.25)
        cmb_utype.current(0)

        # Botones
        btn_add = Button(self.container, text="Guardar", command=self.add, font=self.font_styles["button"],
                         bg="#13278f", fg="#bde3ff", bd=3, cursor="hand2")
        btn_add.place(relx=0.05, rely=0.45, relwidth=0.18, relheight=0.05)
        btn_add.bind("<Enter>", self.on_enter)
        btn_add.bind("<Leave>", self.on_leave)

        btn_update = Button(self.container, text="Modificar", command=self.update, font=self.font_styles["button"],
                            bg="#13278f", fg="#bde3ff", bd=3, cursor="hand2")
        btn_update.place(relx=0.28, rely=0.45, relwidth=0.18, relheight=0.05)
        btn_update.bind("<Enter>", self.on_enter)
        btn_update.bind("<Leave>", self.on_leave)

        btn_delete = Button(self.container, text="Borrar", command=self.delete, font=self.font_styles["button"],
                            bg="#13278f", fg="#bde3ff", bd=3, cursor="hand2")
        btn_delete.place(relx=0.53, rely=0.45, relwidth=0.18, relheight=0.05)
        btn_delete.bind("<Enter>", self.on_enter)
        btn_delete.bind("<Leave>", self.on_leave)

        btn_clear = Button(self.container, text="Limpiar", command=self.clear, font=self.font_styles["button"],
                           bg="#13278f", fg="#bde3ff", bd=3, cursor="hand2")
        btn_clear.place(relx=0.78, rely=0.45, relwidth=0.18, relheight=0.05)
        btn_clear.bind("<Enter>", self.on_enter)
        btn_clear.bind("<Leave>", self.on_leave)

        # Tabla de datos
        emp_frame = Frame(self.container, bd=3, relief=RIDGE, bg="#bde3ff")
        emp_frame.place(relx=0.05, rely=0.55, relwidth=0.9, relheight=0.4)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("eid", "name", "email", "contact", "pass", "utype"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.config(command=self.EmployeeTable.yview)
        scrollx.config(command=self.EmployeeTable.xview)
        self.EmployeeTable.pack(fill=BOTH, expand=1)

        self.EmployeeTable.heading("eid", text="ID")
        self.EmployeeTable.heading("name", text="Nombre")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("contact", text="Teléfono")
        self.EmployeeTable.heading("pass", text="Clave")
        self.EmployeeTable.heading("utype", text="Rol")
        self.EmployeeTable["show"] = "headings"

        # Vincular el evento de clic en la tabla a la función get_data
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    def on_enter(self, event):
        event.widget.config(bg="#0d2abf")

    def on_leave(self, event):
        event.widget.config(bg="#13278f")

    #=======================================================================================

    def on_resize(self, event):
        """Ajusta dinámicamente las fuentes al redimensionar el contenedor."""
        width = event.width
        new_font_size = max(10, int(width / 80))  # Ajusta este factor para controlar el tamaño
        self.font_styles["title"] = ("goudy old style", new_font_size + 11, "bold")
        self.font_styles["label"] = ("goudy old style", new_font_size)
        self.font_styles["entry"] = ("goudy old style", new_font_size)
        self.font_styles["button"] = ("goudy old style", new_font_size)
        self.font_styles["combo"] = ("goudy old style", new_font_size)

        # Actualizar las fuentes
        for widget in self.container.winfo_children():
            if isinstance(widget, (Label, Button, Entry, ttk.Combobox, LabelFrame)):
                widget.config(font=self.font_styles.get("label", ("Arial", 12)))

    def validate_fields(self):
        # Validar si el campo de nombre está vacío
        if self.var_name.get().strip() == "":
            messagebox.showerror("Error", "El campo de nombre no puede estar vacío", parent=self.container)
            return False

        # Verificar si el rol es "Administrador" y la contraseña está vacía
        if self.var_utype.get() == "Administrador" and self.var_pass.get().strip() == "":
            messagebox.showerror("Error", "La contraseña es obligatoria para el rol de Administrador", parent=self.container)
            return False

        return True

    def add(self):
        if not self.validate_fields():
            return

        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            # Verificar si el nombre ya existe
            cur.execute("SELECT * FROM client WHERE name = ?", (self.var_name.get(),))
            existing_client = cur.fetchone()

            if existing_client:
                messagebox.showerror("Error", "El nombre del cliente ya existe. Por favor, use uno diferente.", parent=self.container)
                return

            cur.execute("INSERT INTO client (name, email, contact, pass, utype) VALUES (?, ?, ?, ?, ?)", (
                self.var_name.get(),
                self.var_email.get(),
                self.var_contact.get(),
                self.var_pass.get(),
                self.var_utype.get(),
            ))
            con.commit()
            messagebox.showinfo("Éxito", "Los datos fueron guardados con éxito", parent=self.container)
            self.show()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error debido a: {str(ex)}", parent=self.container)

    def show(self):
        con = sqlite3.connect(database='tbs.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT eid, name, email, contact, pass, utype FROM client")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
            con.commit()
        except Exception as ex:
            messagebox.showerror("Error", f"Error debido a: {str(ex)}", parent=self.container)

        #obtener data
    def get_data(self, event):
        current_row = self.EmployeeTable.focus()
        content = self.EmployeeTable.item(current_row)
        row = content['values']

  
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_contact.set(row[3])
        self.var_pass.set(row[4])
        self.var_utype.set(row[5])

    def update(self):
        if not self.validate_fields():
            return

        con = sqlite3.connect(database='tbs.db')
        cur = con.cursor()
        try:
            # Verificar si el cliente existe
            cur.execute("SELECT * FROM client WHERE name = ?", (self.var_name.get(),))
            existing_client = cur.fetchone()

            if not existing_client:
                messagebox.showerror("Error", "El cliente no existe. Por favor, verifique el nombre.", parent=self.container)
                return

            cur.execute("UPDATE client SET email = ?, contact = ?, pass = ?, utype = ? WHERE name = ?", (
                self.var_email.get(),
                self.var_contact.get(),
                self.var_pass.get(),
                self.var_utype.get(),
                self.var_name.get(),
            ))
            con.commit()
            messagebox.showinfo("Éxito", "Los datos fueron actualizados con éxito", parent=self.container)
            self.show()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error debido a: {str(ex)}", parent=self.container)

    def delete(self):
        con = sqlite3.connect(database='tbs.db')
        cur = con.cursor()
        try:
            current_row = self.EmployeeTable.focus()
            content = self.EmployeeTable.item(current_row)
            row = content['values']

            if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este usuario?", parent=self.container):
                cur.execute("DELETE FROM client WHERE eid=?", (row[0],))  # Use the ID from the selected row
                con.commit()
                messagebox.showinfo("Correcto", "Usuario eliminado correctamente", parent=self.container)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.container)

    def clear(self):
        self.var_name.set("")
        self.var_email.set("")
        self.var_contact.set("")
        self.var_pass.set("")
        self.var_utype.set("Administrador")


        #buscar data
    def search(self):
        con = sqlite3.connect(database='tbs.db')
        cur = con.cursor()
        try:
            search_by = self.var_searchby.get()
            search_txt = self.var_searchtxt.get()
            if search_by == "Seleccionar":
                messagebox.showerror("Error", "Seleccione un criterio de búsqueda", parent=self.container)
                return

            query = None
            # Construir la consulta con LIKE
            if search_by == "Correo Electrónico":
                query = "SELECT eid, name, email, contact, pass, utype FROM client WHERE email LIKE ?"
            elif search_by == "Nombre":
                query = "SELECT eid, name, email, contact, pass, utype FROM client WHERE name LIKE ?"
            elif search_by == "Telefono":
                query = "SELECT eid, name, email, contact, pass, utype FROM client WHERE contact LIKE ?"

            if query:
                cur.execute(query, (f"%{search_txt}%",))  # Usa '%' antes y después para buscar contenido parcial

            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                # Mostrar la contraseña como asteriscos si se desea
                self.EmployeeTable.insert('', END, values=(row[0], row[1], row[2], row[3], "******", row[5]))
            con.commit()

            if not rows:
                messagebox.showinfo("Sin Resultados", "No se encontraron usuarios con los criterios de búsqueda", parent=self.container)

        except Exception as ex:
            messagebox.showerror("Error", f"Error debido a: {str(ex)}", parent=self.container)

    def clear_search(self):
        """Limpia el filtro de búsqueda y el campo de texto."""
        self.var_searchby.set("Seleccionar")
        self.var_searchtxt.set("")
        self.show()

if __name__ == "__main__":
    root = Tk()
    obj = ClientClass(root)
    root.mainloop()