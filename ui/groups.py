import customtkinter as ctk
from tkinter import messagebox

class GroupForm(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, group_data=None, callback=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.group_data = group_data
        self.callback = callback
        self.title("Ajouter un Groupe" if not group_data else "Modifier le Groupe")
        self.geometry("500x500")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Load data for dropdowns
        self.subjects_list = self.db_manager.get_all_subjects()
        self.teachers_list = self.db_manager.get_all_teachers()
        
        self.layout_widgets()
        if group_data:
            self.fill_fields()

    def layout_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Title
        lbl_title = ctk.CTkLabel(self, text="Informations du groupe", font=("Arial", 20, "bold"))
        lbl_title.grid(row=0, column=0, columnspan=2, pady=20)

        # Fields
        self.nom = self.create_entry("Nom du Groupe:", 1)
        
        # Matière (Dropdown)
        ctk.CTkLabel(self, text="Matière:").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        subject_names = [f"{s[0]} - {s[1]}" for s in self.subjects_list]
        self.matiere_combo = ctk.CTkComboBox(self, values=subject_names if subject_names else ["Aucune matière"])
        self.matiere_combo.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        
        # Professeur (Dropdown)
        ctk.CTkLabel(self, text="Professeur:").grid(row=3, column=0, padx=20, pady=10, sticky="w")
        teacher_names = [f"{t[0]} - {t[1]} {t[2]}" for t in self.teachers_list]
        self.prof_combo = ctk.CTkComboBox(self, values=teacher_names if teacher_names else ["Aucun enseignant"])
        self.prof_combo.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        
        self.salle = self.create_entry("Salle:", 4)

        # Save Button
        btn_save = ctk.CTkButton(self, text="Enregistrer", command=self.save_group)
        btn_save.grid(row=5, column=0, columnspan=2, pady=30, padx=20, sticky="ew")

    def create_entry(self, label_text, row):
        ctk.CTkLabel(self, text=label_text).grid(row=row, column=0, padx=20, pady=10, sticky="w")
        entry = ctk.CTkEntry(self)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="ew")
        return entry

    def fill_fields(self):
        # group_data for editing: (id, nom, matiere_id, prof_id, salle)
        if self.group_data:
            details = self.db_manager.get_group_details(self.group_data[0])
            if details:
                self.nom.insert(0, details[1])
                
                # Set matiere
                if details[2]:
                    for idx, s in enumerate(self.subjects_list):
                        if s[0] == details[2]:
                            self.matiere_combo.set(f"{s[0]} - {s[1]}")
                            break
                
                # Set prof
                if details[3]:
                    for idx, t in enumerate(self.teachers_list):
                        if t[0] == details[3]:
                            self.prof_combo.set(f"{t[0]} - {t[1]} {t[2]}")
                            break
                
                self.salle.insert(0, details[4] or "")

    def save_group(self):
        nom = self.nom.get()
        salle = self.salle.get()
        
        if not nom:
            messagebox.showerror("Erreur", "Le nom du groupe est obligatoire.")
            return
        
        # Extract IDs from combobox selections
        matiere_id = None
        prof_id = None
        
        matiere_selection = self.matiere_combo.get()
        if matiere_selection and matiere_selection != "Aucune matière":
            try:
                matiere_id = int(matiere_selection.split(" - ")[0])
            except:
                pass
        
        prof_selection = self.prof_combo.get()
        if prof_selection and prof_selection != "Aucun enseignant":
            try:
                prof_id = int(prof_selection.split(" - ")[0])
            except:
                pass

        if self.group_data:
            self.db_manager.update_group(self.group_data[0], nom, matiere_id, prof_id, salle)
            messagebox.showinfo("Succès", "Groupe modifié avec succès.")
        else:
            self.db_manager.add_group(nom, matiere_id, prof_id, salle)
            messagebox.showinfo("Succès", "Groupe ajouté avec succès.")
        
        if self.callback:
            self.callback()
        self.destroy()


class GroupsPage(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        self.db_manager = db_manager
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        title = ctk.CTkLabel(self.header_frame, text="Gestion des Groupes", font=("Arial", 24, "bold"))
        title.pack(side="left")

        self.btn_add = ctk.CTkButton(self.header_frame, text="+ Nouveau Groupe", command=self.open_add_dialog)
        self.btn_add.pack(side="right")

        # --- Search Bar ---
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Rechercher un groupe...", width=300)
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.btn_search = ctk.CTkButton(self.search_frame, text="Rechercher", width=100, command=self.perform_search)
        self.btn_search.pack(side="left")
        
        self.btn_reload = ctk.CTkButton(self.search_frame, text="↻", width=40, command=self.load_groups)
        self.btn_reload.pack(side="left", padx=10)

        # --- Table Header ---
        self.table_header = ctk.CTkFrame(self, height=40)
        self.table_header.grid(row=2, column=0, sticky="new", padx=20, pady=(10,0))
        self.table_header.grid_columnconfigure((0,1,2,3), weight=1)
        self.table_header.grid_columnconfigure(4, weight=0, minsize=150)
        
        headers = ["Nom du Groupe", "Matière", "Professeur", "Salle", "Actions"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.table_header, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scroll_frame.grid_columnconfigure((0,1,2,3), weight=1)
        self.scroll_frame.grid_columnconfigure(4, weight=0, minsize=150)

        self.load_groups()

    def load_groups(self, groups=None):
        # Clear existing rows
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if groups is None:
            groups = self.db_manager.get_all_groups()

        for i, group in enumerate(groups):
            self.create_row(i, group)

    def create_row(self, index, group):
        # group: (id, nom, matiere, prof, salle)
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row_frame.grid(row=index, column=0, columnspan=5, sticky="ew", pady=2)
        row_frame.grid_columnconfigure((0,1,2,3), weight=1)
        row_frame.grid_columnconfigure(4, weight=0, minsize=150)

        ctk.CTkLabel(row_frame, text=group[1]).grid(row=0, column=0)
        ctk.CTkLabel(row_frame, text=group[2] or "-").grid(row=0, column=1)
        ctk.CTkLabel(row_frame, text=group[3] or "-").grid(row=0, column=2)
        ctk.CTkLabel(row_frame, text=group[4] or "-").grid(row=0, column=3)

        # Actions
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=4)
        
        btn_edit = ctk.CTkButton(actions_frame, text="✎", width=30, height=30, 
                                 fg_color="#F39C12", hover_color="#D35400",
                                 command=lambda g=group: self.open_edit_dialog(g))
        btn_edit.pack(side="left", padx=2)
        
        btn_del = ctk.CTkButton(actions_frame, text="🗑", width=30, height=30, 
                                fg_color="#E74C3C", hover_color="#C0392B",
                                command=lambda id=group[0]: self.delete_group(id))
        btn_del.pack(side="left", padx=2)

    def open_add_dialog(self):
        GroupForm(self, self.db_manager, callback=self.load_groups)

    def open_edit_dialog(self, group):
        GroupForm(self, self.db_manager, group_data=group, callback=self.load_groups)

    def delete_group(self, group_id):
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce groupe ?"):
            self.db_manager.delete_group(group_id)
            self.load_groups()

    def perform_search(self):
        query = self.search_entry.get()
        if query:
            results = self.db_manager.search_groups(query)
            self.load_groups(results)
        else:
            self.load_groups()
