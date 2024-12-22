from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os


class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        blank_space = " "
        self.root.state('zoomed')
        self.root.title(
            150 * blank_space
            + "Plamparambil Power Tools Billing and Management System |  Developed by Shibino"
        )
        self.root.config(bg="#fafafa")

        # Images


        # Login frame
        self.email = StringVar()
        self.password = StringVar()

        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(relx=0.55, rely=0.13, relwidth=0.26, relheight=0.65)

        title = Label(
            login_frame,
            text="Ingreso",
            font=("Elephant", 30, "bold"),
            bg="white",
        ).place(relx=0, rely=0.1, relwidth=1)

        lbl_clientid = Label(
            login_frame,
            text="Nombre",
            font=("Andalus", 15),
            bg="white",
            fg="#13278f",
        ).place(relx=0.14, rely=0.25)

        txt_email = Entry(
            login_frame,
            textvariable=self.email,
            font=("times new roman", 15),
            bg="#ECECEC",
        ).place(relx=0.14, rely=0.32, relwidth=0.7)

        lbl_pass = Label(
            login_frame,
            text="Contraseña",
            font=("Andalus", 15),
            bg="white",
            fg="#13278f",
        ).place(relx=0.14, rely=0.45)

        txt_pass = Entry(
            login_frame,
            textvariable=self.password,
            show="*",
            font=("times new roman", 15),
            bg="#ECECEC",
        ).place(relx=0.14, rely=0.52, relwidth=0.7)

        btn_login = Button(
            login_frame,
            command=self.login,
            text="Ingresar",
            font=("Arial Rounded MT Bold", 15),
            bg="#13278f",
            activebackground="#13278f",
            fg="white",
            cursor="hand2",
        ).place(relx=0.14, rely=0.7, relwidth=0.7, relheight=0.1)

        # Animation images
        self.im1 = ImageTk.PhotoImage(file="images/phonela.jpg")
        self.im2 = ImageTk.PhotoImage(file="images/123.png")

        self.lbl_change_image = Label(self.root, bg="white")
        self.lbl_change_image.place(relx=0.25, rely=0.13, relwidth=0.2, relheight=0.6)

        self.animate()

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im

        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000, self.animate)

    def login(self):
        con = sqlite3.connect(database="tbs.db")
        cur = con.cursor()
        try:
            if self.email.get() == "" or self.password.get() == "":
                messagebox.showerror("Error", "Rellena todo los campos", parent=self.root)
            else:
                cur.execute(
                    "select utype from client where email=? AND pass=?",
                    (self.email.get(), self.password.get()),
                )
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror(
                        "Error", "Usuario/Contraseña incorrectas", parent=self.root
                    )
                else:
                    if user[0] == "Administrador":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error debido a : {str(ex)} ", parent=self.root
            )


root = Tk()
obj = Login_System(root)
root.mainloop()
