import customtkinter as ctk
from widgets.sidebar import Sidebar
from ui.dashboard import Dashboard
from database.db_manager import DatabaseManager
import os

# Configuration de base
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestion Centre de Soutien")
        self.geometry("1100x700")

        # Database Initialization
        self.db = DatabaseManager()

        # Layout Grid Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = Sidebar(self, self.change_view)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Main Content Area
        self.current_frame = None
        self.show_dashboard()

    def change_view(self, view_name):
        # Clear current frame
        if self.current_frame:
            self.current_frame.destroy()

        if view_name == "dashboard":
            self.show_dashboard()
        elif view_name == "students":
            self.show_placeholder("Gestion des Élèves")
        elif view_name == "teachers":
            self.show_placeholder("Gestion des Enseignants")
        elif view_name == "subjects":
            self.show_placeholder("Gestion des Matières")
        elif view_name == "groups":
            self.show_placeholder("Gestion des Groupes")
        elif view_name == "payments":
            self.show_placeholder("Paiements & Comptabilité")
        elif view_name == "presence":
            self.show_placeholder("Feuille de Présence")

    def show_dashboard(self):
        self.current_frame = Dashboard(self, self.db)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_placeholder(self, title):
        self.current_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        label = ctk.CTkLabel(self.current_frame, text=f"Module: {title}", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=50)
        
        sub_label = ctk.CTkLabel(self.current_frame, text="Cette fonctionnalité est en cours de développement.")
        sub_label.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
