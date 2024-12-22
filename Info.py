from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataVisualizationClass:
    def __init__(self, container):
        self.container = container

        # Título
        self.title = Label(self.container, text="Visualización de Datos de Ventas y Stock", font=("goudy old style", 25, "bold"),
                           bg="#13278f", fg="white", bd=3)
        self.title.pack(side=TOP, fill=X)

        # Botones para mostrar gráficos
        self.btn_stock = Button(self.container, text="Mostrar Stock de Productos", command=self.show_stock,
                                font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_stock.place(relx=0.1, rely=0.1, relwidth=0.4, height=40)

        self.btn_sales_by_service = Button(self.container, text="Mostrar Ventas por Servicio", command=self.show_sales_by_service,
                                            font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_sales_by_service.place(relx=0.55, rely=0.1, relwidth=0.4, height=40)

        self.btn_sales_by_product = Button(self.container, text="Mostrar Ventas por Producto", command=self.show_sales_by_product,
                                            font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_sales_by_product.place(relx=0.1, rely=0.15, relwidth=0.4, height=40)

        self.btn_total_sales = Button(self.container, text="Mostrar Ventas Totales", command=self.show_total_sales,
                                       font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_total_sales.place(relx=0.55, rely=0.15, relwidth=0.4, height=40)

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

    def fetch_sales_by_service(self):
        """Consulta las ventas por servicio."""
        con = sqlite3.connect('tbs.db')
        cur = con.cursor()
        cur.execute("""
            SELECT s.name, SUM(o.total_price) 
            FROM orders o
            JOIN order_services os ON o.id = os.order_id
            JOIN services s ON os.service_id = s.id
            GROUP BY s.name
        """)
        data = cur.fetchall()
        con.close()
        return data

    def fetch_sales_by_product(self):
        """Consulta las ventas por producto."""
        con = sqlite3.connect('tbs.db')
        cur = con.cursor()
        cur.execute("""
            SELECT st.itemname, SUM(o.total_price) 
            FROM orders o
            JOIN order_products op ON o.id = op.order_id
            JOIN stock st ON op.product_id = st.pid
            GROUP BY st.itemname
        """)
        data = cur.fetchall()
        con.close()
        return data

    def fetch_total_sales(self):
        """Consulta las ventas totales."""
        con = sqlite3.connect('tbs.db')
        cur = con.cursor()
        cur.execute("SELECT SUM(total_price) FROM orders")
        total = cur.fetchone()[0] or 0
        con.close()
        return total

    def show_sales_by_service(self):
        """Genera y muestra el gráfico de ventas por servicio."""
        data = self.fetch_sales_by_service()
        if not data:
            messagebox.showerror("Error", "No hay datos de ventas para mostrar el gráfico.")
            return

        servicios = [row[0] for row in data]
        ventas = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(servicios, ventas, color='skyblue')
        ax.set_xlabel('Servicio')
        ax.set_ylabel('Total Ventas')
        ax.set_title('Ventas por Servicio')

        self.clear_canvas()
        self.display_chart(fig)

    def show_sales_by_product(self):
        """Genera y muestra el gráfico de ventas por producto."""
        data = self.fetch_sales_by_product()
        if not data:
            messagebox.showerror("Error", "No hay datos de ventas para mostrar el gráfico.")
            return

        productos = [row[0] for row in data]
        ventas = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(productos, ventas, color='lightgreen')
        ax.set_xlabel('Producto')
        ax.set_ylabel('Total Ventas')
        ax.set_title('Ventas por Producto')

        self.clear_canvas()
        self.display_chart(fig)

    def show_total_sales(self):
        """Genera y muestra el total de ventas."""
        total = self.fetch_total_sales()
        messagebox.showinfo("Total de Ventas", f"El total de ventas es: {total:.2f}")

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
