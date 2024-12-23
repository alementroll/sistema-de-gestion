from tkinter import *
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os  # Importar el módulo os para abrir el PDF

class DataVisualizationClass:
    def __init__(self, container):
        self.container = container
        self.container.config(bg="#cae6fa")

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

        # Botón para generar PDF
        self.btn_generate_pdf = Button(self.container, text="Generar PDF Resumen", command=self.generate_pdf,
                                        font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_generate_pdf.place(relx=0.35, rely=0.2, relwidth=0.3, height=40)

        # Botón para abrir PDF
        self.btn_open_pdf = Button(self.container, text="Abrir PDF Resumen", command=self.open_pdf,
                                    font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_open_pdf.place(relx=0.35, rely=0.3, relwidth=0.3, height=40)

        # Canvas donde se dibujará el gráfico
        self.canvas_frame = Frame(self.container)
        self.canvas_frame.place(relx=0.01, rely=0.4, relwidth=0.98, relheight=0.55)

        self.pdf_filename = "resumen_datos.pdf"  # Nombre del archivo PDF

    def fetch_client_data(self):
        """Consulta los datos de los clientes."""
        con = sqlite3.connect('tbs.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM client")
        data = cur.fetchall()
        con.close()
        return data

    def fetch_service_data(self):
        """Consulta los datos de los servicios."""
        con = sqlite3.connect('tbs.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM services")
        data = cur.fetchall()
        con.close()
        return data

    def fetch_stock_data(self):
        """Consulta el stock de productos."""
        con = sqlite3.connect('tbs.db')
        cur = con.cursor()
        cur.execute("SELECT itemname, qty FROM stock")
        data = cur.fetchall()
        con.close()
        return data

    def fetch_order_data(self):
        """Consulta los datos de los pedidos."""
        con = sqlite3.connect('tbs.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM orders")
        data = cur.fetchall()
        con.close()
        return data

    def fetch_order_services(self):
        """Consulta los servicios por pedido."""
        con = sqlite3.connect('tbs.db')
        cur = con.cursor()
        cur.execute("""
            SELECT orders.id, services.name 
            FROM order_services 
            JOIN orders ON order_services.order_id = orders.id
            JOIN services ON order_services.service_id = services.id
        """)
        data = cur.fetchall()
        con.close()
        return data

    def fetch_order_products(self):
        """Consulta los productos por pedido."""
        con = sqlite3.connect('tbs.db')
        cur = con.cursor()
        cur.execute("""
            SELECT orders.id, stock.itemname 
            FROM order_products 
            JOIN orders ON order_products.order_id = orders.id
            JOIN stock ON order_products.product_id = stock.pid
        """)
        data = cur.fetchall()
        con.close()
        return data

    def generate_pdf(self):
        """Genera un PDF con un resumen de la información de la base de datos."""
        client_data = self.fetch_client_data()
        service_data = self.fetch_service_data()
        stock_data = self.fetch_stock_data()
        order_data = self.fetch_order_data()
        order_services = self.fetch_order_services()
        order_products = self.fetch_order_products()

        c = canvas.Canvas(self.pdf_filename, pagesize=letter)
        width, height = letter

        # Título en el PDF
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 50, "Resumen de Datos")

        # Datos de clientes
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 80, "Clientes:")
        y_position = height - 100
        for eid, name, email, contact, _, _ in client_data:
            c.drawString(100, y_position, f"ID: {eid}, Nombre: {name}, Email: {email}, Contacto: {contact}")
            y_position -= 20

        # Datos de servicios
        c.drawString(100, y_position, "Servicios:")
        y_position -= 20
        for service_id, name, price, estimated_time in service_data:
            c.drawString(100, y_position, f"ID: {service_id}, Nombre: {name}, Precio: {price}, Tiempo Estimado: {estimated_time}")
            y_position -= 20

        # Datos de stock
        c.drawString(100, y_position, "Stock de Productos:")
        y_position -= 20
        for itemname, qty in stock_data:
            c.drawString(100, y_position, f"Producto: {itemname}, Cantidad: {qty}")
            y_position -= 20

        # Datos de pedidos
        c.drawString(100, y_position, "Pedidos:")
        y_position -= 20
        for order_id, client_id, device, status, details, order_date, total_price in order_data:
            c.drawString(100, y_position, f"ID: {order_id}, Cliente ID: {client_id}, Dispositivo: {device}, Estado: {status}, Fecha: {order_date}, Total: {total_price}")
            y_position -= 20

        # Servicios por pedido
        c.drawString(100, y_position, "Servicios por Pedido:")
        y_position -= 20
        for order_id, service_name in order_services:
            c.drawString(100, y_position, f"Pedido ID: {order_id}, Servicio: {service_name}")
            y_position -= 20

        # Productos por pedido
        c.drawString(100, y_position, "Productos por Pedido:")
        y_position -= 20
        for order_id, itemname in order_products:
            c.drawString(100, y_position, f"Pedido ID: {order_id}, Producto: {itemname}")
            y_position -= 20

        c.save()
        messagebox.showinfo("Éxito", f"PDF generado: {self.pdf_filename}")

    def open_pdf(self):
        """Abre el PDF generado con el visor predeterminado del sistema."""
        if os.path.exists(self.pdf_filename):
            os.startfile(self.pdf_filename)  # Para Windows
        else:
            messagebox.showerror("Error", "No se ha generado el PDF aún.")

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
        ax.set_title('Conteo Total de Pedidos')

        self.clear_canvas()
        self.display_chart(fig)

    def clear_canvas(self):
        """Limpia el canvas para mostrar nuevos gráficos."""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

    def display_chart(self, fig):
        """Muestra el gráfico en el canvas."""
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

if __name__ == "__main__":
    root = Tk()
    app = DataVisualizationClass(root)
    root.geometry("800x600")
    root.title("Gestión de Datos")
    root.mainloop()
