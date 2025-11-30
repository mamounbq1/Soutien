"""
Page de gestion des matières modernisée
Utilise les composants modernes pour un design professionnel
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import ModernTheme
from widgets.modern_components import (
    ModernButton,
    ModernEntry,
    ModernLabel,
    ModernTextBox,
    ModernCard,
    SearchBar,
    PageHeader,
    TableHeader,
    TableRow,
    ActionButtons
)


class SubjectForm(ctk.CTkToplevel):
    """Formulaire de matière modernisé"""
    
    def __init__(self, parent, db_manager, subject_data=None, callback=None):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.subject_data = subject_data
        self.callback = callback
        
        # Configuration de la fenêtre
        self.title("📚 Ajouter une Matière" if not subject_data else "✏️ Modifier la Matière")
        self.geometry("550x550")
        self.resizable(False, False)
        
        # Rendre modal
        self.transient(parent)
        self.grab_set()
        
        # Configuration du fond
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        self._create_ui()
        
        if subject_data:
            self._fill_fields()
        
        # Centrer la fenêtre
        self._center_window()
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_ui(self):
        """Crée l'interface du formulaire"""
        # Container principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # En-tête
        header = ModernLabel(
            main_container,
            text="📚 Informations de la matière",
            style='heading'
        )
        header.pack(pady=(0, 25))
        
        # Carte de formulaire
        form_card = ModernCard(main_container)
        form_card.pack(fill="both", expand=True)
        
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Nom
        ModernLabel(form_content, text="Nom *", style='normal').pack(anchor="w", pady=(0, 5))
        self.nom = ModernEntry(form_content, placeholder="Ex: Mathématiques")
        self.nom.pack(fill="x", pady=(0, 15))
        
        # Description
        ModernLabel(form_content, text="Description", style='normal').pack(anchor="w", pady=(0, 5))
        self.description = ModernTextBox(form_content, height=120)
        self.description.pack(fill="x", pady=(0, 15))
        
        # Tarif mensuel
        ModernLabel(form_content, text="Tarif Mensuel (DH)", style='normal').pack(anchor="w", pady=(0, 5))
        self.tarif_mensuel = ModernEntry(form_content, placeholder="Ex: 500")
        self.tarif_mensuel.pack(fill="x", pady=(0, 10))
        
        # Note
        note_label = ModernLabel(
            form_content,
            text="* Champs obligatoires",
            style='small'
        )
        note_label.pack(anchor="w", pady=(10, 0))
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        cancel_btn = ModernButton(
            buttons_frame,
            text="Annuler",
            icon="❌",
            style='outline',
            command=self.destroy
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = ModernButton(
            buttons_frame,
            text="Enregistrer",
            icon="💾",
            style='success',
            command=self._save_subject
        )
        save_btn.pack(side="right")
    
    def _fill_fields(self):
        """Remplit les champs avec les données existantes"""
        self.nom.insert(0, self.subject_data[1])
        self.description.insert("1.0", self.subject_data[2] or "")
        self.tarif_mensuel.insert(0, str(self.subject_data[3]) if self.subject_data[3] else "")
    
    def _save_subject(self):
        """Sauvegarde la matière"""
        data = {
            "nom": self.nom.get(),
            "description": self.description.get("1.0", "end-1c"),
            "tarif_mensuel": self.tarif_mensuel.get()
        }
        
        if not data["nom"]:
            messagebox.showerror("Erreur", "Le nom de la matière est obligatoire.")
            return
        
        # Validate tarif
        try:
            if data["tarif_mensuel"]:
                data["tarif_mensuel"] = float(data["tarif_mensuel"])
            else:
                data["tarif_mensuel"] = 0.0
        except ValueError:
            messagebox.showerror("Erreur", "Le tarif mensuel doit être un nombre.")
            return

        if self.subject_data:
            self.db_manager.update_subject(self.subject_data[0], **data)
            messagebox.showinfo("✅ Succès", "Matière modifiée avec succès.")
        else:
            self.db_manager.add_subject(**data)
            messagebox.showinfo("✅ Succès", "Matière ajoutée avec succès.")
        
        if self.callback:
            self.callback()
        self.destroy()


class SubjectsPage(ctk.CTkFrame):
    """Page de gestion des matières modernisée"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.db_manager = db_manager
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self._create_ui()
        self._load_subjects()
    
    def _create_ui(self):
        """Crée l'interface utilisateur"""
        # En-tête de page
        header = PageHeader(
            self,
            title="📚 Gestion des Matières",
            subtitle="Gérez le catalogue des matières enseignées",
            add_button_text="Nouvelle Matière",
            add_callback=self._open_add_dialog
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Barre de recherche
        search_bar = SearchBar(
            self,
            placeholder="Rechercher une matière...",
            search_callback=self._perform_search,
            refresh_callback=self._load_subjects
        )
        search_bar.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Carte conteneur pour le tableau
        table_card = ModernCard(self)
        table_card.grid(row=2, column=0, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)
        
        # En-tête du tableau
        headers = TableHeader(
            table_card,
            columns=["Nom", "Description", "Tarif Mensuel", "Actions"]
        )
        headers.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        
        # Frame scrollable pour les données
        self.scroll_frame = ctk.CTkScrollableFrame(
            table_card,
            fg_color="transparent"
        )
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.scroll_frame.grid_columnconfigure(0, weight=1)
    
    def _load_subjects(self, subjects=None):
        """Charge et affiche les matières"""
        # Nettoyer le contenu existant
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        if subjects is None:
            subjects = self.db_manager.get_all_subjects()
        
        if not subjects:
            no_data = ModernLabel(
                self.scroll_frame,
                text="Aucune matière trouvée",
                style='secondary'
            )
            no_data.pack(pady=40)
            return
        
        # Créer les lignes du tableau
        for i, subject in enumerate(subjects):
            self._create_subject_row(subject, i)
    
    def _create_subject_row(self, subject, index):
        """Crée une ligne pour une matière"""
        # Boutons d'action
        actions = ActionButtons(
            self.scroll_frame,
            on_edit=lambda s=subject: self._open_edit_dialog(s),
            on_delete=lambda id=subject[0]: self._delete_subject(id)
        )
        
        # Données de la ligne
        desc = subject[2][:50] + "..." if subject[2] and len(subject[2]) > 50 else (subject[2] or "-")
        data = [
            subject[1],  # Nom
            desc,  # Description (tronquée)
            f"{subject[3]} DH" if subject[3] else "-",  # Tarif
        ]
        
        # Créer la ligne
        row = TableRow(
            self.scroll_frame,
            data=data,
            actions_widget=actions,
            is_alternate=(index % 2 == 0)
        )
        row.pack(fill="x", pady=2)
    
    def _open_add_dialog(self):
        """Ouvre le dialogue d'ajout"""
        SubjectForm(self, self.db_manager, callback=self._load_subjects)
    
    def _open_edit_dialog(self, subject):
        """Ouvre le dialogue de modification"""
        SubjectForm(
            self,
            self.db_manager,
            subject_data=subject,
            callback=self._load_subjects
        )
    
    def _delete_subject(self, subject_id):
        """Supprime une matière"""
        if messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment supprimer cette matière ?\nCette action est irréversible."
        ):
            self.db_manager.delete_subject(subject_id)
            self._load_subjects()
            messagebox.showinfo("✅ Succès", "Matière supprimée avec succès.")
    
    def _perform_search(self, query):
        """Effectue une recherche"""
        if query:
            results = self.db_manager.search_subjects(query)
            self._load_subjects(results)
        else:
            self._load_subjects()
