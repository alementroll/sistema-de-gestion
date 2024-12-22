from tkinter import *
from tkinter import messagebox
import sqlite3
import shutil
import os

class SettingClass(Frame):
    def __init__(self, container):
        super().__init__(container, bg="#bde3ff")  # Cambia el color de fondo aquí
        self.container = container

        # Título
        self.title = Label(self.container, text="Ajustes", 
                           font=("goudy old style", 25, "bold"), bg="#13278f", fg="white", bd=3)
        self.title.pack(side=TOP, fill=X)

        # Botón para realizar respaldo manual
        self.btn_backup = Button(self.container, text="Hacer Respaldo Manual", command=self.create_backup,
                                 font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_backup.place(relx=0.35, rely=0.4, relwidth=0.3, height=50)

    def create_backup(self):
        """Crea un respaldo de la base de datos SQLite."""
        try:
            # Ruta del archivo original de la base de datos
            db_file = "tbs.db"

            # Verificar si el archivo existe
            if not os.path.exists(db_file):
                messagebox.showerror("Error", "La base de datos no existe.")
                return

            # Directorio de respaldo
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)  # Crear el directorio si no existe

            # Nombre del archivo de respaldo con timestamp
            backup_file = os.path.join(backup_dir, "tbs_backup.db")

            # Copiar el archivo
            shutil.copy2(db_file, backup_file)

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Respaldo creado en: {backup_file}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el respaldo: {e}")

# Crear la aplicación
if __name__ == "__main__":
    root = Tk()
    root.title("Panel de Configuración")

    # Configurar el tamaño y diseño de la ventana principal
    root.geometry("800x600")
    root.configure(bg="#bde3ff")  # Color de fondo de la ventana principal

    # Crear la instancia de SettingClass
    app = SettingClass(root)
    app.pack(fill=BOTH, expand=True)

    root.mainloop()