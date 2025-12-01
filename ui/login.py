"""
Interface de connexion (login)
Écran d'authentification avant d'accéder à l'application
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import ModernTheme
from config.settings import AppSettings
from database.db_compatibility import DatabaseCompatibility
from utils import center_window
from utils.messages import Messages


class LoginWindow(ctk.CTkToplevel):
    """Fenêtre de connexion"""
    
    def __init__(self, parent, on_success_callback):
        super().__init__(parent)
        
        self.on_success = on_success_callback
        self.db = DatabaseCompatibility()
        
        # Configuration de la fenêtre
        self.title("Connexion - " + AppSettings.APP_NAME)
        self.geometry("450x600")
        self.resizable(False, False)
        
        # Rendre modal
        self.transient(parent)
        self.grab_set()
        
        # Configuration du fond
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        self._create_ui()
        
        # Centrer la fenêtre
        center_window(self)
        
        # Focus sur le champ username
        self.username_entry.focus()
    
    def _create_ui(self):
        """Crée l'interface de connexion"""
        # Container principal avec scroll au cas où
        main_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        main_container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Logo/Icône
        logo_label = ctk.CTkLabel(
            main_container,
            text="🎓",
            font=ctk.CTkFont(size=60)
        )
        logo_label.pack(pady=(0, 15))
        
        # Titre
        title_label = ctk.CTkLabel(
            main_container,
            text="Connexion",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK)
        )
        title_label.pack(pady=(0, 8))
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(
            main_container,
            text=AppSettings.APP_NAME,
            font=ctk.CTkFont(size=12),
            text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
        )
        subtitle_label.pack(pady=(0, 25))
        
        # Carte de formulaire
        form_card = ctk.CTkFrame(
            main_container,
            corner_radius=ModernTheme.BORDER_RADIUS,
            fg_color=(ModernTheme.BG_CARD_LIGHT, ModernTheme.BG_CARD_DARK)
        )
        form_card.pack(fill="both", expand=True)
        
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Nom d'utilisateur
        username_label = ctk.CTkLabel(
            form_content,
            text="Nom d'utilisateur",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        username_label.pack(fill="x", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Entrez votre nom d'utilisateur",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.username_entry.pack(fill="x", pady=(0, 15))
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # Mot de passe
        password_label = ctk.CTkLabel(
            form_content,
            text="Mot de passe",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Entrez votre mot de passe",
            show="●",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.password_entry.pack(fill="x", pady=(0, 20))
        self.password_entry.bind("<Return>", lambda e: self._login())
        
        # Bouton de connexion
        login_btn = ctk.CTkButton(
            form_content,
            text="Se connecter",
            command=self._login,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=ModernTheme.PRIMARY,
            hover_color=ModernTheme.PRIMARY_DARK
        )
        login_btn.pack(fill="x")
        
        # Note
        note_label = ctk.CTkLabel(
            main_container,
            text="Utilisateur par défaut: admin / admin123",
            font=ctk.CTkFont(size=10),
            text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
        )
        note_label.pack(pady=(15, 0))
    
    def _login(self):
        """Tente la connexion"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror(
                Messages.ERROR_TITLE,
                "Veuillez entrer votre nom d'utilisateur et mot de passe"
            )
            return
        
        # Vérifier les identifiants
        if self._verify_credentials(username, password):
            messagebox.showinfo(
                Messages.SUCCESS_TITLE,
                f"Bienvenue, {username} !"
            )
            self.destroy()
            if self.on_success:
                self.on_success()
        else:
            messagebox.showerror(
                Messages.ERROR_TITLE,
                "Nom d'utilisateur ou mot de passe incorrect"
            )
            self.password_entry.delete(0, 'end')
            self.username_entry.focus()
    
    def _verify_credentials(self, username: str, password: str) -> bool:
        """
        Vérifie les identifiants de connexion
        
        Args:
            username: Nom d'utilisateur
            password: Mot de passe
        
        Returns:
            True si les identifiants sont corrects
        """
        try:
            import hashlib
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Hasher le mot de passe fourni
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            # Vérifier dans la base de données
            cursor.execute(
                "SELECT id, role FROM USERS WHERE username=? AND password=?",
                (username, hashed_password)
            )
            
            result = cursor.fetchone()
            conn.close()
            
            return result is not None
        except Exception as e:
            print(f"❌ Erreur lors de la vérification des identifiants: {e}")
            return False


def show_login(parent, on_success_callback):
    """
    Affiche la fenêtre de connexion
    
    Args:
        parent: Fenêtre parente
        on_success_callback: Fonction à appeler en cas de succès
    
    Note:
        La fenêtre est déjà modale (transient + grab_set),
        donc pas besoin de wait_window qui bloquerait le mainloop
    """
    login_window = LoginWindow(parent, on_success_callback)
