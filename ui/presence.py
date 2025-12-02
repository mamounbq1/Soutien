"""
Page de gestion des présences modernisée
Utilise les composants modernes pour un design professionnel
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import ModernTheme
from widgets.modern_components import (
    ModernButton,
    ModernEntry,
    ModernLabel,
    ModernComboBox,
    ModernCard,
    PageHeader
)


class PresencePage(ctk.CTkFrame):
    """Page de gestion des présences modernisée"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.db_manager = db_manager
        self.selected_group_id = None
        self.selected_date = datetime.now().strftime("%Y-%m-%d")
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self._create_ui()
    
    def _create_ui(self):
        """Crée l'interface utilisateur"""
        # En-tête de page
        header = PageHeader(
            self,
            title="📋 Feuille de Présence",
            subtitle="Gérez les présences par groupe et par date",
            add_button_text=None  # Pas de bouton d'ajout pour cette page
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Panneau de sélection
        self._create_selection_panel()
        
        # Tableau de présence
        self._create_presence_table()
    
    def _create_selection_panel(self):
        """Crée le panneau de sélection"""
        selection_card = ModernCard(self)
        selection_card.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        selection_content = ctk.CTkFrame(selection_card, fg_color="transparent")
        selection_content.pack(fill="both", expand=True, padx=25, pady=25)
        selection_content.grid_columnconfigure((0, 1), weight=1)
        
        # Sélection du groupe
        ModernLabel(selection_content, text="Groupe *", style='normal').grid(
            row=0, column=0, padx=(0, 15), pady=(0, 10), sticky="w"
        )
        
        groups = self.db_manager.get_all_groups()
        group_names = [f"{g[0]} - {g[1]}" for g in groups]
        self.group_combo = ModernComboBox(
            selection_content,
            values=group_names if group_names else ["Aucun groupe"],
            command=self._on_group_select
        )
        self.group_combo.grid(row=0, column=1, pady=(0, 10), sticky="ew")
        
        # Sélection de la date
        ModernLabel(selection_content, text="Date *", style='normal').grid(
            row=1, column=0, padx=(0, 15), pady=(0, 10), sticky="w"
        )
        
        self.date_entry = ModernEntry(selection_content, placeholder="YYYY-MM-DD")
        self.date_entry.insert(0, self.selected_date)
        self.date_entry.grid(row=1, column=1, pady=(0, 10), sticky="ew")
        
        # Bouton de chargement
        load_btn = ModernButton(
            selection_content,
            text="Charger la Présence",
            icon="📋",
            style='primary',
            command=self._load_presence
        )
        load_btn.grid(row=2, column=0, columnspan=2, pady=(15, 0), sticky="ew")
    
    def _create_presence_table(self):
        """Crée le tableau de présence"""
        table_card = ModernCard(self)
        table_card.grid(row=2, column=0, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)
        
        # En-tête du tableau avec BorderedTable style
        header_frame = ctk.CTkFrame(
            table_card,
            fg_color=(ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK),
            corner_radius=0
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        header_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        headers = ["Nom", "Prénom", "Statut"]
        for i, h in enumerate(headers):
            # Cellule de header avec bordures
            header_cell = ctk.CTkFrame(
                header_frame,
                fg_color="transparent",
                border_width=1,
                border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK),
                corner_radius=0
            )
            header_cell.grid(row=0, column=i, sticky="nsew")
            
            ModernLabel(
                header_cell,
                text=h,
                font_size=10,
                font_weight="bold"
            ).pack(padx=8, pady=6)
        
        # Frame scrollable pour le contenu
        self.scroll_frame = ctk.CTkScrollableFrame(
            table_card,
            fg_color="transparent"
        )
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.scroll_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Message d'information initial
        self.info_label = ModernLabel(
            self.scroll_frame,
            text="📋 Sélectionnez un groupe et une date pour charger la présence",
            style='secondary'
        )
        self.info_label.grid(row=0, column=0, columnspan=3, pady=50)
        
        # Bouton de sauvegarde
        self.btn_save = ModernButton(
            table_card,
            text="Enregistrer la Présence",
            icon="💾",
            style='success',
            command=self._save_presence,
            state="disabled"
        )
        self.btn_save.grid(row=2, column=0, pady=20, padx=20, sticky="ew")
    
    def _on_group_select(self, choice):
        """Gère la sélection d'un groupe"""
        if choice and choice != "Aucun groupe":
            try:
                self.selected_group_id = int(choice.split(" - ")[0])
            except:
                self.selected_group_id = None
    
    def _load_presence(self):
        """Charge la présence pour le groupe et la date sélectionnés"""
        if not self.selected_group_id:
            messagebox.showerror("Erreur", "Veuillez sélectionner un groupe.")
            return
        
        self.selected_date = self.date_entry.get()
        
        # Valider le format de date
        try:
            datetime.strptime(self.selected_date, "%Y-%m-%d")
        except:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez YYYY-MM-DD.")
            return
        
        # Nettoyer le contenu précédent
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Obtenir les étudiants du groupe
        students = self.db_manager.get_group_students(self.selected_group_id)
        
        if not students:
            no_students = ModernLabel(
                self.scroll_frame,
                text="Aucun élève dans ce groupe",
                style='secondary'
            )
            no_students.grid(row=0, column=0, columnspan=3, pady=50)
            self.btn_save.configure(state="disabled")
            return
        
        # Vérifier si la présence existe déjà pour cette date
        existing_presence = self.db_manager.get_presence_by_group_date(
            self.selected_group_id,
            self.selected_date
        )
        presence_dict = {p[1]: p[4] for p in existing_presence}  # student_id: status
        
        # Créer les lignes de présence
        self.presence_widgets = []
        for i, student in enumerate(students):
            # student: (id, nom, prenom, tel, date_inscription)
            self._create_presence_row(student, i, presence_dict)
        
        self.btn_save.configure(state="normal")
    
    def _create_presence_row(self, student, index, presence_dict):
        """Crée une ligne de présence pour un étudiant"""
        student_id = student[0]
        
        # Frame de ligne avec bordures (style BorderedTable)
        row_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=(
                ModernTheme.BG_HOVER_LIGHT if index % 2 == 0 else ModernTheme.BG_CARD_LIGHT,
                ModernTheme.BG_HOVER_DARK if index % 2 == 0 else ModernTheme.BG_CARD_DARK
            ),
            corner_radius=0
        )
        row_frame.grid(row=index, column=0, columnspan=3, sticky="ew", pady=0)
        row_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Nom - avec bordure
        nom_cell = ctk.CTkFrame(
            row_frame,
            fg_color="transparent",
            border_width=1,
            border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK),
            corner_radius=0
        )
        nom_cell.grid(row=0, column=0, sticky="nsew")
        ModernLabel(nom_cell, text=student[1], font_size=11).pack(padx=8, pady=6)
        
        # Prénom - avec bordure
        prenom_cell = ctk.CTkFrame(
            row_frame,
            fg_color="transparent",
            border_width=1,
            border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK),
            corner_radius=0
        )
        prenom_cell.grid(row=0, column=1, sticky="nsew")
        ModernLabel(prenom_cell, text=student[2], font_size=11).pack(padx=8, pady=6)
        
        # Statut (Radio buttons) - avec bordure
        status_cell = ctk.CTkFrame(
            row_frame,
            fg_color="transparent",
            border_width=1,
            border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK),
            corner_radius=0
        )
        status_cell.grid(row=0, column=2, sticky="nsew")
        
        status_frame = ctk.CTkFrame(status_cell, fg_color="transparent")
        status_frame.pack(padx=8, pady=6)
        
        status_var = ctk.StringVar(value=presence_dict.get(student_id, "present"))
        
        # Style des radio buttons
        rb_present = ctk.CTkRadioButton(
            status_frame,
            text="✓ Présent",
            variable=status_var,
            value="present",
            fg_color=ModernTheme.SUCCESS,
            hover_color=ModernTheme.BTN_SUCCESS_HOVER
        )
        rb_present.pack(side="left", padx=8)
        
        rb_absent = ctk.CTkRadioButton(
            status_frame,
            text="✗ Absent",
            variable=status_var,
            value="absent",
            fg_color=ModernTheme.DANGER,
            hover_color=ModernTheme.BTN_DANGER_HOVER
        )
        rb_absent.pack(side="left", padx=8)
        
        rb_late = ctk.CTkRadioButton(
            status_frame,
            text="⌚ Retard",
            variable=status_var,
            value="retard",
            fg_color=ModernTheme.WARNING,
            hover_color=ModernTheme.BTN_WARNING_HOVER
        )
        rb_late.pack(side="left", padx=8)
        
        self.presence_widgets.append({
            "student_id": student_id,
            "status_var": status_var
        })
    
    def _save_presence(self):
        """Sauvegarde la présence"""
        if not self.selected_group_id or not hasattr(self, 'presence_widgets'):
            messagebox.showerror("Erreur", "Aucune présence à enregistrer.")
            return
        
        # Sauvegarder la présence de chaque étudiant
        for widget_data in self.presence_widgets:
            student_id = widget_data["student_id"]
            status = widget_data["status_var"].get()
            
            # Vérifier si l'enregistrement existe
            existing = self.db_manager.check_presence_exists(
                self.selected_group_id,
                student_id,
                self.selected_date
            )
            
            if existing:
                # Mettre à jour l'enregistrement existant
                self.db_manager.update_presence(existing[0], status)
            else:
                # Créer un nouvel enregistrement
                self.db_manager.add_presence(
                    self.selected_group_id,
                    student_id,
                    self.selected_date,
                    status
                )
        
        messagebox.showinfo("✅ Succès", "Présence enregistrée avec succès.")
        self._load_presence()  # Recharger pour afficher les données sauvegardées
