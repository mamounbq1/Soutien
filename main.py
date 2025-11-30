"""
Application principale modernisée
Point d'entrée de l'application avec design moderne et professionnel
"""

import customtkinter as ctk
from widgets.modern_sidebar import ModernSidebar
from ui.modern_dashboard import ModernDashboard
from ui.students import StudentsPage
from ui.teachers import TeachersPage
from ui.subjects import SubjectsPage
from ui.groups import GroupsPage
from ui.payments import PaymentsPage
from ui.presence import PresencePage
from database.db_manager import DatabaseManager
from config.theme import ModernTheme
import os


class ModernApp(ctk.CTk):
    """
    Application principale modernisée
    - Design professionnel
    - Navigation fluide
    - Thème cohérent
    """
    
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre
        self.title("Système de Gestion - Centre de Soutien Scolaire")
        self.geometry("1400x800")
        self.minsize(1200, 700)
        
        # Configuration du thème
        ctk.set_appearance_mode("light")  # "light" ou "dark"
        ctk.set_default_color_theme("blue")
        
        # Initialisation de la base de données
        self.db = DatabaseManager()
        
        # Configuration du layout principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Configuration du fond de l'application
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        # Créer l'interface
        self._create_ui()
        
        # Centrer la fenêtre
        self._center_window()
    
    def _create_ui(self):
        """Crée l'interface utilisateur"""
        # Sidebar moderne
        self.sidebar = ModernSidebar(self, self.change_view)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Container pour le contenu principal
        self.content_container = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)
        
        # Frame de contenu actuel
        self.current_frame = None
        
        # Afficher le dashboard par défaut
        self.show_dashboard()
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def change_view(self, view_name):
        """
        Change la vue affichée
        Args:
            view_name: Nom de la vue à afficher
        """
        # Détruire la vue précédente
        if self.current_frame:
            self.current_frame.destroy()
        
        # Afficher la nouvelle vue
        view_methods = {
            "dashboard": self.show_dashboard,
            "students": self.show_students,
            "teachers": self.show_teachers,
            "subjects": self.show_subjects,
            "groups": self.show_groups,
            "payments": self.show_payments,
            "presence": self.show_presence,
        }
        
        method = view_methods.get(view_name)
        if method:
            method()
    
    def show_dashboard(self):
        """Affiche le tableau de bord moderne"""
        self.current_frame = ModernDashboard(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
    
    def show_students(self):
        """Affiche la page de gestion des élèves"""
        self.current_frame = StudentsPage(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
    
    def show_teachers(self):
        """Affiche la page de gestion des enseignants"""
        self.current_frame = TeachersPage(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
    
    def show_subjects(self):
        """Affiche la page de gestion des matières"""
        self.current_frame = SubjectsPage(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
    
    def show_groups(self):
        """Affiche la page de gestion des groupes"""
        self.current_frame = GroupsPage(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
    
    def show_payments(self):
        """Affiche la page de paiements"""
        self.current_frame = PaymentsPage(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
    
    def show_presence(self):
        """Affiche la page de présence"""
        self.current_frame = PresencePage(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)


def main():
    """Point d'entrée de l'application"""
    app = ModernApp()
    app.mainloop()


if __name__ == "__main__":
    main()
