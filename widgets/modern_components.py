"""
Composants réutilisables modernisés
- Boutons stylisés
- Champs de saisie
- Tableaux
- Formulaires
"""

import customtkinter as ctk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import ModernTheme


class ModernButton(ctk.CTkButton):
    """Bouton modernisé avec différents styles"""
    
    STYLES = {
        'primary': {
            'fg_color': (ModernTheme.BTN_PRIMARY, ModernTheme.BTN_PRIMARY),
            'hover_color': (ModernTheme.BTN_PRIMARY_HOVER, ModernTheme.BTN_PRIMARY_HOVER),
            'text_color': 'white',
        },
        'secondary': {
            'fg_color': (ModernTheme.BTN_SECONDARY, ModernTheme.BTN_SECONDARY),
            'hover_color': (ModernTheme.BTN_SECONDARY_HOVER, ModernTheme.BTN_SECONDARY_HOVER),
            'text_color': 'white',
        },
        'success': {
            'fg_color': (ModernTheme.BTN_SUCCESS, ModernTheme.BTN_SUCCESS),
            'hover_color': (ModernTheme.BTN_SUCCESS_HOVER, ModernTheme.BTN_SUCCESS_HOVER),
            'text_color': 'white',
        },
        'danger': {
            'fg_color': (ModernTheme.BTN_DANGER, ModernTheme.BTN_DANGER),
            'hover_color': (ModernTheme.BTN_DANGER_HOVER, ModernTheme.BTN_DANGER_HOVER),
            'text_color': 'white',
        },
        'outline': {
            'fg_color': 'transparent',
            'hover_color': (ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK),
            'text_color': (ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
            'border_width': 2,
            'border_color': (ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK),
        },
    }
    
    def __init__(self, master, text, icon=None, style='primary', **kwargs):
        button_style = self.STYLES.get(style, self.STYLES['primary'])
        
        # Ajouter l'icône au texte si présente
        display_text = f"{icon}  {text}" if icon else text
        
        super().__init__(
            master,
            text=display_text,
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL, weight="normal"),
            height=ModernTheme.BUTTON_HEIGHT,
            corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
            **button_style,
            **kwargs
        )


class ModernEntry(ctk.CTkEntry):
    """Champ de saisie modernisé"""
    
    def __init__(self, master, placeholder="", **kwargs):
        super().__init__(
            master,
            placeholder_text=placeholder,
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
            height=ModernTheme.INPUT_HEIGHT,
            corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
            border_width=1,
            border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK),
            **kwargs
        )


class ModernLabel(ctk.CTkLabel):
    """Label modernisé avec différents styles"""
    
    def __init__(self, master, text, style='normal', **kwargs):
        styles = {
            'title': {
                'font': ctk.CTkFont(size=ModernTheme.FONT_SIZE_XXLARGE, weight="bold"),
                'text_color': (ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
            },
            'heading': {
                'font': ctk.CTkFont(size=ModernTheme.FONT_SIZE_LARGE, weight="bold"),
                'text_color': (ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
            },
            'subheading': {
                'font': ctk.CTkFont(size=ModernTheme.FONT_SIZE_MEDIUM, weight="bold"),
                'text_color': (ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
            },
            'normal': {
                'font': ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
                'text_color': (ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
            },
            'secondary': {
                'font': ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
                'text_color': (ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK),
            },
            'small': {
                'font': ctk.CTkFont(size=ModernTheme.FONT_SIZE_SMALL),
                'text_color': (ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK),
            },
        }
        
        label_style = styles.get(style, styles['normal'])
        
        super().__init__(
            master,
            text=text,
            **label_style,
            **kwargs
        )


class ModernComboBox(ctk.CTkComboBox):
    """ComboBox modernisé"""
    
    def __init__(self, master, values=None, **kwargs):
        super().__init__(
            master,
            values=values or [],
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
            height=ModernTheme.INPUT_HEIGHT,
            corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
            border_width=1,
            border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK),
            button_color=(ModernTheme.PRIMARY, ModernTheme.PRIMARY),
            button_hover_color=(ModernTheme.PRIMARY_DARK, ModernTheme.PRIMARY_DARK),
            **kwargs
        )


class ModernTextBox(ctk.CTkTextbox):
    """Zone de texte modernisée"""
    
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
            corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
            border_width=1,
            border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK),
            **kwargs
        )


class ModernCard(ctk.CTkFrame):
    """Carte modernisée pour contenir du contenu"""
    
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=ModernTheme.BORDER_RADIUS,
            fg_color=(ModernTheme.BG_CARD_LIGHT, ModernTheme.BG_CARD_DARK),
            **kwargs
        )


