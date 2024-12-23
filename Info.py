from tkinter import *
from tkinter import messagebox, simpledialog  # Asegúrate de incluir simpledialog
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import threading
import time
from datetime import datetime

class DataVisualizationClass:
    def __init__(self, container):
        self.container = container
        self.container.config(bg="#bde3ff")

        # Título
        self.title = Label(self.container, text="Visualización de Datos de Stock", font=("goudy old style", 25, "bold"),
                           bg="#13278f", fg="white", bd=3)
        self.title.pack(side=TOP, fill=X)

        # Botón para crear recordatorio
        self.btn_reminder = Button(self.container, text="Crear Recordatorio", command=self.create_reminder,
                                    font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_reminder.place(relx=0.35, rely=0.1, relwidth=0.3, height=40)

        # Botón para mostrar gráficos de stock
        self.btn_stock = Button(self.container, text="Mostrar Stock de Productos", command=self.show_stock,
                                font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_stock.place(relx=0.2, rely=0.2, relwidth=0.3, height=40)

        # Botón para mostrar cantidad de pedidos
        self.btn_orders = Button(self.container, text="Mostrar Cantidad de Pedidos", command=self.show_order_count,
                                font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_orders.place(relx=0.55, rely=0.2, relwidth=0.3, height=40)

        # Botón para generar PDF
        self.btn_generate_pdf = Button(self.container, text="Generar PDF Resumen", command=self.generate_pdf,
                                        font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_generate_pdf.place(relx=0.35, rely=0.3, relwidth=0.3, height=40)

        # Botón para abrir PDF
        self.btn_open_pdf = Button(self.container, text="Abrir PDF Resumen", command=self.open_pdf,
                                    font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_open_pdf.place(relx=0.35, rely=0.4, relwidth=0.3, height=40)


        self.pdf_filename = "resumen_datos.pdf"  # Nombre del archivo PDF

        # Variable para almacenar el recordatorio
        self.reminder_message = None
        self.reminder_time = None

        # Iniciar un hilo para verificar recordatorios
        reminder_thread = threading.Thread(target=self.check_reminders)
        reminder_thread.daemon = True
        reminder_thread.start()

    def create_reminder(self):
        """Crear un recordatorio solicitando mensaje, fecha y hora."""
        self.reminder_message = simpledialog.askstring("Recordatorio", "Ingrese el mensaje del recordatorio:")
        reminder_time_str = simpledialog.askstring(
            "Recordatorio",
            "Ingrese la fecha y hora (formato: DD-MM-AAAA HH:MM AM/PM):"
        )
        
        try:
            self.reminder_time = datetime.strptime(reminder_time_str, "%d-%m-%Y %I:%M %p")
            messagebox.showinfo("Éxito", "Recordatorio creado para: " + str(self.reminder_time))
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha y hora incorrecto.")



    def check_reminders(self):
        """Verifica constantemente si hay recordatorios que deben activarse."""
        while True:
            time.sleep(60)  # Verifica cada minuto
            if self.reminder_time and datetime.now() >= self.reminder_time:
                messagebox.showinfo("Recordatorio", self.reminder_message)
                self.reminder_time = None  # Reinicia el recordatorio

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
        for order in order_data:
            c.drawString(100, y_position, f"Pedido ID: {order[0]}")  # Suponiendo que el ID es el primer elemento
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
        for order_id, product_name in order_products:
            c.drawString(100, y_position, f"Pedido ID: {order_id}, Producto: {product_name}")
            y_position -= 20

        c.save()
        messagebox.showinfo("Éxito", f"PDF guardado como {self.pdf_filename}")

    def open_pdf(self):
        """Abre el PDF generado."""
        os.startfile(self.pdf_filename)

    def show_stock(self):
        """Muestra los gráficos de stock de productos."""
        stock_data = self.fetch_stock_data()
        items = [row[0] for row in stock_data]
        quantities = [row[1] for row in stock_data]

        plt.figure(figsize=(10, 6))
        plt.bar(items, quantities, color='blue')
        plt.title("Stock de Productos")
        plt.xlabel("Productos")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def show_order_count(self):
        """Muestra la cantidad de pedidos en un gráfico."""
        order_data = self.fetch_order_data()
        order_count = len(order_data)

        plt.figure(figsize=(10, 6))
        plt.bar(["Pedidos"], [order_count], color='orange')
        plt.title("Cantidad de Pedidos")
        plt.xlabel("Tipo de Pedido")
        plt.ylabel("Cantidad")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    root = Tk()
    app = DataVisualizationClass(root)
    root.geometry("800x600")
    root.mainloop()
