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
from ui.rooms import RoomsPage
from ui.groups import GroupsPage
from ui.schedule import SchedulePage
from ui.payments import PaymentsPage
from ui.presence import PresencePage
from ui.parametres import ParametresPage
from database.db_compatibility import DatabaseCompatibility
from config.theme import ModernTheme
from config.settings import AppSettings, ThemeSettings
import os


class ModernApp(ctk.CTk):
    """
    Application principale modernisée
    - Design professionnel
    - Navigation fluide
    - Thème cohérent
    - Authentification requise
    """
    
    def __init__(self, require_login=True):
        super().__init__()
        
        # Configuration de la fenêtre
        self.title(AppSettings.APP_NAME)
        self.geometry(f"{AppSettings.WINDOW_WIDTH}x{AppSettings.WINDOW_HEIGHT}")
        self.minsize(AppSettings.WINDOW_MIN_WIDTH, AppSettings.WINDOW_MIN_HEIGHT)
        
        # Configuration du thème
        ctk.set_appearance_mode(AppSettings.DEFAULT_THEME_MODE)
        ctk.set_default_color_theme(AppSettings.DEFAULT_COLOR_THEME)
        
        # Initialisation de la base de données
        self.db = DatabaseCompatibility()
        
        # Configuration du layout principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Configuration du fond de l'application
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        self.is_authenticated = False
        
        # Afficher le login si requis
        if require_login:
            self.withdraw()  # Cacher la fenêtre principale
            # Afficher le login après que la fenêtre soit créée
            self.after(100, self._show_login)
        else:
            self.is_authenticated = True
            self._create_ui()
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
    
    def _show_login(self):
        """Affiche l'écran de connexion"""
        from ui.login import show_login
        show_login(self, self._on_login_success)
    
    def _on_login_success(self):
        """Callback appelé après connexion réussie"""
        self.is_authenticated = True
        self.deiconify()  # Afficher la fenêtre principale
        self._create_ui()
        self._center_window()
    
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
            "rooms": self.show_rooms,
            "groups": self.show_groups,
            "schedule": self.show_schedule,
            "payments": self.show_payments,
            "presence": self.show_presence,
            "parametres": self.show_parametres,
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
    
    def show_rooms(self):
        """Affiche la page de gestion des salles"""
        self.current_frame = RoomsPage(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
    
    def show_groups(self):
        """Affiche la page de gestion des groupes"""
        self.current_frame = GroupsPage(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
    
    def show_schedule(self):
        """Affiche la page de l'emploi du temps"""
        self.current_frame = SchedulePage(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
    
    def show_payments(self):
        """Affiche la page de paiements"""
        self.current_frame = PaymentsPage(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
    
    def show_presence(self):
        """Affiche la page de présence"""
        self.current_frame = PresencePage(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
    
    def show_parametres(self):
        """Affiche la page de paramètres"""
        self.current_frame = ParametresPage(self.content_container, self.db)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)


def main(require_login=True):
    """
    Point d'entrée de l'application
    
    Args:
        require_login: Si True, affiche l'écran de connexion
    """
    app = ModernApp(require_login=require_login)
    app.mainloop()


if __name__ == "__main__":
    main()
