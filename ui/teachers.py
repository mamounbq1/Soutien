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
    BorderedTable,
    ActionButtons
)
from ui.print_dialogs import PrintTeacherPayslipDialog


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
        
        # Barre de recherche et bouton d'impression
        search_container = ctk.CTkFrame(self, fg_color="transparent")
        search_container.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        search_container.grid_columnconfigure(0, weight=1)
        
        search_bar = SearchBar(
            search_container,
            placeholder="Rechercher un enseignant par nom, prénom ou matière...",
            search_callback=self._perform_search,
            refresh_callback=self._load_teachers
        )
        search_bar.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ModernButton(
            search_container,
            text="🖨️ Fiche de Paie",
            command=self._open_print_dialog,
            style='primary',
            width=160
        ).grid(row=0, column=1)
        
        # Carte conteneur pour le tableau
        table_card = ModernCard(self)
        table_card.grid(row=2, column=0, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(0, weight=1)
        
        # Frame scrollable pour le tableau
        scroll_container = ctk.CTkScrollableFrame(
            table_card,
            fg_color="transparent"
        )
        scroll_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        scroll_container.grid_columnconfigure(0, weight=1)
        
        # Tableau avec bordures (style Dashboard)
        self.table = BorderedTable(
            scroll_container,
            headers=["Nom", "Prénom", "Matière", "Téléphone", "Salaire/h", "Actions"],
            column_weights=[2, 2, 1, 1, 1, 1]
        )
        self.table.grid(row=0, column=0, sticky="nsew")
    
    def _load_teachers(self, teachers=None):
        """Charge et affiche les enseignants"""
        # Nettoyer les lignes existantes
        self.table.clear_rows()
        
        if teachers is None:
            teachers = self.db_manager.get_all_teachers()
        
        if not teachers:
            no_data_label = ctk.CTkLabel(
                self.table,
                text="Aucun enseignant enregistré",
                font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
                text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
            )
            no_data_label.grid(row=1, column=0, columnspan=6, pady=40)
            return
        
        # Ajouter chaque enseignant au tableau
        for teacher in teachers:
            self._add_teacher_row(teacher)
    
    def _add_teacher_row(self, teacher):
        """Ajoute une ligne enseignant au tableau"""
        teacher_id = teacher[0]
        
        def create_actions_widget(cell_frame):
            """Crée les boutons d'action dans la cellule fournie"""
            actions_container = ctk.CTkFrame(cell_frame, fg_color="transparent")
            
            # Bouton éditer
            edit_btn = ctk.CTkButton(
                actions_container,
                text="Modifier",
                width=70,
                height=26,
                corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
                fg_color=(ModernTheme.WARNING, ModernTheme.WARNING),
                hover_color=("#F57C00", "#F57C00"),
                font=ctk.CTkFont(size=11),
                command=lambda: self._open_edit_dialog(teacher)
            )
            edit_btn.pack(side="left", padx=(0, 4))
            
            # Bouton supprimer
            delete_btn = ctk.CTkButton(
                actions_container,
                text="Supprimer",
                width=75,
                height=26,
                corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
                fg_color=(ModernTheme.DANGER, ModernTheme.DANGER),
                hover_color=(ModernTheme.BTN_DANGER_HOVER, ModernTheme.BTN_DANGER_HOVER),
                font=ctk.CTkFont(size=11),
                command=lambda: self._delete_teacher(teacher_id)
            )
            delete_btn.pack(side="left")
            
            return actions_container
        
        # Ajouter la ligne avec les données
        self.table.add_row([
            teacher[1],  # Nom
            teacher[2],  # Prénom
            teacher[3] or "-",  # Matière
            teacher[4] or "-",  # Téléphone
            f"{teacher[5]} DH" if teacher[5] else "-",  # Salaire
            create_actions_widget
        ])
    
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
    
    def _open_print_dialog(self):
        """Ouvre le dialogue d'impression de fiche de paie"""
        PrintTeacherPayslipDialog(self, self.db_manager)
    
    def _perform_search(self, query):
        """Effectue une recherche"""
        if query:
            results = self.db_manager.search_teachers(query)
            self._load_teachers(results)
        else:
            self._load_teachers()
