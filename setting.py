from tkinter import *
from tkinter import ttk

class SettingClass(Frame):
    def __init__(self, container):
        super().__init__(container)  # Inicializa el Frame
        self.container = container
        
        # Colores
        self.light_mode_bg = "#bde3ff"
        self.dark_mode_bg = "#2e2e2e"
        self.light_mode_fg = "black"
        self.dark_mode_fg = "white"

        # Variables
        self.is_dark_mode = False

        # Usar Grid para manejar la disposición de los widgets
        self.grid(row=0, column=0, sticky="nsew")
        
        # Establecer las configuraciones iniciales del layout
        self.container.grid_rowconfigure(0, weight=1)  # Fila que contendrá el Frame
        self.container.grid_columnconfigure(0, weight=1)  # Columna que contendrá el Frame

        # Botón para cambiar el modo
        self.toggle_button = Button(self, text="Cambiar Modo", command=self.toggle_mode, font=("Arial", 12, "bold"))
        self.toggle_button.grid(row=0, column=0, pady=20, sticky="ew")

        # Etiqueta que cambia de color según el modo
        self.label = Label(self, text="Modo Claro/Oscuro", font=("Arial", 14), bg=self.light_mode_bg, fg=self.light_mode_fg)
        self.label.grid(row=1, column=0, pady=20, sticky="ew")

        # Configurar el modo inicial (Modo Claro)
        self.apply_light_mode()

    def toggle_mode(self):
        """Alterna entre el modo claro y el modo oscuro."""
        if self.is_dark_mode:
            self.apply_light_mode()
        else:
            self.apply_dark_mode()

        # Alternar el estado del modo
        self.is_dark_mode = not self.is_dark_mode

    def apply_light_mode(self):
        """Aplica el modo claro."""
        self.config(bg=self.light_mode_bg)
        self.label.config(bg=self.light_mode_bg, fg=self.light_mode_fg)
        self.toggle_button.config(bg=self.light_mode_bg, fg=self.light_mode_fg)

    def apply_dark_mode(self):
        """Aplica el modo oscuro."""
        self.config(bg=self.dark_mode_bg)
        self.label.config(bg=self.dark_mode_bg, fg=self.dark_mode_fg)
        self.toggle_button.config(bg=self.dark_mode_bg, fg=self.dark_mode_fg)


if __name__ == "__main__":
    root = Tk()
    app = SettingClass(root)  # Se pasa root como contenedor
    app.grid(row=0, column=0, sticky="nsew")  # Empaquetar el Frame dentro de la ventana principal
    
    root.geometry("300x150")  # Tamaño de la ventana inicial
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()
