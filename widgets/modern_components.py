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
        
        # Extraire height des kwargs s'il existe, sinon utiliser le défaut
        height = kwargs.pop('height', ModernTheme.BUTTON_HEIGHT)
        
        super().__init__(
            master,
            text=display_text,
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL, weight="normal"),
            height=height,
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
    
    def __init__(self, master, text, style='normal', font_size=None, font_weight=None, **kwargs):
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
        
        # Support pour font_size et font_weight personnalisés
        if font_size is not None or font_weight is not None:
            # Extraire la taille et le poids actuels du style
            current_font = label_style.get('font', ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL))
            size = font_size if font_size is not None else ModernTheme.FONT_SIZE_NORMAL
            weight = font_weight if font_weight is not None else "normal"
            label_style['font'] = ctk.CTkFont(size=size, weight=weight)
        
        # Fusionner label_style et kwargs, en donnant priorité aux kwargs
        # pour éviter les conflits (ex: font défini deux fois)
        final_kwargs = {**label_style, **kwargs}
        
        super().__init__(
            master,
            text=text,
            **final_kwargs
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
        
        # Bouton d'ajout optionnel (plus visible)
        if add_button_text and add_callback:
            add_btn = ModernButton(
                self,
                text=add_button_text,
                icon=ModernTheme.ICONS['add'],
                style='primary',
                width=180,  # Largeur augmentée pour meilleure visibilité
                height=40,  # Hauteur augmentée
                command=add_callback
            )
            add_btn.pack(side="right", padx=10, pady=5)


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
        # Utiliser un seul string 'transparent' au lieu d'un tuple
        if is_alternate:
            bg_color = (ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK)
        else:
            bg_color = "transparent"
        
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


class ScrollableTable(ctk.CTkScrollableFrame):
    """
    Tableau scrollable avec bordures
    - Support du scroll vertical automatique
    - Bordures sur toutes les cellules
    - En-têtes avec background
    - Lignes alternées
    """
    
    def __init__(self, master, headers, column_weights=None, **kwargs):
        """
        Args:
            master: Widget parent
            headers: Liste des noms de colonnes
            column_weights: Liste des poids pour chaque colonne
        """
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.headers = headers
        self.num_cols = len(headers)
        self.column_weights = column_weights or [1] * self.num_cols
        self.current_row = 1
        
        # Configuration des colonnes
        for i, weight in enumerate(self.column_weights):
            self.grid_columnconfigure(i, weight=weight)
        
        # Créer les en-têtes
        self._create_headers()
    
    def _create_headers(self):
        """Crée la ligne d'en-têtes avec bordures"""
        for col, header in enumerate(self.headers):
            header_frame = ctk.CTkFrame(
                self,
                fg_color=(ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK),
                corner_radius=0,
                border_width=1,
                border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK)
            )
            header_frame.grid(row=0, column=col, sticky="nsew", padx=0, pady=0)
            
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK),
                anchor="w"
            )
            header_label.pack(padx=8, pady=6, fill="both", expand=True)
    
    def add_row(self, data, is_alternate=None):
        """Ajoute une ligne au tableau (identique à BorderedTable)"""
        if is_alternate is None:
            is_alternate = (self.current_row % 2 == 0)
        
        row_color = (ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK) if is_alternate else "transparent"
        
        col = 0
        for cell_data in data:
            if isinstance(cell_data, dict):
                text = cell_data.get("text", "")
                colspan = cell_data.get("colspan", 1)
                fg_color = cell_data.get("fg", None)
                font_size = cell_data.get("font_size", 11)
                font_weight = cell_data.get("font_weight", "normal")
                
                cell_frame = ctk.CTkFrame(
                    self,
                    fg_color=row_color,
                    corner_radius=0,
                    border_width=1,
                    border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK)
                )
                cell_frame.grid(row=self.current_row, column=col, columnspan=colspan, sticky="nsew", padx=0, pady=0)
                
                cell_label = ctk.CTkLabel(
                    cell_frame,
                    text=str(text),
                    font=ctk.CTkFont(size=font_size, weight=font_weight),
                    text_color=fg_color or (ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
                    anchor="center" if colspan > 1 else "w"
                )
                cell_label.pack(padx=8, pady=6, fill="both", expand=True)
                col += colspan
                continue
            
            cell_frame = ctk.CTkFrame(
                self,
                fg_color=row_color,
                corner_radius=0,
                border_width=1,
                border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK)
            )
            cell_frame.grid(row=self.current_row, column=col, sticky="nsew", padx=0, pady=0)
            
            if callable(cell_data):
                widget = cell_data(cell_frame)
                widget.pack(padx=6, pady=4)
            elif isinstance(cell_data, ctk.CTkBaseClass):
                cell_data.pack(padx=6, pady=4)
            else:
                cell_label = ctk.CTkLabel(
                    cell_frame,
                    text=str(cell_data),
                    font=ctk.CTkFont(size=11),
                    text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
                    anchor="w"
                )
                cell_label.pack(padx=8, pady=6, fill="both", expand=True)
            
            col += 1
        
        row_index = self.current_row
        self.current_row += 1
        return row_index
    
    def clear_rows(self):
        """Supprime toutes les lignes de données (garde les en-têtes)"""
        for widget in self.winfo_children():
            info = widget.grid_info()
            if info and info.get('row', 0) > 0:
                widget.destroy()
        self.current_row = 1


