"""
Module de gestion des groupes - SIMPLIFIÉ
Groupes = Matière + Niveau + Élèves (prof et salle dans emploi du temps)
"""
import customtkinter as ctk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import ModernTheme
from widgets.modern_components import *


class GroupForm(ctk.CTkToplevel):
    """Formulaire de groupe simplifié et modernisé"""
    
    def __init__(self, parent, db_manager, group_data=None, callback=None):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.group_data = group_data
        self.callback = callback
        
        self.title("👥 Ajouter un Groupe" if not group_data else "✏️ Modifier le Groupe")
        self.geometry("600x700")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        self.subjects_list = self.db_manager.get_all_subjects()
        
        self._create_ui()
        
        if group_data:
            self._fill_fields()
            self._load_group_students()
        
        self._center_window()
    
    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_ui(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        header = ModernLabel(
            main_container,
            text="👥 Informations du groupe",
            style='heading'
        )
        header.pack(pady=(0, 25))
        
        # SECTION 1: Informations de base
        info_card = ModernCard(main_container)
        info_card.pack(fill="x", pady=(0, 15))
        
        info_content = ctk.CTkFrame(info_card, fg_color="transparent")
        info_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        ModernLabel(info_content, text="Nom du Groupe *", style='normal').pack(anchor="w", pady=(0, 5))
        self.nom = ModernEntry(info_content, placeholder="Ex: Groupe A - Maths 2nde")
        self.nom.pack(fill="x", pady=(0, 15))
        
        ModernLabel(info_content, text="Matière *", style='normal').pack(anchor="w", pady=(0, 5))
        subject_names = [f"{s[0]} - {s[1]}" for s in self.subjects_list] if self.subjects_list else ["Aucune matière"]
        self.matiere_combo = ModernComboBox(info_content, values=subject_names)
        self.matiere_combo.pack(fill="x", pady=(0, 15))
        
        ModernLabel(info_content, text="Niveau *", style='normal').pack(anchor="w", pady=(0, 5))
        niveaux = ["2nde", "1ère", "Terminale", "Bac+1", "Bac+2", "Autre"]
        self.niveau_combo = ModernComboBox(info_content, values=niveaux, command=self._on_niveau_change)
        self.niveau_combo.pack(fill="x", pady=(0, 10))
        
        # SECTION 2: Élèves inscrits (uniquement en mode édition)
        if self.group_data:
            students_card = ModernCard(main_container)
            students_card.pack(fill="both", expand=True, pady=(0, 15))
            
            students_content = ctk.CTkFrame(students_card, fg_color="transparent")
            students_content.pack(fill="both", expand=True, padx=25, pady=25)
            
            header_frame = ctk.CTkFrame(students_content, fg_color="transparent")
            header_frame.pack(fill="x", pady=(0, 10))
            
            ModernLabel(header_frame, text="👨‍🎓 Élèves inscrits", style='subheading').pack(side="left")
            self.count_label = ModernLabel(header_frame, text="(0)", style='secondary')
            self.count_label.pack(side="left", padx=(5, 0))
            
            # Ajouter un élève
            add_frame = ctk.CTkFrame(students_content, fg_color="transparent")
            add_frame.pack(fill="x", pady=(0, 10))
            
            # Combo sera rempli dynamiquement selon le niveau choisi
            self.student_combo = ModernComboBox(add_frame, values=["Sélectionnez un niveau d'abord"])
            self.student_combo.pack(side="left", fill="x", expand=True, padx=(0, 10))
            
            add_btn = ModernButton(
                add_frame,
                text="Ajouter",
                icon="➕",
                style='primary',
                width=100,
                command=self._add_student
            )
            add_btn.pack(side="right")
            
            # Liste des élèves
            self.students_scroll = ctk.CTkScrollableFrame(
                students_content,
                height=150,
                fg_color=(ModernTheme.TABLE_ALT_LIGHT, ModernTheme.TABLE_ALT_DARK)
            )
            self.students_scroll.pack(fill="both", expand=True)
            self.students_scroll.grid_columnconfigure(0, weight=1)
        
        # Note
        note_label = ModernLabel(
            main_container,
            text="* Champs obligatoires | Le professeur et la salle seront définis dans l'emploi du temps",
            style='small'
        )
        note_label.pack(anchor="w", pady=(10, 0))
        
        # Boutons
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
            command=self._save_group
        )
        save_btn.pack(side="right")
    
    def _fill_fields(self):
        if self.group_data:
            details = self.db_manager.get_group_details(self.group_data[0])
            if details:
                self.nom.insert(0, details[1])
                
                if details[2]:  # matiere_id
                    for s in self.subjects_list:
                        if s[0] == details[2]:
                            self.matiere_combo.set(f"{s[0]} - {s[1]}")
                            break
                
                if details[3]:  # niveau
                    self.niveau_combo.set(details[3])
                    # Charger les élèves disponibles pour ce niveau
                    self._update_student_list(details[3])
    
    def _on_niveau_change(self, niveau):
        """Callback quand le niveau change - met à jour la liste des élèves"""
        if self.group_data and hasattr(self, 'student_combo'):
            self._update_student_list(niveau)
    
    def _update_student_list(self, niveau):
        """Met à jour la liste des élèves disponibles selon le niveau"""
        if not hasattr(self, 'student_combo'):
            return
        
        # Récupérer tous les élèves
        all_students = self.db_manager.get_all_students()
        
        # Filtrer par niveau/classe
        # Format élève: (id, nom, prenom, tel, adresse, ..., filiere, classe)
        filtered_students = []
        for s in all_students:
            # s[10] = classe (ex: "1ère Année Bac", "Terminale", etc.)
            classe = s[10] if len(s) > 10 else ""
            
            # Correspondance niveau groupe <-> classe élève
            match = False
            if niveau == "2nde" and "2" in classe.lower():
                match = True
            elif niveau == "1ère" and ("1" in classe.lower() or "premi" in classe.lower()):
                match = True
            elif niveau == "Terminale" and ("term" in classe.lower() or "bac" in classe.lower()):
                match = True
            elif niveau == "Bac+1" and ("bac+1" in classe.lower() or "1ère année" in classe.lower()):
                match = True
            elif niveau == "Bac+2" and ("bac+2" in classe.lower() or "2ème année" in classe.lower()):
                match = True
            elif niveau == "Autre" or not niveau:
                match = True  # Afficher tous si "Autre" ou pas de niveau
            
            if match:
                filtered_students.append(s)
        
        # Mettre à jour le ComboBox
        if filtered_students:
            student_names = [f"{s[0]} - {s[1]} {s[2]}" for s in filtered_students]
            self.student_combo.configure(values=student_names)
            self.student_combo.set(student_names[0] if student_names else "")
        else:
            self.student_combo.configure(values=["Aucun élève pour ce niveau"])
            self.student_combo.set("Aucun élève pour ce niveau")
    
    def _load_group_students(self):
        """Charger les élèves du groupe"""
        if not self.group_data:
            return
        
        students = self.db_manager.get_group_students(self.group_data[0])
        
        # Nettoyer la liste
        for widget in self.students_scroll.winfo_children():
            widget.destroy()
        
        # Mettre à jour le compteur
        self.count_label.configure(text=f"({len(students)})")
        
        # Afficher les élèves
        for i, student in enumerate(students):
            self._create_student_row(student, i)
    
    def _create_student_row(self, student, index):
        """Créer une ligne pour un élève inscrit"""
        row_frame = ctk.CTkFrame(
            self.students_scroll,
            fg_color="transparent"
        )
        row_frame.grid(row=index, column=0, sticky="ew", pady=2, padx=5)
        row_frame.grid_columnconfigure(0, weight=1)
        
        student_label = ModernLabel(
            row_frame,
            text=f"• {student[1]} {student[2]}",
            style='normal'
        )
        student_label.pack(side="left")
        
        remove_btn = ModernButton(
            row_frame,
            text="Retirer",
            icon="🗑",
            style='danger',
            width=80,
            command=lambda s=student: self._remove_student(s)
        )
        remove_btn.pack(side="right")
    
    def _add_student(self):
        """Ajouter un élève au groupe"""
        if not self.group_data:
            messagebox.showwarning("Attention", "Enregistrez d'abord le groupe avant d'ajouter des élèves.")
            return
        
        selection = self.student_combo.get()
        if not selection or selection == "Aucun élève":
            messagebox.showerror("Erreur", "Veuillez sélectionner un élève.")
            return
        
        try:
            student_id = int(selection.split(" - ")[0])
        except:
            messagebox.showerror("Erreur", "Sélection invalide.")
            return
        
        # Ajouter l'inscription
        success = self.db_manager.add_inscription(student_id, self.group_data[0])
        
        if success:
            messagebox.showinfo("✅ Succès", "Élève ajouté au groupe.")
            self._load_group_students()
        else:
            messagebox.showwarning("Attention", "Cet élève est déjà inscrit dans ce groupe.")
    
    def _remove_student(self, student):
        """Retirer un élève du groupe"""
        if messagebox.askyesno("Confirmation", f"Retirer {student[1]} {student[2]} du groupe ?"):
            self.db_manager.remove_inscription(student[0], self.group_data[0])
            messagebox.showinfo("✅ Succès", "Élève retiré du groupe.")
            self._load_group_students()
    
    def _save_group(self):
        """Sauvegarder le groupe"""
        nom = self.nom.get()
        matiere_selection = self.matiere_combo.get()
        niveau = self.niveau_combo.get()
        
        if not nom:
            messagebox.showerror("Erreur", "Le nom du groupe est obligatoire.")
            return
        
        if not matiere_selection or matiere_selection == "Aucune matière":
            messagebox.showerror("Erreur", "Veuillez sélectionner une matière.")
            return
        
        try:
            matiere_id = int(matiere_selection.split(" - ")[0])
        except:
            messagebox.showerror("Erreur", "Sélection de matière invalide.")
            return
        
        if self.group_data:
            self.db_manager.update_group(self.group_data[0], nom, matiere_id, niveau)
            messagebox.showinfo("✅ Succès", "Groupe modifié avec succès.")
        else:
            group_id = self.db_manager.add_group(nom, matiere_id, niveau)
            messagebox.showinfo("✅ Succès", "Groupe créé avec succès.\nVous pouvez maintenant ajouter des élèves.")
            # Recharger le formulaire en mode édition
            self.group_data = (group_id,)
            self.destroy()
            if self.callback:
                self.callback()
            return
        
        if self.callback:
            self.callback()
        self.destroy()


