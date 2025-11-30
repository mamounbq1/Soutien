"""
Sidebar modernisée avec design professionnel
- Icônes pour chaque menu
- Effet de hover amélioré
- Sélection visuelle du menu actif
- Animation subtile
"""

import customtkinter as ctk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import ModernTheme


class ModernMenuButton(ctk.CTkButton):
    """Bouton de menu modernisé avec icône et indicateur de sélection"""
    
    def __init__(self, master, text, icon, command, **kwargs):
        self.icon = icon
        self.button_text = text
        self.is_selected = False
        
        super().__init__(
            master,
            text=f"{icon}  {text}",
            command=command,
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL, weight="normal"),
            height=ModernTheme.BUTTON_HEIGHT + 5,
            corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
            fg_color="transparent",
            text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
            hover_color=(ModernTheme.SIDEBAR_HOVER_LIGHT, ModernTheme.SIDEBAR_HOVER_DARK),
            anchor="w",
            **kwargs
        )
        
    def set_selected(self, selected: bool):
        """Change l'état de sélection du bouton"""
        self.is_selected = selected
        if selected:
            self.configure(
                fg_color=(ModernTheme.SIDEBAR_ACTIVE_LIGHT, ModernTheme.SIDEBAR_ACTIVE_DARK),
                text_color=(ModernTheme.PRIMARY, ModernTheme.PRIMARY_LIGHT),
                font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL, weight="bold")
            )
        else:
            self.configure(
                fg_color="transparent",
                text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
                font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL, weight="normal")
            )


class ModernSidebar(ctk.CTkFrame):
    """
    Sidebar modernisée avec design professionnel
    - Menu avec icônes
    - Sélection visuelle
    - Transitions fluides
    """
    
    def __init__(self, master, callback):
        super().__init__(
            master,
            width=ModernTheme.SIDEBAR_WIDTH,
            corner_radius=0,
            fg_color=(ModernTheme.SIDEBAR_BG_LIGHT, ModernTheme.SIDEBAR_BG_DARK)
        )
        
        self.callback = callback
        self.menu_buttons = {}
        self.current_view = "dashboard"
        
        # Configuration de la grille
        self.grid_rowconfigure(10, weight=1)  # Spacer pour pousser le logout en bas
        
        self._create_header()
        self._create_menu_items()
        self._create_footer()
        
    def _create_header(self):
        """Crée l'en-tête de la sidebar avec logo et titre"""
        # Frame pour l'en-tête
        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=80
        )
        header_frame.grid(row=0, column=0, padx=0, pady=(20, 30), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Logo/Icône
        logo_label = ctk.CTkLabel(
            header_frame,
            text="🎓",
            font=ctk.CTkFont(size=40)
        )
        logo_label.grid(row=0, column=0, pady=(0, 5))
        
        # Titre de l'application
        title_label = ctk.CTkLabel(
            header_frame,
            text="Centre Soutien",
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_LARGE, weight="bold"),
            text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK)
        )
        title_label.grid(row=1, column=0)
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Gestion Éducative",
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_SMALL),
            text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
        )
        subtitle_label.grid(row=2, column=0, pady=(2, 0))
        
        # Séparateur
        separator = ctk.CTkFrame(
            self,
            height=1,
            fg_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK)
        )
        separator.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
    
    def _create_menu_items(self):
        """Crée tous les éléments de menu avec icônes"""
        menu_items = [
            ("Dashboard", "dashboard", ModernTheme.ICONS['dashboard'], 2),
            ("Élèves", "students", ModernTheme.ICONS['students'], 3),
            ("Enseignants", "teachers", ModernTheme.ICONS['teachers'], 4),
            ("Matières", "subjects", ModernTheme.ICONS['subjects'], 5),
            ("Groupes", "groups", ModernTheme.ICONS['groups'], 6),
            ("Paiements", "payments", ModernTheme.ICONS['payments'], 7),
            ("Présence", "presence", ModernTheme.ICONS['presence'], 8),
        ]
        
        for text, name, icon, row in menu_items:
            btn = ModernMenuButton(
                self,
                text=text,
                icon=icon,
                command=lambda n=name: self._on_menu_click(n)
            )
            btn.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
            self.menu_buttons[name] = btn
            
        # Sélectionner le dashboard par défaut
        self.menu_buttons["dashboard"].set_selected(True)
    
    def _create_footer(self):
        """Crée le pied de page avec bouton déconnexion"""
        # Séparateur
        separator = ctk.CTkFrame(
            self,
            height=1,
            fg_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK)
        )
        separator.grid(row=11, column=0, padx=20, pady=(10, 15), sticky="ew")
        
        # Bouton de déconnexion
        logout_btn = ctk.CTkButton(
            self,
            text=f"{ModernTheme.ICONS['logout']}  Déconnexion",
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
            height=ModernTheme.BUTTON_HEIGHT,
            corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
            fg_color="transparent",
            text_color=(ModernTheme.DANGER, ModernTheme.DANGER),
            hover_color=(ModernTheme.SIDEBAR_HOVER_LIGHT, ModernTheme.SIDEBAR_HOVER_DARK),
            border_width=2,
            border_color=(ModernTheme.DANGER, ModernTheme.DANGER),
            anchor="center",
            command=self._on_logout
        )
        logout_btn.grid(row=12, column=0, padx=15, pady=(0, 20), sticky="ew")
    
    def _on_menu_click(self, view_name):
        """Gère le clic sur un élément de menu"""
        # Désélectionner tous les boutons
        for btn in self.menu_buttons.values():
            btn.set_selected(False)
        
        # Sélectionner le bouton cliqué
        if view_name in self.menu_buttons:
            self.menu_buttons[view_name].set_selected(True)
        
        self.current_view = view_name
        
        # Appeler le callback
        if self.callback:
            self.callback(view_name)
    
    def _on_logout(self):
        """Gère la déconnexion"""
        print("Déconnexion...")
        # TODO: Implémenter la vraie déconnexion
        
    def set_active_view(self, view_name):
        """Change la vue active programmatiquement"""
        if view_name in self.menu_buttons:
            self._on_menu_click(view_name)
