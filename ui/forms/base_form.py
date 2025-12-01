"""
Classe de base pour tous les formulaires
Fournit fonctionnalités communes (validation, centrage, modal, etc.)
"""

import customtkinter as ctk
from tkinter import messagebox
from config.theme import ModernTheme
from utils import center_window
from utils.messages import Messages


class BaseForm(ctk.CTkToplevel):
    """Formulaire de base avec fonctionnalités communes"""
    
    def __init__(self, parent, title: str, width: int = 550, height: int = 700, **kwargs):
        super().__init__(parent)
        
        self.callback = kwargs.get('callback', None)
        self.data = kwargs.get('data', None)
        
        # Configuration de la fenêtre
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        
        # Rendre modal
        self.transient(parent)
        self.grab_set()
        
        # Configuration du fond
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        # Container principal
        self.main_container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Centrer la fenêtre
        center_window(self)
    
    def create_field(self, parent, label_text: str, row: int):
        """Créer un label pour un champ"""
        from widgets.modern_components import ModernLabel
        label = ModernLabel(parent, text=label_text, style='normal')
        label.grid(row=row, column=0, padx=(0, 15), pady=10, sticky="w")
    
    def validate_required(self, fields: dict) -> bool:
        """
        Valider les champs obligatoires
        
        Args:
            fields: Dict {nom_champ: valeur}
        
        Returns:
            True si tout OK, False sinon
        """
        for field_name, value in fields.items():
            if not value or not value.strip():
                messagebox.showerror(
                    Messages.ERROR_TITLE,
                    Messages.ERROR_MISSING_FIELD.format(field=field_name)
                )
                return False
        return True
    
    def show_success(self, message: str):
        """Afficher un message de succès"""
        messagebox.showinfo(Messages.SUCCESS_TITLE, message)
    
    def show_error(self, message: str):
        """Afficher un message d'erreur"""
        messagebox.showerror(Messages.ERROR_TITLE, message)
    
    def close_and_callback(self):
        """Fermer et appeler le callback"""
        self.destroy()
        if self.callback:
            self.callback()
