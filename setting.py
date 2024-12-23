from tkinter import *
from tkinter import messagebox, simpledialog
import sqlite3
import shutil
import os
import threading
import time
from tkinter import filedialog

class SettingClass(Frame):
    title = None  

    def __init__(self, container):
        super().__init__(container, bg="#bde3ff") 
        self.container = container
        self.container.config(bg="#bde3ff")

   
        if SettingClass.title is None:
            SettingClass.title = Label(self.container, text="Ajustes", 
                                        font=("goudy old style", 25, "bold"), bg="#13278f", fg="white", bd=3)
            SettingClass.title.pack(side=TOP, fill=X)

        # Botón para realizar respaldo manual
        self.btn_backup = Button(self.container, text="Hacer Respaldo Manual", command=self.create_backup,
                                 font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_backup.place(relx=0.35, rely=0.25, relwidth=0.3, height=50)

        # Botón para restaurar respaldo
        self.btn_restore = Button(self.container, text="Restaurar Respaldo", command=self.restore_backup,
                                  font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_restore.place(relx=0.35, rely=0.35, relwidth=0.3, height=50)

        # Botón para cambiar contraseñas
        self.btn_change_password = Button(self.container, text="Cambiar Contraseña de Usuario", command=self.change_password,
                                           font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_change_password.place(relx=0.35, rely=0.45, relwidth=0.3, height=50)

        # Configuración de respaldo automático
        self.auto_backup_label = Label(self.container, text="Respaldo Automático (días):", 
                                       font=("goudy old style", 15, "bold"), bg="#bde3ff")
        self.auto_backup_label.place(relx=0.3, rely=0.6)

        self.auto_backup_entry = Entry(self.container, font=("goudy old style", 15), bd=3)
        self.auto_backup_entry.place(relx=0.5, rely=0.6, relwidth=0.2, height=30)

        self.btn_start_auto_backup = Button(self.container, text="Iniciar Respaldo Automático", command=self.start_auto_backup,
                                             font=("goudy old style", 15, "bold"), bg="#13278f", fg="white", bd=3, cursor="hand2")
        self.btn_start_auto_backup.place(relx=0.35, rely=0.7, relwidth=0.3, height=50)

        self.auto_backup_thread = None
        self.auto_backup_running = False

    def create_backup(self):
        """Crea un respaldo de la base de datos SQLite."""
        try:
            db_file = "tbs.db"
            if not os.path.exists(db_file):
                messagebox.showerror("Error", "La base de datos no existe.")
                return
            
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)

            backup_file = os.path.join(backup_dir, f"tbs_backup_{int(time.time())}.db")  

            shutil.copy2(db_file, backup_file)
            messagebox.showinfo("Éxito", f"Respaldo creado en: {backup_file}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el respaldo: {e}")

    def restore_backup(self):
        """Restaura un respaldo de la base de datos SQLite."""
        try:
            backup_file = filedialog.askopenfilename(title="Selecciona un respaldo", 
                                                      filetypes=[("Database files", "*.db")],
                                                      initialdir="backups")  

            if not backup_file:  
                return

  
            shutil.copy2(backup_file, "tbs.db")
            messagebox.showinfo("Éxito", "Respaldo restaurado exitosamente.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo restaurar el respaldo: {e}")

    def start_auto_backup(self):
        """Inicia el respaldo automático según el intervalo ingresado."""
        if self.auto_backup_running:
            messagebox.showinfo("Información", "El respaldo automático ya está en funcionamiento.")
            return
        
        try:
            interval = int(self.auto_backup_entry.get()) * 86400  
            if interval <= 0:
                messagebox.showerror("Error", "Por favor ingresa un intervalo válido (mayor a 0).")
                return
            
            self.auto_backup_running = True
            self.auto_backup_thread = threading.Thread(target=self.auto_backup, args=(interval,))
            self.auto_backup_thread.start()
            messagebox.showinfo("Éxito", f"Respaldo automático iniciado cada {int(interval/86400)} días.")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido.")

    def auto_backup(self, interval):
        """Realiza el respaldo automático."""
        while self.auto_backup_running:
            time.sleep(interval)  
            self.create_backup()  

    def stop_auto_backup(self):
        """Detiene el respaldo automático."""
        self.auto_backup_running = False
        if self.auto_backup_thread is not None:
            self.auto_backup_thread.join()  
        messagebox.showinfo("Información", "El respaldo automático ha sido detenido.")

    def change_password(self):
        """Permite cambiar la contraseña de un usuario."""
     
        if not self.is_admin():
            messagebox.showerror("Error", "No tienes permisos para cambiar contraseñas.")
            return
        

        user_id = simpledialog.askinteger("Cambiar Contraseña", "Ingresa el ID del usuario:")
        if user_id is None:
            return  

        new_password = simpledialog.askstring("Cambiar Contraseña", "Ingresa la nueva contraseña:", show='*')
        if new_password is None:
            return  
        
  
        self.update_password(user_id, new_password)

    def is_admin(self):
        """Verifica si el usuario actual es administrador."""
        current_user_type = "Administrador"  
        return current_user_type == "Administrador"

    def update_password(self, user_id, new_password):
        """Actualiza la contraseña del usuario en la base de datos."""
        try:
            con = sqlite3.connect("tbs.db")
            cur = con.cursor()
            cur.execute("UPDATE client SET pass = ? WHERE eid = ?", (new_password, user_id))
            con.commit()

            if cur.rowcount == 0:
                messagebox.showerror("Error", "Usuario no encontrado.")
            else:
                messagebox.showinfo("Éxito", "Contraseña actualizada exitosamente.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la contraseña: {e}")
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    root.title("Panel de Configuración")
    root.geometry("800x600")
    root.configure(bg="#bde3ff")


    app = SettingClass(root)
    app.pack(fill=BOTH, expand=True)

    root.mainloop()