class SearchBar(ctk.CTkFrame):
    """Barre de recherche moderne"""
    
    def __init__(self, master, placeholder="Rechercher...", search_callback=None, refresh_callback=None):
        super().__init__(
            master,
            fg_color="transparent"
        )
        
        self.search_callback = search_callback
        self.refresh_callback = refresh_callback
        
        # Champ de recherche
        self.search_entry = ModernEntry(
            self,
            placeholder=placeholder
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Bouton rechercher
        search_btn = ModernButton(
            self,
            text="Rechercher",
            icon=ModernTheme.ICONS['search'],
            style='primary',
            width=120,
            command=self._on_search
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        # Bouton rafraîchir
        refresh_btn = ModernButton(
            self,
            text="",
            icon=ModernTheme.ICONS['refresh'],
            style='outline',
            width=40,
            command=self._on_refresh
        )
        refresh_btn.pack(side="left")
        
        # Bind Enter key
        self.search_entry.bind("<Return>", lambda e: self._on_search())
    
    def _on_search(self):
        if self.search_callback:
            query = self.search_entry.get()
            self.search_callback(query)
    
    def _on_refresh(self):
        if self.refresh_callback:
            self.search_entry.delete(0, 'end')
            self.refresh_callback()
    
    def get_query(self):
        return self.search_entry.get()


class ActionButtons(ctk.CTkFrame):
    """Boutons d'action pour les lignes de tableau"""
    
    def __init__(self, master, on_edit=None, on_delete=None):
        super().__init__(
            master,
            fg_color="transparent"
        )
        
        # Bouton éditer
        if on_edit:
            edit_btn = ctk.CTkButton(
                self,
                text=ModernTheme.ICONS['edit'],
                width=35,
                height=35,
                corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
                fg_color=(ModernTheme.WARNING, ModernTheme.WARNING),
                hover_color=("#F57C00", "#F57C00"),
                font=ctk.CTkFont(size=16),
                command=on_edit
            )
            edit_btn.pack(side="left", padx=(0, 5))
        
        # Bouton supprimer
        if on_delete:
            delete_btn = ctk.CTkButton(
                self,
                text=ModernTheme.ICONS['delete'],
                width=35,
                height=35,
                corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
                fg_color=(ModernTheme.DANGER, ModernTheme.DANGER),
                hover_color=(ModernTheme.BTN_DANGER_HOVER, ModernTheme.BTN_DANGER_HOVER),
                font=ctk.CTkFont(size=16),
                command=on_delete
            )
            delete_btn.pack(side="left")


class PageHeader(ctk.CTkFrame):
    """En-tête de page standardisé"""
    
    def __init__(self, master, title, subtitle=None, add_button_text=None, add_callback=None):
        super().__init__(
            master,
            fg_color="transparent"
        )
        
        # Frame gauche pour titre et sous-titre
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.pack(side="left", fill="x", expand=True)
        
        # Titre
        title_label = ModernLabel(left_frame, text=title, style='title')
        title_label.pack(anchor="w")
        
        # Sous-titre optionnel
        if subtitle:
            subtitle_label = ModernLabel(left_frame, text=subtitle, style='secondary')
            subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Bouton d'ajout optionnel
        if add_button_text and add_callback:
            add_btn = ModernButton(
                self,
                text=add_button_text,
                icon=ModernTheme.ICONS['add'],
                style='primary',
                command=add_callback
            )
            add_btn.pack(side="right")


class TableHeader(ctk.CTkFrame):
    """En-tête de tableau stylisé"""
    
    def __init__(self, master, columns):
        super().__init__(
            master,
            height=45,
            corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
            fg_color=(ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK)
        )
        
        # Configuration des colonnes
        num_cols = len(columns)
        for i in range(num_cols):
            self.grid_columnconfigure(i, weight=1)
        
        # Créer les labels d'en-tête
        for i, col_name in enumerate(columns):
            label = ModernLabel(
                self,
                text=col_name,
                style='subheading'
            )
            label.grid(row=0, column=i, padx=15, pady=10, sticky="w")


class TableRow(ctk.CTkFrame):
    """Ligne de tableau stylisée avec effet hover"""
    
    def __init__(self, master, data, actions_widget=None, is_alternate=False):
        bg_color = (
            (ModernTheme.BG_HOVER_LIGHT if is_alternate else "transparent",
             ModernTheme.BG_HOVER_DARK if is_alternate else "transparent")
        )
        
        super().__init__(
            master,
            fg_color=bg_color,
            corner_radius=ModernTheme.BORDER_RADIUS_SMALL
        )
        
        # Configuration des colonnes
        num_cols = len(data) + (1 if actions_widget else 0)
        for i in range(num_cols - 1):
            self.grid_columnconfigure(i, weight=1)
        if actions_widget:
            self.grid_columnconfigure(num_cols - 1, weight=0, minsize=100)
        
        # Afficher les données
        for i, value in enumerate(data):
            label = ModernLabel(self, text=str(value), style='normal')
            label.grid(row=0, column=i, padx=15, pady=12, sticky="w")
        
        # Ajouter les boutons d'action si fournis
        if actions_widget:
            actions_widget.grid(row=0, column=num_cols - 1, padx=15, pady=8, sticky="e")
        
        # Effet hover
        self.bind("<Enter>", lambda e: self.configure(
            fg_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK)
        ))
        self.bind("<Leave>", lambda e: self.configure(fg_color=bg_color))
