from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import tkinter.ttk as ttk
import sqlite3
import os

class SalesClass:
    def __init__(self, container):
        self.container = container
        self.container.config(bg="white")

        self.widget_sizes = {
            "title_font": 20,
            "label_font": 14,
            "button_font": 12,
            "list_font": 12,
        }

        # Inicialización de bill_list
        self.bill_list = []  # Aquí inicializamos la lista

        # Evento de redimensionamiento
        self.container.bind("<Configure>", self.on_resize)

        self.var_invoice = StringVar()

        # Título
        self.title = Label(self.container, text="Ver facturas de clientes", font=("goudy old style", self.widget_sizes["title_font"], "bold"), bg="#13278f", fg="white")
        self.title.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)

        # Factura
        self.lbl_invoice = Label(self.container, text="Factura No.", font=("goudy old style", self.widget_sizes["label_font"]), bg="white")
        self.lbl_invoice.place(relx=0, rely=0.15, relwidth=0.2, relheight=0.05)

        self.txt_invoice = Entry(self.container, textvariable=StringVar(), font=("goudy old style", self.widget_sizes["label_font"]), bg="white")
        self.txt_invoice.place(relx=0.15, rely=0.15, relwidth=0.4, relheight=0.05)

        self.btn_search = Button(self.container, text="Buscar", font=("goudy old style", self.widget_sizes["button_font"], "bold"), bg="#13278f", fg="white", cursor="hand2")
        self.btn_search.place(relx=0.75, rely=0.15, relwidth=0.10, relheight=0.04)

        self.btn_clear = Button(self.container, text="Limpiar", command=self.clear, font=("goudy old style", self.widget_sizes["button_font"], "bold"), bg="#13278f", fg="white", cursor="hand2")
        self.btn_clear.place(relx=0.85, rely=0.15, relwidth=0.10, relheight=0.04)

        # Lista de facturas
        self.sales_frame = Frame(self.container, bd=3, relief=RIDGE)
        self.sales_frame.place(relx=0.02, rely=0.2, relwidth=0.25, relheight=0.6)

        scrolly = Scrollbar(self.sales_frame, orient=VERTICAL)
        self.sales_list = Listbox(self.sales_frame, font=("goudy old style", self.widget_sizes["list_font"]), 
                                bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH, expand=True)
        self.sales_list.bind("<ButtonRelease-1>", self.get_data)

        # Área de facturas
        self.bill_frame = Frame(self.container, bg="white", relief="ridge", bd=2)
        self.bill_frame.place(relx=0.35, rely=0.25, relwidth=0.6, relheight=0.6)

        lbl_title = Label(self.bill_frame, text="Área de facturación del cliente", font=("goudy old style", 20), bg="#13278f", fg="white", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(self.bill_frame, orient=VERTICAL)
        self.bill_area = Text(self.bill_frame, font=("goudy old style", self.widget_sizes["list_font"]), bg="white", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=True)

        # Mostrar las boletas al inicio
        self.show()

        # Añadimos el botón de eliminar debajo del área de las boletas
        self.btn_delete = Button(self.container, text="Eliminar", command=self.delete_invoice, font=("goudy old style", self.widget_sizes["button_font"], "bold"), bg="red", fg="white", cursor="hand2")
        self.btn_delete.place(relx=0.02, rely=0.85, relwidth=0.25, relheight=0.05)

    def on_resize(self, event):
        # Calcula tamaños proporcionales
        width = event.width
        height = event.height

        self.widget_sizes["title_font"] = int(width / 50)
        self.widget_sizes["label_font"] = int(width / 70)
        self.widget_sizes["button_font"] = int(width / 100)
        self.widget_sizes["list_font"] = int(width / 90)

        # Actualiza fuentes dinámicamente
        self.title.config(font=("goudy old style", self.widget_sizes["title_font"], "bold"))
        self.lbl_invoice.config(font=("goudy old style", self.widget_sizes["label_font"]))
        self.txt_invoice.config(font=("goudy old style", self.widget_sizes["label_font"]))
        self.btn_search.config(font=("goudy old style", self.widget_sizes["button_font"], "bold"))
        self.sales_list.config(font=("goudy old style", int(width / 90)))
        self.bill_area.config(font=("goudy old style", self.widget_sizes["list_font"]))    

    # Métodos de funcionalidad de SalesClass
    def show(self):
        self.bill_list.clear()
        self.sales_list.delete(0, END)
        for i in os.listdir('bill'):
            if i.endswith('.txt'):
                self.sales_list.insert(END, i)
                self.bill_list.append(i.split(".")[0])

    def get_data(self, ev):
        index_ = self.sales_list.curselection()
        file_name = self.sales_list.get(index_)
        self.bill_area.delete('1.0', END)
        with open(f'bill/{file_name}', 'r') as fp:
            for line in fp:
                self.bill_area.insert(END, line)

    def delete_invoice(self):
        selected_invoice = self.sales_list.curselection()
        
        if not selected_invoice:
            messagebox.showerror("Error", "Por favor seleccione una boleta para eliminar", parent=self.container)
            return
        
        file_name = self.sales_list.get(selected_invoice)
        file_path = f'bill/{file_name}'
        
        confirm = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de eliminar la boleta {file_name}?", parent=self.container)
        
        if confirm:
            try:
                os.remove(file_path)  # Eliminar el archivo
                messagebox.showinfo("Éxito", f"Boleta {file_name} eliminada correctamente", parent=self.container)
                self.show()  # Actualizar la lista
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la boleta: {e}", parent=self.container)

    def search(self):
        if not self.var_invoice.get():
            messagebox.showerror("Error", "Se necesita el número de factura", parent=self.container)
        elif self.var_invoice.get() in self.bill_list:
            self.bill_area.delete('1.0', END)
            with open(f'bill/{self.var_invoice.get()}.txt', 'r') as fp:
                for line in fp:
                    self.bill_area.insert(END, line)
        else:
            messagebox.showerror("Error", "Numero de factura invalido", parent=self.container)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0', END)

# Ejemplo de inicialización en una ventana Tk para ver el resultado
if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True)
    obj = SalesClass(frame)
    root.mainloop()
