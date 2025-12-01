"""
Page de gestion des élèves modernisée
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
    ModernComboBox,
    ModernCard,
    SearchBar,
    PageHeader,
    BorderedTable,
    ActionButtons
)
from utils import center_window
from utils.messages import Messages


class StudentForm(ctk.CTkToplevel):
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
        center_window(self)
    
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
        
        # Niveau (ComboBox with values from DB)
        self._create_field(form_content, "Niveau", 2)
        niveaux = self._get_niveaux()
        self.niveau = ModernComboBox(
            form_content,
            values=niveaux
        )
        self.niveau.set("")
        self.niveau.grid(row=2, column=1, pady=10, sticky="ew")
        
        # Téléphone
        self._create_field(form_content, "Téléphone", 3)
        self.tel = ModernEntry(form_content, placeholder="Ex: 0612345678")
        self.tel.grid(row=3, column=1, pady=10, sticky="ew")
        
        # Téléphone parent
        self._create_field(form_content, "Tél. Parents", 4)
        self.parent_tel = ModernEntry(form_content, placeholder="Ex: 0698765432")
        self.parent_tel.grid(row=4, column=1, pady=10, sticky="ew")
        
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
    
    def _get_niveaux(self):
        """Récupérer la liste des niveaux depuis la DB"""
        try:
            niveaux_data = self.db_manager.get_all_niveaux(actif_only=True)
            return [n[1] for n in niveaux_data]  # n[1] = nom_niveau
        except:
            # Fallback values if DB fails
            return ["Primaire", "Collège", "Lycée", "Supérieur"]
    
    def _fill_fields(self):
        """Remplit les champs avec les données existantes"""
        # Format DB: (id, nom, prenom, telephone, adresse, ..., classe as niveau)
        # Indices: 0=id, 1=nom, 2=prenom, 3=tel, 4=adresse, ..., 10=classe (shown as niveau)
        self.nom.insert(0, self.student_data[1])
        self.prenom.insert(0, self.student_data[2])
        # ComboBox uses .set() not .insert()
        self.niveau.set(self.student_data[10] if len(self.student_data) > 10 and self.student_data[10] else "")
        self.tel.insert(0, self.student_data[3] or "")
        
        # Extraire tel parent depuis adresse
        parent_tel = ""
        if len(self.student_data) > 4 and self.student_data[4]:
            parts = self.student_data[4].split('|')
            for part in parts:
                if part.startswith("Parent:"):
                    parent_tel = part.replace("Parent:", "").strip()
        self.parent_tel.insert(0, parent_tel)
    
    def _save_student(self):
        """Sauvegarde l'élève"""
        if not self.nom.get() or not self.prenom.get():
            messagebox.showerror(Messages.ERROR_TITLE, Messages.STUDENT_NAME_REQUIRED)
            return
        
        # Construction adresse (juste tel parent)
        adresse = ""
        if self.parent_tel.get():
            adresse = f"Parent: {self.parent_tel.get()}"
        
        try:
            if self.student_data:
                # Modification - store niveau in classe field, leave filiere empty
                self.db_manager.update_eleve(
                    self.student_data[0],
                    self.nom.get(),
                    self.prenom.get(),
                    "",  # filiere not used
                    self.niveau.get(),  # niveau stored in classe
                    self.tel.get(),
                    adresse
                )
                messagebox.showinfo(Messages.SUCCESS_TITLE, Messages.STUDENT_UPDATED)
            else:
                # Ajout - store niveau in classe field, leave filiere empty
                self.db_manager.add_eleve(
                    self.nom.get(),
                    self.prenom.get(),
                    "",  # filiere not used
                    self.niveau.get(),  # niveau stored in classe
                    self.tel.get(),
                    adresse
                )
                messagebox.showinfo(Messages.SUCCESS_TITLE, Messages.STUDENT_ADDED)
        except ValueError as e:
            messagebox.showerror(Messages.ERROR_TITLE, str(e))
            return
        
        if self.callback:
            self.callback()
        self.destroy()


