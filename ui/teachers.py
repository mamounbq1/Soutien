"""
Page de gestion des enseignants modernisée
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
    ModernCard,
    SearchBar,
    PageHeader,
    TableHeader,
    TableRow,
    ActionButtons
)


class TeacherForm(ctk.CTkToplevel):
    """Formulaire d'enseignant modernisé"""
    
    def __init__(self, parent, db_manager, teacher_data=None, callback=None):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.teacher_data = teacher_data
        self.callback = callback
        
        # Configuration de la fenêtre
        self.title("👨‍🏫 Ajouter un Enseignant" if not teacher_data else "✏️ Modifier l'Enseignant")
        self.geometry("550x600")
        self.resizable(False, False)
        
        # Rendre modal
        self.transient(parent)
        self.grab_set()
        
        # Configuration du fond
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        self._create_ui()
        
        if teacher_data:
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
            text="👨‍🏫 Informations de l'enseignant",
            style='heading'
        )
        header.pack(pady=(0, 25))
        
        # Carte de formulaire
        form_card = ModernCard(main_container)
        form_card.pack(fill="both", expand=True)
        
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Grille pour les champs
        form_content.grid_columnconfigure(1, weight=1)
        
        # Nom
        self._create_field(form_content, "Nom *", 0)
        self.nom = ModernEntry(form_content, placeholder="Ex: Bennani")
        self.nom.grid(row=0, column=1, pady=10, sticky="ew")
        
        # Prénom
        self._create_field(form_content, "Prénom *", 1)
        self.prenom = ModernEntry(form_content, placeholder="Ex: Fatima")
        self.prenom.grid(row=1, column=1, pady=10, sticky="ew")
        
        # Matière
        self._create_field(form_content, "Matière", 2)
        self.matiere = ModernEntry(form_content, placeholder="Ex: Mathématiques")
        self.matiere.grid(row=2, column=1, pady=10, sticky="ew")
        
        # Téléphone
        self._create_field(form_content, "Téléphone", 3)
        self.tel = ModernEntry(form_content, placeholder="Ex: 0612345678")
        self.tel.grid(row=3, column=1, pady=10, sticky="ew")
        
        # Salaire horaire
        self._create_field(form_content, "Salaire Horaire (DH)", 4)
        self.salaire_horaire = ModernEntry(form_content, placeholder="Ex: 150")
        self.salaire_horaire.grid(row=4, column=1, pady=10, sticky="ew")
        
        # Note
        note_label = ModernLabel(
            form_content,
            text="* Champs obligatoires",
            style='small'
        )
        note_label.grid(row=5, column=0, columnspan=2, pady=(15, 5), sticky="w")
        
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
            command=self._save_teacher
        )
        save_btn.pack(side="right")
    
    def _create_field(self, parent, text, row):
        """Crée un label de champ"""
        label = ModernLabel(parent, text=text, style='normal')
        label.grid(row=row, column=0, padx=(0, 15), pady=10, sticky="w")
    
    def _fill_fields(self):
        """Remplit les champs avec les données existantes"""
        self.nom.insert(0, self.teacher_data[1])
        self.prenom.insert(0, self.teacher_data[2])
        self.matiere.insert(0, self.teacher_data[3] or "")
        self.tel.insert(0, self.teacher_data[4] or "")
        self.salaire_horaire.insert(0, str(self.teacher_data[5]) if self.teacher_data[5] else "")
    
    def _save_teacher(self):
        """Sauvegarde l'enseignant"""
        data = {
            "nom": self.nom.get(),
            "prenom": self.prenom.get(),
            "matiere": self.matiere.get(),
            "tel": self.tel.get(),
            "salaire_horaire": self.salaire_horaire.get()
        }
        
        if not data["nom"] or not data["prenom"]:
            messagebox.showerror("Erreur", "Le nom et le prénom sont obligatoires.")
            return
        
        # Validate salaire_horaire
        try:
            if data["salaire_horaire"]:
                data["salaire_horaire"] = float(data["salaire_horaire"])
            else:
                data["salaire_horaire"] = 0.0
        except ValueError:
            messagebox.showerror("Erreur", "Le salaire horaire doit être un nombre.")
            return

        if self.teacher_data:
            self.db_manager.update_teacher(self.teacher_data[0], **data)
            messagebox.showinfo("✅ Succès", "Enseignant modifié avec succès.")
        else:
            self.db_manager.add_teacher(**data)
            messagebox.showinfo("✅ Succès", "Enseignant ajouté avec succès.")
        
        if self.callback:
            self.callback()
        self.destroy()


class TeachersPage(ctk.CTkFrame):
    """Page de gestion des enseignants modernisée"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.db_manager = db_manager
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self._create_ui()
        self._load_teachers()
    
    def _create_ui(self):
        """Crée l'interface utilisateur"""
        # En-tête de page
        header = PageHeader(
            self,
            title="👨‍🏫 Gestion des Enseignants",
            subtitle="Gérez votre équipe pédagogique",
            add_button_text="Nouvel Enseignant",
            add_callback=self._open_add_dialog
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Barre de recherche
        search_bar = SearchBar(
            self,
            placeholder="Rechercher un enseignant par nom, prénom ou matière...",
            search_callback=self._perform_search,
            refresh_callback=self._load_teachers
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
            columns=["Nom", "Prénom", "Matière", "Téléphone", "Salaire/h", "Actions"]
        )
        headers.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        
        # Frame scrollable pour les données
        self.scroll_frame = ctk.CTkScrollableFrame(
            table_card,
            fg_color="transparent"
        )
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.scroll_frame.grid_columnconfigure(0, weight=1)
    
    def _load_teachers(self, teachers=None):
        """Charge et affiche les enseignants"""
        # Nettoyer le contenu existant
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        if teachers is None:
            teachers = self.db_manager.get_all_teachers()
        
        if not teachers:
            no_data = ModernLabel(
                self.scroll_frame,
                text="Aucun enseignant trouvé",
                style='secondary'
            )
            no_data.pack(pady=40)
            return
        
        # Créer les lignes du tableau
        for i, teacher in enumerate(teachers):
            self._create_teacher_row(teacher, i)
    
    def _create_teacher_row(self, teacher, index):
        """Crée une ligne pour un enseignant"""
        # Boutons d'action
        actions = ActionButtons(
            self.scroll_frame,
            on_edit=lambda t=teacher: self._open_edit_dialog(t),
            on_delete=lambda id=teacher[0]: self._delete_teacher(id)
        )
        
        # Données de la ligne
        data = [
            teacher[1],  # Nom
            teacher[2],  # Prénom
            teacher[3] or "-",  # Matière
            teacher[4] or "-",  # Téléphone
            f"{teacher[5]} DH" if teacher[5] else "-",  # Salaire
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
        TeacherForm(self, self.db_manager, callback=self._load_teachers)
    
    def _open_edit_dialog(self, teacher):
        """Ouvre le dialogue de modification"""
        TeacherForm(
            self,
            self.db_manager,
            teacher_data=teacher,
            callback=self._load_teachers
        )
    
    def _delete_teacher(self, teacher_id):
        """Supprime un enseignant"""
        if messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment supprimer cet enseignant ?\nCette action est irréversible."
        ):
            self.db_manager.delete_teacher(teacher_id)
            self._load_teachers()
            messagebox.showinfo("✅ Succès", "Enseignant supprimé avec succès.")
    
    def _perform_search(self, query):
        """Effectue une recherche"""
        if query:
            results = self.db_manager.search_teachers(query)
            self._load_teachers(results)
        else:
            self._load_teachers()