class BorderedTable(ctk.CTkFrame):
    """
    Tableau avec bordures complètes (grille style Excel)
    - Bordures sur toutes les cellules
    - En-têtes avec background
    - Lignes alternées
    - Configuration des colonnes flexible
    - Support du tri par colonnes
    """
    
    def __init__(self, master, headers, column_weights=None, sortable=False, **kwargs):
        """
        Args:
            master: Widget parent
            headers: Liste des noms de colonnes (ex: ["Nom", "Prénom", "Actions"])
            column_weights: Liste des poids pour chaque colonne (ex: [2, 1, 1])
                           Si None, toutes les colonnes ont weight=1
            sortable: Si True, active le tri par clic sur les en-têtes
        """
        super().__init__(
            master,
            fg_color="transparent",
            **kwargs
        )
        
        self.headers = headers
        self.num_cols = len(headers)
        self.column_weights = column_weights or [1] * self.num_cols
        self.current_row = 1  # Row 0 = headers
        self.sortable = sortable
        self.sort_column = None
        self.sort_reverse = False
        self.data_rows = []  # Stocker les données pour le tri
        
        # Configuration des colonnes
        for i, weight in enumerate(self.column_weights):
            self.grid_columnconfigure(i, weight=weight)
        
        # Créer les en-têtes
        self._create_headers()
    
    def _create_headers(self):
        """Crée la ligne d'en-têtes avec bordures"""
        for col, header in enumerate(self.headers):
            header_frame = ctk.CTkFrame(
                self,
                fg_color=(ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK),
                corner_radius=0,
                border_width=1,
                border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK)
            )
            header_frame.grid(row=0, column=col, sticky="nsew", padx=0, pady=0)
            
            # Ajouter indicateur de tri si activé
            header_text = header
            if self.sortable and col < len(self.headers) - 1:  # Pas de tri sur la colonne Actions
                header_text = f"{header} ▼▲"
            
            header_label = ctk.CTkLabel(
                header_frame,
                text=header_text,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK),
                anchor="w"
            )
            header_label.pack(padx=8, pady=6, fill="both", expand=True)
            
            # Bind du clic pour tri
            if self.sortable and col < len(self.headers) - 1:
                header_frame.configure(cursor="hand2")
                header_frame.bind("<Button-1>", lambda e, c=col: self._sort_by_column(c))
                header_label.bind("<Button-1>", lambda e, c=col: self._sort_by_column(c))
    
    def _sort_by_column(self, col_index):
        """Trie les données par colonne"""
        if not self.data_rows:
            return
        
        # Inverser l'ordre si on clique sur la même colonne
        if self.sort_column == col_index:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col_index
            self.sort_reverse = False
        
        # Trier les données
        try:
            self.data_rows.sort(
                key=lambda row: str(row[col_index]) if col_index < len(row) else "",
                reverse=self.sort_reverse
            )
        except (IndexError, TypeError):
            pass  # Ignorer les erreurs de tri
        
        # Rafraîchir l'affichage
        self.clear_rows()
        for row_data in self.data_rows:
            self.add_row(row_data)
    
    def add_row(self, data, is_alternate=None):
        """
        Ajoute une ligne de données au tableau
        
        Args:
            data: Liste de valeurs ou widgets pour chaque colonne
                 - Si string/nombre: crée un Label automatiquement
                 - Si widget CTk: utilise directement le widget
                 - Si dict: {"text": "...", "colspan": 2, "fg": color, "font_size": 11, "font_weight": "bold"}
            is_alternate: Si None, alterne automatiquement
        
        Returns:
            row_index: Index de la ligne ajoutée
        """
        if is_alternate is None:
            is_alternate = (self.current_row % 2 == 0)
        
        # Couleur de fond alternée
        if is_alternate:
            row_color = (ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK)
        else:
            row_color = "transparent"
        
        # Créer une cellule pour chaque donnée
        col = 0
        for cell_data in data:
            # Support pour dictionnaire avec options avancées
            if isinstance(cell_data, dict):
                text = cell_data.get("text", "")
                colspan = cell_data.get("colspan", 1)
                fg_color = cell_data.get("fg", None)
                font_size = cell_data.get("font_size", 11)
                font_weight = cell_data.get("font_weight", "normal")
                
                cell_frame = ctk.CTkFrame(
                    self,
                    fg_color=row_color,
                    corner_radius=0,
                    border_width=1,
                    border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK)
                )
                cell_frame.grid(row=self.current_row, column=col, columnspan=colspan, sticky="nsew", padx=0, pady=0)
                
                cell_label = ctk.CTkLabel(
                    cell_frame,
                    text=str(text),
                    font=ctk.CTkFont(size=font_size, weight=font_weight),
                    text_color=fg_color or (ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
                    anchor="center" if colspan > 1 else "w"
                )
                cell_label.pack(padx=8, pady=6, fill="both", expand=True)
                col += colspan
                continue
            
            cell_frame = ctk.CTkFrame(
                self,
                fg_color=row_color,
                corner_radius=0,
                border_width=1,
                border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK)
            )
            cell_frame.grid(row=self.current_row, column=col, sticky="nsew", padx=0, pady=0)
            
            # Si c'est une fonction (callback), l'appeler avec cell_frame comme parent
            if callable(cell_data):
                widget = cell_data(cell_frame)
                widget.pack(padx=6, pady=4)
            # Si c'est un widget CTk existant, il doit avoir cell_frame comme parent
            elif isinstance(cell_data, ctk.CTkBaseClass):
                cell_data.pack(padx=6, pady=4)
            else:
                # Sinon créer un label pour texte/nombre
                cell_label = ctk.CTkLabel(
                    cell_frame,
                    text=str(cell_data),
                    font=ctk.CTkFont(size=11),
                    text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
                    anchor="w"
                )
                cell_label.pack(padx=8, pady=6, fill="both", expand=True)
            
            col += 1
        
        # Stocker les données pour le tri (seulement les valeurs texte/nombre)
        if self.sortable:
            simple_data = []
            for cell_data in data:
                if isinstance(cell_data, dict):
                    simple_data.append(cell_data.get("text", ""))
                elif callable(cell_data) or isinstance(cell_data, ctk.CTkBaseClass):
                    simple_data.append("")  # Les widgets ne peuvent pas être triés
                else:
                    simple_data.append(cell_data)
            self.data_rows.append(simple_data)
        
        row_index = self.current_row
        self.current_row += 1
        return row_index
    
    def clear_rows(self):
        """Supprime toutes les lignes de données (garde les en-têtes)"""
        for widget in self.winfo_children():
            info = widget.grid_info()
            if info and info.get('row', 0) > 0:
                widget.destroy()
        self.current_row = 1
        if self.sortable:
            self.data_rows = []
    
    def clear(self):
        """Alias pour clear_rows() pour compatibilité"""
        self.clear_rows()


