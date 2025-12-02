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
from widgets.virtual_table import VirtualScrollTable
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
            placeholder="Rechercher par Nom, Prénom ou ID Élève...",
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
        
        # ComboBox niveau - Load from DB
        niveaux_list = self._get_niveaux()
        filter_values = ["Tous"] + niveaux_list
        self.filter_niveau = ModernComboBox(
            filters_frame,
            values=filter_values,
            width=200
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
        
        # Virtual Scrolling Table (High Performance) with Pagination
        # Optimized column widths to fill the entire space
        self.table = VirtualScrollTable(
            table_card,
            headers=["Nom", "Prénom", "Niveau", "Téléphone", "Tél. Parents", "Actions"],
            column_widths=[200, 200, 160, 145, 145, 100],  # Increased widths (total: 950px)
            row_height=45,
            visible_rows=12,  # 12 rows visible (ensures all 10 students are fully visible)
            rows_per_page=10,  # Show 10 students per page
            enable_pagination=True  # Enable pagination
        )
        self.table.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Set row action callbacks
        self.table.set_row_callback("edit", self._open_edit_dialog_from_data)
        self.table.set_row_callback("delete", self._delete_student_from_data)
    
    def _load_students(self, students=None):
        """Charge et affiche les élèves"""
        if students is None:
            students = self.db_manager.get_all_eleves()  # DIRECT - pas de conversion
        
        if not students:
            # Clear table and show no data message
            self.table.clear()
            return
        
        # Prepare data for virtual table
        table_data = []
        self.student_id_map = {}  # Map row index to student data
        
        for idx, student in enumerate(students):
            # Extract data with CORRECT indices
            tel_parent = ""
            if len(student) > 4 and student[4]:
                parts = student[4].split('|')
                for part in parts:
                    if part.startswith("Parent:"):
                        tel_parent = part.replace("Parent:", "").strip()
            
            # Build niveau: CLASSE or FILIERE or "CLASSE FILIERE"
            classe = student[10] if len(student) > 10 and student[10] else ""
            filiere = student[9] if len(student) > 9 and student[9] else ""
            
            # Smart niveau display
            if classe and filiere and filiere not in classe:
                niveau = f"{classe} {filiere}"  # Ex: "Collège 2AC"
            elif filiere:
                niveau = filiere  # Ex: "Prépa", "Licence"
            elif classe:
                niveau = classe  # Ex: "Supérieur"
            else:
                niveau = ""
            
            # Add row data
            row_data = [
                student[1],           # Nom
                student[2],           # Prénom
                niveau or "-",        # Niveau (combined classe + filiere)
                student[3] or "-",   # Téléphone
                tel_parent or "-",   # Tél Parents
                "Actions"             # Actions placeholder
            ]
            table_data.append(row_data)
            self.student_id_map[idx] = student  # Store full student data
        
        # Set data to virtual table (only renders visible rows)
        self.table.set_data(table_data)
    
    def _open_edit_dialog_from_data(self, row_data):
        """Open edit dialog from row data (for virtual table callback)"""
        # Get row index from current selection
        row_index = self.table.get_selected_row_index()
        if row_index is not None and row_index in self.student_id_map:
            student = self.student_id_map[row_index]
            self._open_edit_dialog(student)
    
    def _delete_student_from_data(self, row_data):
        """Delete student from row data (for virtual table callback)"""
        # Get row index from current selection
        row_index = self.table.get_selected_row_index()
        if row_index is not None and row_index in self.student_id_map:
            student = self.student_id_map[row_index]
            student_id = student[0]
            self._delete_student(student_id)
    
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
            # Filtrage intelligent basé sur la structure de niveau
            filtered = []
            for s in results:
                filiere = s[9] if len(s) > 9 else ""  # Index 9 = filiere (niveau détaillé)
                classe = s[10] if len(s) > 10 else ""  # Index 10 = classe (catégorie)
                
                # Si niveau sélectionné contient un espace (ex: "Primaire CE1")
                if " " in niveau_filter:
                    # Matcher "classe + filiere" (ex: "Primaire" + "CE1" = "Primaire CE1")
                    full_niveau = f"{classe} {filiere}".strip()
                    if full_niveau == niveau_filter:
                        filtered.append(s)
                else:
                    # Matcher soit filiere soit classe directement
                    if filiere == niveau_filter or classe == niveau_filter:
                        filtered.append(s)
            results = filtered
        
        self._load_students(results)
    
    def _apply_filters(self, *args):
        """Applique les filtres actifs"""
        self._perform_search(None)
    
    def _get_niveaux(self):
        """Récupérer la liste des niveaux depuis la DB"""
        try:
            niveaux_data = self.db_manager.get_all_niveaux(actif_only=True)
            return [n[1] for n in niveaux_data]  # n[1] = nom_niveau
        except:
            # Fallback values if DB fails
            return ["Primaire", "Collège", "Lycée", "Supérieur"]
