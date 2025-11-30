"""
Exemple de page Élèves modernisée
Démontre l'utilisation des composants modernes
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
    ModernComboBox,
    ModernCard,
    SearchBar,
    PageHeader,
    TableHeader,
    TableRow,
    ActionButtons
)


class ModernStudentForm(ctk.CTkToplevel):
    """Formulaire d'élève modernisé"""
    
    def __init__(self, parent, db_manager, student_data=None, callback=None):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.student_data = student_data
        self.callback = callback
        
        # Configuration de la fenêtre
        self.title("📝 Ajouter un Élève" if not student_data else "✏️ Modifier l'Élève")
        self.geometry("550x700")
        self.resizable(False, False)
        
        # Rendre modal
        self.transient(parent)
        self.grab_set()
        
        # Configuration du fond
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        self._create_ui()
        
        if student_data:
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
        main_container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # En-tête
        header = ModernLabel(
            main_container,
            text="👨‍🎓 Informations de l'élève",
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
        self.nom = ModernEntry(form_content, placeholder="Ex: Alami")
        self.nom.grid(row=0, column=1, pady=10, sticky="ew")
        
        # Prénom
        self._create_field(form_content, "Prénom *", 1)
        self.prenom = ModernEntry(form_content, placeholder="Ex: Ahmed")
        self.prenom.grid(row=1, column=1, pady=10, sticky="ew")
        
        # Niveau
        self._create_field(form_content, "Niveau", 2)
        self.niveau = ModernComboBox(
            form_content,
            values=["Primaire", "Collège", "Lycée", "Supérieur"]
        )
        self.niveau.set("Lycée")
        self.niveau.grid(row=2, column=1, pady=10, sticky="ew")
        
        # Filière
        self._create_field(form_content, "Filière/Classe", 3)
        self.filiere = ModernEntry(form_content, placeholder="Ex: 1ère Bac Sciences")
        self.filiere.grid(row=3, column=1, pady=10, sticky="ew")
        
        # Téléphone
        self._create_field(form_content, "Téléphone", 4)
        self.tel = ModernEntry(form_content, placeholder="Ex: 0612345678")
        self.tel.grid(row=4, column=1, pady=10, sticky="ew")
        
        # Téléphone parent
        self._create_field(form_content, "Tél. Parents", 5)
        self.parent_tel = ModernEntry(form_content, placeholder="Ex: 0698765432")
        self.parent_tel.grid(row=5, column=1, pady=10, sticky="ew")
        
        # Note
        note_label = ModernLabel(
            form_content,
            text="* Champs obligatoires",
            style='small'
        )
        note_label.grid(row=6, column=0, columnspan=2, pady=(15, 5), sticky="w")
        
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
            command=self._save_student
        )
        save_btn.pack(side="right")
    
    def _create_field(self, parent, text, row):
        """Crée un label de champ"""
        label = ModernLabel(parent, text=text, style='normal')
        label.grid(row=row, column=0, padx=(0, 15), pady=10, sticky="w")
    
    def _fill_fields(self):
        """Remplit les champs avec les données existantes"""
        self.nom.insert(0, self.student_data[1])
        self.prenom.insert(0, self.student_data[2])
        self.niveau.set(self.student_data[3])
        self.filiere.insert(0, self.student_data[4])
        self.tel.insert(0, self.student_data[5])
        self.parent_tel.insert(0, self.student_data[6])
    
    def _save_student(self):
        """Sauvegarde l'élève"""
        data = {
            "nom": self.nom.get(),
            "prenom": self.prenom.get(),
            "niveau": self.niveau.get(),
            "filiere": self.filiere.get(),
            "tel": self.tel.get(),
            "parent_tel": self.parent_tel.get()
        }
        
        if not data["nom"] or not data["prenom"]:
            messagebox.showerror("Erreur", "Le nom et le prénom sont obligatoires.")
            return
        
        if self.student_data:
            self.db_manager.update_student(self.student_data[0], **data)
            messagebox.showinfo("✅ Succès", "Élève modifié avec succès.")
        else:
            self.db_manager.add_student(**data)
            messagebox.showinfo("✅ Succès", "Élève ajouté avec succès.")
        
        if self.callback:
            self.callback()
        self.destroy()


class ModernStudentsPage(ctk.CTkFrame):
    """Page de gestion des élèves modernisée"""
    
    def __init__(self, parent, db_manager):
        super().__init__(
            parent,
            fg_color="transparent"
        )
        
        self.db_manager = db_manager
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self._create_ui()
        self._load_students()
    
    def _create_ui(self):
        """Crée l'interface utilisateur"""
        # En-tête de page
        header = PageHeader(
            self,
            title="👨‍🎓 Gestion des Élèves",
            subtitle="Gérez vos élèves facilement",
            add_button_text="Nouvel Élève",
            add_callback=self._open_add_dialog
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Barre de recherche
        search_bar = SearchBar(
            self,
            placeholder="Rechercher un élève par nom, prénom ou téléphone...",
            search_callback=self._perform_search,
            refresh_callback=self._load_students
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
            columns=["Nom", "Prénom", "Niveau", "Filière", "Téléphone", "Actions"]
        )
        headers.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        
        # Frame scrollable pour les données
        self.scroll_frame = ctk.CTkScrollableFrame(
            table_card,
            fg_color="transparent"
        )
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.scroll_frame.grid_columnconfigure(0, weight=1)
    
    def _load_students(self, students=None):
        """Charge et affiche les élèves"""
        # Nettoyer le contenu existant
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        if students is None:
            students = self.db_manager.get_all_students()
        
        if not students:
            no_data = ModernLabel(
                self.scroll_frame,
                text="Aucun élève trouvé",
                style='secondary'
            )
            no_data.pack(pady=40)
            return
        
        # Créer les lignes du tableau
        for i, student in enumerate(students):
            self._create_student_row(student, i)
    
    def _create_student_row(self, student, index):
        """Crée une ligne pour un élève"""
        # Boutons d'action
        actions = ActionButtons(
            self.scroll_frame,
            on_edit=lambda s=student: self._open_edit_dialog(s),
            on_delete=lambda id=student[0]: self._delete_student(id)
        )
        
        # Données de la ligne
        data = [
            student[1],  # Nom
            student[2],  # Prénom
            student[3],  # Niveau
            student[4],  # Filière
            student[5],  # Téléphone
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
        ModernStudentForm(self, self.db_manager, callback=self._load_students)
    
    def _open_edit_dialog(self, student):
        """Ouvre le dialogue de modification"""
        ModernStudentForm(
            self,
            self.db_manager,
            student_data=student,
            callback=self._load_students
        )
    
    def _delete_student(self, student_id):
        """Supprime un élève"""
        if messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment supprimer cet élève ?\nCette action est irréversible."
        ):
            self.db_manager.delete_student(student_id)
            self._load_students()
            messagebox.showinfo("✅ Succès", "Élève supprimé avec succès.")
    
    def _perform_search(self, query):
        """Effectue une recherche"""
        if query:
            results = self.db_manager.search_students(query)
            self._load_students(results)
        else:
            self._load_students()
