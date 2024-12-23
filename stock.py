from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class stockClass:
    def __init__(self, container):
        self.container = container
        self.container.config(bg="#cae6fa")     

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_pid = StringVar()
        self.var_hsncode = StringVar()
        self.sup_list = []
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()

        self.font_sizes = {
            "title_font": 22,
            "label_font": 20,
            "entry_font": 14,
            "button_font": 17,
            "table_font": 12
        }

        # Frame para Productos
        self.stock_Frame = Frame(self.container, bd=3, relief=RIDGE, bg="#bde3ff")
        self.stock_Frame.place(relx=0.01, rely=0.02, relwidth=0.4, relheight=0.8)

        self.title = Label(self.stock_Frame, text="Productos", font=("goudy old style", self.font_sizes["title_font"], "bold"), bg="#13278f", fg="white", bd=3)
        self.title.pack(side=TOP, fill=X)

        # Labels y Entradas
        self.lbl_item_name = Label(self.stock_Frame, text="Nombre", font=("goudy old style", self.font_sizes["label_font"], "bold"), bg="#bde3ff")
        self.lbl_price = Label(self.stock_Frame, text="Precio", font=("goudy old style", self.font_sizes["label_font"], "bold"), bg="#bde3ff")
        self.lbl_qty = Label(self.stock_Frame, text="Cantidad", font=("goudy old style", self.font_sizes["label_font"], "bold"), bg="#bde3ff")

        self.txt_name = Entry(self.stock_Frame, textvariable=self.var_name, font=("goudy old style", self.font_sizes["entry_font"]), bg="white")
        self.txt_price = Entry(self.stock_Frame, textvariable=self.var_price, font=("goudy old style", self.font_sizes["entry_font"]), bg="white")
        self.txt_qty = Entry(self.stock_Frame, textvariable=self.var_qty, font=("goudy old style", self.font_sizes["entry_font"]), bg="white")

        # Botones
        self.btn_add = Button(self.stock_Frame, text="Guardar", command=self.add, font=("goudy old style", self.font_sizes["button_font"]), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_update = Button(self.stock_Frame, text="Modificar", command=self.update, font=("goudy old style", self.font_sizes["button_font"]), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_delete = Button(self.stock_Frame, text="Borrar", command=self.delete, font=("goudy old style", self.font_sizes["button_font"]), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_clear = Button(self.stock_Frame, text="Limpiar", command=self.clear, font=("goudy old style", self.font_sizes["button_font"]), bg="#13278f", fg="white", bd=3, cursor="hand2")

        # Ubicaciones relativas
        self.lbl_item_name.place(relx=0.05, rely=0.2, relwidth=0.3)
        self.lbl_price.place(relx=0.05, rely=0.3, relwidth=0.3)
        self.lbl_qty.place(relx=0.05, rely=0.4, relwidth=0.3)

        self.txt_name.place(relx=0.4, rely=0.2, relwidth=0.5)
        self.txt_price.place(relx=0.4, rely=0.3, relwidth=0.5)
        self.txt_qty.place(relx=0.4, rely=0.4, relwidth=0.5)

        self.btn_add.place(relx=0.05, rely=0.85, relwidth=0.2, relheight=0.1)
        self.btn_update.place(relx=0.3, rely=0.85, relwidth=0.2, relheight=0.1)
        self.btn_delete.place(relx=0.55, rely=0.85, relwidth=0.2, relheight=0.1)
        self.btn_clear.place(relx=0.8, rely=0.85, relwidth=0.2, relheight=0.1)

        # search Frame
        self.search_frame = Frame(self.container, bd=3, relief=RIDGE, bg="#bde3ff")
        self.search_frame.place(relx=0.43, rely=0.02, relwidth=0.55, relheight=0.15)

        self.search_title = Label(self.search_frame, text="Buscar Producto", font=("goudy old style", self.font_sizes["title_font"], "bold"), bg="#13278f", fg="white", bd=3)
        self.search_title.pack(side=TOP, fill=X)

        # options
        self.cmb_search = ttk.Combobox(self.search_frame, textvariable=self.var_searchby, values=("Seleccionar", "Nombre", "Precio","cantidad"), state='readonly', justify=CENTER, font=("goudy old style", self.font_sizes["entry_font"]))
        self.cmb_search.place(relx=0.02, rely=0.5, relwidth=0.2)
        self.cmb_search.current(0)

        self.txt_search = Entry(self.search_frame, textvariable=self.var_searchtxt, font=("goudy old style", self.font_sizes["entry_font"]), bg="white", bd=3)
        self.txt_search.place(relx=0.25, rely=0.5, relwidth=0.4)

        self.btn_search = Button(self.search_frame, text="Buscar", command=self.search, font=("goudy old style", self.font_sizes["button_font"], "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_search.place(relx=0.67, rely=0.5, relwidth=0.15, relheight=0.4)

        self.btn_clear_search = Button(self.search_frame, text="Limpiar", command=self.clear_search, font=("goudy old style", self.font_sizes["button_font"], "bold"),
                        bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_clear_search.place(relx=0.83, rely=0.5, relwidth=0.15, relheight=0.4)

        # Tabla de stock
        self.s_Frame = Frame(self.container, bd=3, relief=RIDGE)
        self.s_Frame.place(relx=0.43, rely=0.2, relwidth=0.55, relheight=0.75)

        self.scrolly = Scrollbar(self.s_Frame, orient=VERTICAL)
        self.scrollx = Scrollbar(self.s_Frame, orient=HORIZONTAL)

        self.StockTable = ttk.Treeview(self.s_Frame, columns=("pid", "itemname", "price", "qty"), yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.scrollx.pack(side=BOTTOM, fill=X)
        self.scrolly.pack(side=RIGHT, fill=Y)
        self.scrollx.config(command=self.StockTable.xview)
        self.scrolly.config(command=self.StockTable.yview)

        self.StockTable.heading("pid", text="Id")
        self.StockTable.heading("itemname", text="Nombre")
        self.StockTable.heading("price", text="Precio")
        self.StockTable.heading("qty", text="Cantidad")

        self.StockTable["show"] = "headings"

        self.StockTable.column("pid", width=90)
        self.StockTable.column("itemname", width=100)
        self.StockTable.column("price", width=100)
        self.StockTable.column("qty", width=100)
        self.StockTable.pack(fill=BOTH, expand=1)

        self.container.bind("<Configure>", self.on_resize)
        self.StockTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()
    
    def on_resize(self, event):
        """Ajusta dinámicamente el tamaño del texto."""
        new_width = event.width

        # Escalar tamaños de fuente proporcionalmente
        self.font_sizes["title_font"] = int(new_width / 50)
        self.font_sizes["label_font"] = int(new_width / 60)
        self.font_sizes["entry_font"] = int(new_width / 90)
        self.font_sizes["button_font"] = int(new_width / 100)
        self.font_sizes["table_font"] = int(new_width / 110)

        # Actualizar fuentes
        self.title.config(font=("goudy old style", self.font_sizes["title_font"], "bold"))
        self.search_title.config(font=("goudy old style", self.font_sizes["title_font"], "bold"))

        for widget in [self.lbl_item_name, self.lbl_price, self.lbl_qty, self.btn_add, self.btn_update, self.btn_delete, self.btn_clear, self.btn_search, self.btn_clear_search]:
            widget.config(font=("goudy old style", self.font_sizes["label_font"]))

        self.txt_name.config(font=("goudy old style", self.font_sizes["entry_font"]))
        self.txt_price.config(font=("goudy old style", self.font_sizes["entry_font"]))
        self.txt_qty.config(font=("goudy old style", self.font_sizes["entry_font"]))
        self.cmb_search.config(font=("goudy old style", self.font_sizes["entry_font"]))
        self.txt_search.config(font=("goudy old style", self.font_sizes["entry_font"]))

    def show(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:

            cur.execute("SELECT pid, itemname, price, qty FROM stock")
            rows = cur.fetchall()
            self.StockTable.delete(*self.StockTable.get_children())
            for row in rows:
                self.StockTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)} ", parent=self.container)

    def get_data(self, ev):
        f = self.StockTable.focus()
        content = (self.StockTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])  
        self.var_name.set(row[1])       
        self.var_price.set(row[2])      
        self.var_qty.set(row[3])     

    def add(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            if self.var_sup.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "Llena todo los campos", parent=self.container)
            else:
                cur.execute("Select * from stock where itemname=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Producto ya existe, crea otro", parent=self.container)
                else:
                    cur.execute("Insert into stock (itemname, price, qty) values(?,?,?)", (
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Exito", "Producto agregado correctamente", parent=self.container)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)} ", parent=self.container)   


    def update(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":  
                messagebox.showerror("Error", "Selecciona un producto de la lista", parent=self.container)
            else:
                cur.execute("Select * from stock where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Producto no encontrado, selecciona de la lista", parent=self.container)
                else:
   
                    cur.execute("Update stock set itemname=?, price=?, qty=? where pid=?", (
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Éxito", "Producto actualizado correctamente", parent=self.container)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error debido a: {str(ex)}", parent=self.container)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Seleciona un producto de la lista", parent=self.container)
            else:
                cur.execute("Delete from stock where pid=?", (self.var_pid.get(),))
                con.commit()
                messagebox.showinfo("Exito", "Producto borrado correctamente", parent=self.container)
                self.show()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)} ", parent=self.container)

    def clear(self):
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")

    def search(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:

            search_by = self.var_searchby.get()
            search_txt = self.var_searchtxt.get()

   
            if search_by == "Seleccionar":
                messagebox.showerror("Error", "Seleccione un criterio de búsqueda", parent=self.container)
                return


            query = None
            if search_by == "Nombre":
                query = "SELECT pid, itemname, price, qty FROM stock WHERE itemname LIKE ?"
            elif search_by == "Precio":
                query = "SELECT pid, itemname, price, qty FROM stock WHERE price LIKE ?"
            elif search_by == "Cantidad":
                query = "SELECT pid, itemname, price, qty FROM stock WHERE qty LIKE ?"

            if query:
  
                cur.execute(query, (f"%{search_txt}%",))


            rows = cur.fetchall()


            self.StockTable.delete(*self.StockTable.get_children())

  
            for row in rows:
                self.StockTable.insert('', END, values=row)


            if not rows:
                messagebox.showinfo("Sin Resultados", "No se encontraron coincidencias con los criterios de búsqueda", parent=self.container)

            con.commit()

        except Exception as ex:
            messagebox.showerror("Error", f"Error debido a: {str(ex)}", parent=self.container)
        finally:
            con.close()

    def clear_search(self):
        """Limpia el filtro de búsqueda y el campo de texto."""
        self.var_searchby.set("Seleccionar")
        self.var_searchtxt.set("")
        self.show()


if __name__ == "__main__":
    root = Tk()
    obj = stockClass(root)
    root.mainloop()