class StudentsPage(ctk.CTkFrame):
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
        
        # Zone de recherche et filtres
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        search_frame.grid_columnconfigure(0, weight=1)
        
        # Barre de recherche
        search_bar = SearchBar(
            search_frame,
            placeholder="Rechercher un élève par nom, prénom ou téléphone...",
            search_callback=self._perform_search,
            refresh_callback=self._load_students
        )
        search_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Frame pour filtres
        filters_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        filters_frame.grid(row=1, column=0, sticky="w")
        
        # Label "Filtrer par:"
        filter_label = ModernLabel(
            filters_frame,
            text="Filtrer par niveau:",
            style='normal'
        )
        filter_label.pack(side="left", padx=(0, 10))
        
        # ComboBox niveau
        self.filter_niveau = ModernComboBox(
            filters_frame,
            values=["Tous", "Primaire", "Collège", "Lycée", "Supérieur"],
            width=150
        )
        self.filter_niveau.set("Tous")
        self.filter_niveau.configure(command=self._apply_filters)
        self.filter_niveau.pack(side="left", padx=(0, 10))
        
        # Bouton appliquer filtres
        apply_filter_btn = ModernButton(
            filters_frame,
            text="Appliquer",
            icon="🔍",
            style='primary',
            width=120,
            command=self._apply_filters
        )
        apply_filter_btn.pack(side="left")
        
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
            headers=["Nom", "Prénom", "Niveau", "Téléphone", "Tél Parents", "Actions"],
            column_weights=[2, 2, 1, 1, 1, 1]  # Nom et Prénom plus larges
        )
        self.table.grid(row=0, column=0, sticky="nsew")
    
    def _load_students(self, students=None):
        """Charge et affiche les élèves"""
        # Nettoyer les lignes existantes
        self.table.clear_rows()
        
        if students is None:
            students = self.db_manager.get_all_eleves()  # DIRECT - pas de conversion
        
        if not students:
            # Message si aucun élève
            no_data_label = ctk.CTkLabel(
                self.table,
                text="Aucun élève enregistré",
                font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
                text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
            )
            no_data_label.grid(row=1, column=0, columnspan=6, pady=40)
            return
        
        # Ajouter chaque élève au tableau
        for student in students:
            self._add_student_row(student)
    
    def _add_student_row(self, student):
        """Ajoute une ligne élève au tableau"""
        # Stocker les callbacks avec l'ID de l'élève
        student_id = student[0]
        
        # Fonction callback qui créera les boutons dans la cellule
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
                command=lambda: self._open_edit_dialog(student)
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
                command=lambda: self._delete_student(student_id)
            )
            delete_btn.pack(side="left")
            
            return actions_container
        
        # Ajouter la ligne avec les données (fonction callback pour actions)
        # Format DB: (id, nom, prenom, telephone, adresse, ..., filiere, classe)
        # Indices: 0=id, 1=nom, 2=prenom, 3=tel, 4=adresse, 9=filiere, 10=classe
        
        # Extraire téléphone parent depuis adresse
        tel_parent = ""
        if len(student) > 4 and student[4]:
            parts = student[4].split('|')
            for part in parts:
                if part.startswith("Parent:"):
                    tel_parent = part.replace("Parent:", "").strip()
        
        # Construire niveau depuis classe
        niveau = student[10] if len(student) > 10 else ""
        
        self.table.add_row([
            student[1],  # Nom
            student[2],  # Prénom
            niveau or "-",  # Niveau (=classe)
            student[3] or "-",  # Téléphone
            tel_parent or "-",  # Tél Parents (extrait de adresse)
            create_actions_widget  # Fonction callback
        ])
    
    def _open_add_dialog(self):
        """Ouvre le dialogue d'ajout"""
        StudentForm(self, self.db_manager, callback=self._load_students)
    
    def _open_edit_dialog(self, student):
        """Ouvre le dialogue de modification"""
        StudentForm(
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
        """Effectue une recherche avec filtres"""
        if query:
            results = self.db_manager.search_students(query)
        else:
            results = self.db_manager.get_all_eleves()  # DIRECT - pas de conversion
        
        # Appliquer le filtre de niveau
        niveau_filter = self.filter_niveau.get()
        if niveau_filter != "Tous" and results:
            results = [s for s in results if s[3] == niveau_filter]
        
        self._load_students(results)
    
    def _apply_filters(self, *args):
        """Applique les filtres actifs"""
        self._perform_search(None)
