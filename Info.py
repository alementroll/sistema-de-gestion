from tkinter import *
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataVisualizationClass:
    def __init__(self, container):
        self.container = container

        # Título
        self.title = Label(self.container, text="Visualización de Datos de Stock", font=("goudy old style", 25, "bold"),
                           bg="#13278f", fg="white", bd=3)
        self.title.pack(side=TOP, fill=X)

        # Botón para mostrar gráficos de stock
        self.btn_stock = Button(self.container, text="Mostrar Stock de Productos", command=self.show_stock,
                                font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_stock.place(relx=0.2, rely=0.1, relwidth=0.3, height=40)

        # Botón para mostrar cantidad de pedidos
        self.btn_orders = Button(self.container, text="Mostrar Cantidad de Pedidos", command=self.show_order_count,
                                font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_orders.place(relx=0.55, rely=0.1, relwidth=0.3, height=40)

        # Canvas donde se dibujará el gráfico
        self.canvas_frame = Frame(self.container)
        self.canvas_frame.place(relx=0.01, rely=0.2, relwidth=0.98, relheight=0.75)

    def fetch_stock_data(self):
        """Consulta el stock de productos."""
        con = sqlite3.connect('tbs.db')
        cur = con.cursor()
        cur.execute("""
            SELECT itemname, qty 
            FROM stock
        """)
        data = cur.fetchall()
        con.close()
        return data

    def fetch_order_count(self):
        """Consulta la cantidad total de pedidos."""
        con = sqlite3.connect('tbs.db')
        cur = con.cursor()
        cur.execute("""
            SELECT COUNT(*) FROM orders
        """)
        count = cur.fetchone()[0]
        con.close()
        return count

    def show_stock(self):
        """Genera y muestra el gráfico de stock de productos."""
        data = self.fetch_stock_data()
        if not data:
            messagebox.showerror("Error", "No hay datos de stock para mostrar el gráfico.")
            return

        productos = [row[0] for row in data]
        cantidades = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(productos, cantidades, color='lightblue')
        ax.set_xlabel('Producto')
        ax.set_ylabel('Cantidad en Stock')
        ax.set_title('Stock de Productos')

        self.clear_canvas()
        self.display_chart(fig)

    def show_order_count(self):
        """Muestra la cantidad total de pedidos en un gráfico."""
        count = self.fetch_order_count()
        
        # Crear un gráfico con el conteo de pedidos
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(['Total de Pedidos'], [count], color='orange')
        ax.set_ylabel('Cantidad de Pedidos')
        ax.set_title('Cantidad Total de Pedidos')

        # Configurar el eje y para mostrar solo números enteros
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

        self.clear_canvas()
        self.display_chart(fig)

    def clear_canvas(self):
        """Elimina el gráfico anterior si existe."""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

    def display_chart(self, fig):
        """Integra el gráfico con Tkinter."""
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

# Crear la aplicación
if __name__ == "__main__":
    root = Tk()
    app = DataVisualizationClass(root)
    root.geometry("1920x1080")
    root.mainloop()