class GroupsPage(ctk.CTkFrame):
    """Page de gestion des groupes modernisée et simplifiée"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.db_manager = db_manager
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self._create_ui()
        self._load_groups()
    
    def _create_ui(self):
        header = PageHeader(
            self,
            title="👥 Gestion des Groupes",
            subtitle="Créez des groupes par matière et niveau, puis ajoutez des élèves",
            add_button_text="Nouveau Groupe",
            add_callback=self._open_add_dialog
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        search_bar = SearchBar(
            self,
            placeholder="Rechercher un groupe...",
            search_callback=self._perform_search,
            refresh_callback=self._load_groups
        )
        search_bar.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        table_card = ModernCard(self)
        table_card.grid(row=2, column=0, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)
        
        # Table BorderedTable avec grille complète
        self.table = BorderedTable(
            table_card,
            headers=["Nom", "Matière", "Niveau", "Élèves", "Actions"],
            column_weights=[2, 2, 1, 1, 1]  # Nom, Matière, Niveau, Élèves, Actions
        )
        self.table.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    def _load_groups(self, groups=None):
        self.table.clear()
        
        if groups is None:
            groups = self.db_manager.get_all_groups()
        
        if not groups:
            self.table.add_row([{"text": "Aucun groupe trouvé", "colspan": 5, "fg": ModernTheme.TEXT_SECONDARY}])
            return
        
        for group in groups:
            self._create_group_row(group)
    
    def _create_group_row(self, group):
        # Compter les élèves
        students = self.db_manager.get_group_students(group[0])
        nb_students = len(students)
        
        def create_actions_widget(parent):
            actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
            
            edit_btn = ModernButton(
                actions_frame,
                text="Modifier",
                style="outline",
                width=32, height=26,
                command=lambda: self._open_edit_dialog(group)
            )
            edit_btn.pack(side="left", padx=2)
            
            delete_btn = ModernButton(
                actions_frame,
                text="Supprimer",
                style="danger",
                width=32, height=26,
                command=lambda: self._delete_group(group[0])
            )
            delete_btn.pack(side="left", padx=2)
            
            return actions_frame
        
        data = [
            {"text": group[1], "font_size": 11},  # Nom
            {"text": group[2] or "-", "font_size": 11},  # Matière
            {"text": group[3] or "-", "font_size": 11},  # Niveau
            {"text": f"{nb_students} élève(s)", "font_size": 11},  # Élèves
            create_actions_widget  # Actions
        ]
        
        self.table.add_row(data)
    
    def _open_add_dialog(self):
        GroupForm(self, self.db_manager, callback=self._load_groups)
    
    def _open_edit_dialog(self, group):
        GroupForm(
            self,
            self.db_manager,
            group_data=group,
            callback=self._load_groups
        )
    
    def _delete_group(self, group_id):
        if messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment supprimer ce groupe ?\nToutes les inscriptions seront supprimées."
        ):
            self.db_manager.delete_group(group_id)
            self._load_groups()
            messagebox.showinfo("✅ Succès", "Groupe supprimé avec succès.")
    
    def _perform_search(self, query):
        if query:
            results = self.db_manager.search_groups(query)
            self._load_groups(results)
        else:
            self._load_groups()
