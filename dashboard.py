from tkinter import *
from PIL import Image, ImageTk
from clients import ClientClass
from services import ServiceClass
from stock import stockClass
from sales import SalesClass
from billing import billClass
from orders import OrderClass
from orders_list import OrderListClass
from Info import DataVisualizationClass
from setting import SettingClass
import sqlite3
from tkinter import messagebox
import os
import time

class TBS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1600x900")  # Resolución inicial
        self.fullscreen = True
        self.root.bind("<Configure>", self.on_resize)

        self.screen_width = self.root.winfo_width()
        self.screen_height = self.root.winfo_height()

        # Variables iniciales
        self.widget_sizes = {
            "title_font": 40,
            "menu_font": 30,
            "button_font": 15,
            "clock_font": 14,
            "footer_font": 12
        }

        # Header
        self.icon_title = PhotoImage(file="images/tool.png")
        self.title = Label(self.root, text="Panel de Control", image=self.icon_title, compound=LEFT,
                           font=("ARIEL", self.widget_sizes["title_font"], "bold"),
                           bg="#13278f", fg="#bde3ff", anchor="w", padx=20)
        self.title.place(relx=0, rely=0, relwidth=1, relheight=0.15)

        # Botón de cierre de sesión
        self.btn_logout = Button(self.root, text="Cerrar Sesión", command=self.logout,
                                font=("ARIEL", self.widget_sizes["button_font"], "bold"), bg="#bde3ff", cursor="hand2")
        self.btn_logout.place(relx=0.85, rely=0.035, relwidth=0.12, relheight=0.08)
        self.btn_logout.config(font=("ARIEL", self.widget_sizes["button_font"], "bold"))

        self.btn_fullscreen = Button(self.root, text="Pantalla Completa", command=self.toggle_fullscreen,
                                     font=("ARIEL", self.widget_sizes["button_font"], "bold"), bg="#bde3ff", cursor="hand2")
        self.btn_fullscreen.place(relx=0.65, rely=0.035, relwidth=0.16, relheight=0.08)
        self.btn_fullscreen.config(font=("ARIEL", self.widget_sizes["button_font"], "bold"))

        # Reloj
        self.lbl_clock = Label(self.root, text="Bienvenido a Plamparambil Power Tools...!!\t\t Fecha: DD-MM-YYYY\t\t Hora: HH:MM:SS",
                               font=("ARIEL", self.widget_sizes["clock_font"]), bg="#bde3ff", fg="black", borderwidth=3, relief="solid")
        self.lbl_clock.place(relx=0, rely=0.15, relwidth=1, relheight=0.05)

        # Menú izquierdo
        self.LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="#bde3ff")
        self.LeftMenu.place(relx=0, rely=0.2, relwidth=0.2, relheight=0.75)

        self.icon_side = PhotoImage(file="images/side.png")
        self.lbl_menu = Label(self.LeftMenu, text="MENU", font=("ARIEL", self.widget_sizes["menu_font"], "bold"), bg="#13278f", fg="#bde3ff")
        self.lbl_menu.pack(side=TOP, fill=X)

        # Footer
        self.footer = Label(self.root, text="Desarrollado por Calico´s | Sistema de gestión 2024©",
                            font=("ARIEL", self.widget_sizes["footer_font"]), bg="#13278f", fg="white", anchor="center")
        self.footer.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)

        # Botones de menú
        menu_buttons = [
            ("Pedidos", self.show_orders),
            ("Servicios", self.show_services),
            ("Productos", self.show_stock),
            ("Ventas", self.show_sales),
            ("Boleta", self.show_billing),
            ("Clientes", self.show_client),
            ("Datos", self.show_info),
            ("Ajustes", self.show_setting)
        ]

        self.menu_btns = []
        for text, command in menu_buttons:
            btn = Button(self.LeftMenu, text=text, command=command, image=self.icon_side, compound=LEFT, padx=20, anchor="center",
                        font=("ARIEL", self.widget_sizes["button_font"], "bold"), bg="white", bd=3, cursor="hand2")
            btn.pack(pady=10, fill=X, padx=10)
            self.menu_btns.append(btn)

        # Contenedor principal para las pantallas
        self.container = Frame(self.root, bg="white")
        self.container.place(relx=0.2, rely=0.2, relwidth=0.8, relheight=0.75)

        self.root.bind("<Configure>", self.on_resize)

        # Inicializa los frames y asegúrate de que todos usen el mismo contenedor
        self.clients_frame = Frame(self.container, bg="white")
        self.services_frame = Frame(self.container, bg="white")
        self.stock_frame = Frame(self.container, bg="white")
        self.sales_frame = Frame(self.container, bg="white")
        self.billing_frame = Frame(self.container, bg="white")
        self.orders_frame = Frame(self.container, bg="white")
        self.orders_list_frame = Frame(self.container, bg="white")
        self.info_frame = Frame(self.container, bg="white")
        self.settings_frame = Frame(self.container, bg="white")

        self.frames = {
            "clients": self.clients_frame,
            "services": self.services_frame,
            "stock": self.stock_frame,
            "sales": self.sales_frame,
            "billing": self.billing_frame,
            "orders": self.orders_frame,
            "orders_list": self.orders_list_frame,
            "info": self.info_frame,
            "settings": self.settings_frame
        }

        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Oculta inicialmente
            frame.lower()  # Envía al fondo

        # Mostrar una pantalla por defecto
        self.show_orders()

        self.update_content()

        # Verificar stock al iniciar
        self.check_stock()

        # Verificar el stock cada hora 
        self.root.after(3600000, self.check_stock)  #REVISA CADA HORA SI HAY ARTICULOS BAJOS, ACA SE PUEDE CAMBIAR

    def check_stock(self):
        """Consulta los niveles de stock y muestra un pop-up si algún artículo tiene menos de 5 unidades."""
        con = sqlite3.connect('tbs.db')  # Conectar a la base de datos
        cur = con.cursor()

        try:
            # Consultar los artículos con stock menor a 5
            cur.execute("SELECT itemname, qty FROM stock WHERE qty < 5")
            data = cur.fetchall()

            if data:
                # Si hay artículos con stock bajo, mostrar un pop-up con el mensaje
                low_stock_items = "\n".join([f"{item[0]}: {item[1]} unidades" for item in data])
                messagebox.showwarning("Stock Bajo", f"¡Atención! Estos artículos tienen menos de 5 unidades:\n{low_stock_items}")
            else:
                messagebox.showinfo("Stock Suficiente", "Todos los artículos tienen suficiente stock.")

        except Exception as ex:
            messagebox.showerror("Error", f"Error al comprobar el stock: {str(ex)}")
        finally:
            con.close()

    def show_frame(self, frame_name):
        """Muestra únicamente el frame seleccionado."""
        for name, frame in self.frames.items():
            if name == frame_name:
                frame.lift()  # Eleva el frame visible
            else:
                frame.lower()  # Oculta los demás

    # Métodos para mostrar cada pantalla
    def on_resize(self, event):  # Ajusta el tamaño del contenedor principal o elementos según el tamaño de la ventana
        """Evento que redimensiona los widgets."""
        new_width = event.width

        # Ajuste proporcional de fuentes
        self.widget_sizes["title_font"] = int(new_width / 30)
        self.widget_sizes["menu_font"] = int(new_width / 40)
        self.widget_sizes["button_font"] = int(new_width / 80)
        self.widget_sizes["clock_font"] = int(new_width / 100)
        self.widget_sizes["footer_font"] = int(new_width / 110)

        # Actualizar fuentes
        self.title.config(font=("ARIEL", self.widget_sizes["title_font"], "bold"))
        self.lbl_menu.config(font=("ARIEL", self.widget_sizes["menu_font"], "bold"))
        self.lbl_clock.config(font=("ARIEL", self.widget_sizes["clock_font"]))
        self.footer.config(font=("ARIEL", self.widget_sizes["footer_font"]))
        self.btn_logout.config(font=("ARIEL", self.widget_sizes["button_font"], "bold"))
        self.btn_fullscreen.config(font=("ARIEL", self.widget_sizes["button_font"], "bold"))

        for btn in self.menu_btns:
            btn.config(font=("ARIEL", self.widget_sizes["button_font"], "bold"))

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
    
    def logout(self):
        self.root.destroy()
        os.system("python login.py")
    
    def reload_clients(self):
        """Recarga la lista de clientes en las vistas correspondientes."""
        if hasattr(self, "client_obj"):
            self.client_obj.show()
        if hasattr(self, "orders_obj"):
            self.orders_obj.load_clients()
        if hasattr(self, "orders_list_obj"):
            self.orders_list_obj.show()

    def show_setting(self):
        self.show_frame("settings")
        if not hasattr(self, "settings"):
            self.settings_obj = SettingClass(self.settings_frame)

    def show_client(self):
        self.show_frame("clients")
        if not hasattr(self, "client_obj"):
            self.client_obj = ClientClass(self.clients_frame)

    def show_services(self):
        self.show_frame("services")
        if not hasattr(self, "services_obj"):
            self.services_obj = ServiceClass(self.services_frame)

    def show_info(self):
        self.show_frame("info")
        if not hasattr(self, "info_obj"):
            self.info_obj = DataVisualizationClass(self.info_frame)

    def show_stock(self):
        self.show_frame("stock")
        if not hasattr(self, "stock_obj"):
            self.stock_obj_obj = stockClass(self.stock_frame)

    def show_sales(self):
        self.show_frame("sales")
        if not hasattr(self, "sales_obj"):
            self.sales_obj = SalesClass(self.sales_frame)

    def show_billing(self):
        self.billing_frame.lift()
        if not hasattr(self, "billing_obj"):
            self.billing_obj = billClass(self.billing_frame)

    def show_orders(self):
        self.orders_frame.lift()
        if not hasattr(self, "orders_obj"):
            self.orders_obj = OrderClass(self.orders_frame, self.show_orders_list, self.reload_clients)
    
    def show_orders_list(self):
        self.show_frame("orders_list")
        if not hasattr(self, "orders_list_obj"):
            self.orders_list_obj = OrderListClass(self.orders_list_frame)

    def update_content(self):
        con = sqlite3.connect(database=r'tbs.db')
        cur = con.cursor()
        try:
            cur.execute("select * from stock")
            product = cur.fetchall()
            # Actualizar contenido de alguna etiqueta o botón si es necesario
            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Calico's - Gestión Inteligente\t\t Fecha: {str(date_)}\t\t Hora: {str(time_)}")
            self.lbl_clock.after(200, self.update_content)
        except Exception as ex:
            messagebox.showerror("Error", f"Error debido a: {str(ex)} ", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = TBS(root)
    root.mainloop()