# ════════════════════════════════════════════════════════════════
# COMPOSANT LOADING/SPINNER
# ════════════════════════════════════════════════════════════════

class LoadingSpinner(ctk.CTkFrame):
    """Spinner de chargement animé"""
    
    def __init__(self, parent, text: str = "Chargement...", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(
            fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK),
            corner_radius=ModernTheme.RADIUS_MD
        )
        
        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, padx=40, pady=40)
        
        # Progressbar circulaire
        self.progress = ctk.CTkProgressBar(
            container,
            mode="indeterminate",
            width=200,
            height=8,
            corner_radius=4,
            fg_color=(ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK),
            progress_color=(ModernTheme.PRIMARY, ModernTheme.PRIMARY)
        )
        self.progress.pack(pady=(0, 15))
        self.progress.start()
        
        # Label de texte
        self.label = ctk.CTkLabel(
            container,
            text=text,
            font=ctk.CTkFont(size=14),
            text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
        )
        self.label.pack()
    
    def update_text(self, text: str):
        """Mettre à jour le texte"""
        self.label.configure(text=text)
    
    def stop(self):
        """Arrêter l'animation"""
        self.progress.stop()
    
    def destroy(self):
        """Détruire le widget"""
        self.stop()
        super().destroy()


class LoadingOverlay(ctk.CTkToplevel):
    """Overlay de chargement modal"""
    
    def __init__(self, parent, text: str = "Chargement en cours..."):
        super().__init__(parent)
        
        # Configuration
        self.title("")
        self.geometry("400x200")
        self.resizable(False, False)
        
        # Rendre modal
        self.transient(parent)
        self.grab_set()
        
        # Retirer les décorations
        self.overrideredirect(True)
        
        # Configuration du fond semi-transparent
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        self.attributes('-alpha', 0.95)
        
        # Centrer
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (200 // 2)
        self.geometry(f"+{x}+{y}")
        
        # Spinner
        self.spinner = LoadingSpinner(self, text=text)
        self.spinner.pack(expand=True, fill="both")
    
    def update_text(self, text: str):
        """Mettre à jour le texte"""
        self.spinner.update_text(text)
    
    def close(self):
        """Fermer l'overlay"""
        self.spinner.stop()
        self.grab_release()
        self.destroy()


# ════════════════════════════════════════════════════════════════
# HELPER POUR OPÉRATIONS ASYNCHRONES
# ════════════════════════════════════════════════════════════════

import threading

def run_with_loading(parent, operation, callback=None, loading_text="Traitement..."):
    """
    Exécuter une opération longue avec overlay de loading
    
    Args:
        parent: Widget parent
        operation: Fonction à exécuter (sans arguments)
        callback: Fonction appelée avec le résultat (optionnel)
        loading_text: Texte à afficher
    
    Usage:
        def my_operation():
            # Code long
            return result
        
        def on_complete(result):
            print(f"Terminé: {result}")
        
        run_with_loading(self, my_operation, on_complete, "Calcul en cours...")
    """
    overlay = LoadingOverlay(parent, loading_text)
    
    def worker():
        try:
            result = operation()
            
            # Fermer l'overlay dans le thread principal
            parent.after(0, lambda: overlay.close())
            
            # Callback avec résultat
            if callback:
                parent.after(0, lambda: callback(result))
        
        except Exception as e:
            parent.after(0, lambda: overlay.close())
            parent.after(0, lambda: print(f"❌ Erreur: {e}"))
    
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
