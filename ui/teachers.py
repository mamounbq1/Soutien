import customtkinter as ctk
from tkinter import messagebox

class TeacherForm(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, teacher_data=None, callback=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.teacher_data = teacher_data
        self.callback = callback
        self.title("Ajouter un Enseignant" if not teacher_data else "Modifier l'Enseignant")
        self.geometry("500x500")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self.layout_widgets()
        if teacher_data:
            self.fill_fields()

    def layout_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Title
        lbl_title = ctk.CTkLabel(self, text="Informations de l'enseignant", font=("Arial", 20, "bold"))
        lbl_title.grid(row=0, column=0, columnspan=2, pady=20)

        # Fields
        self.nom = self.create_entry("Nom:", 1)
        self.prenom = self.create_entry("Prénom:", 2)
        self.matiere = self.create_entry("Matière:", 3)
        self.tel = self.create_entry("Téléphone:", 4)
        self.salaire_horaire = self.create_entry("Salaire Horaire (MAD):", 5)

        # Save Button
        btn_save = ctk.CTkButton(self, text="Enregistrer", command=self.save_teacher)
        btn_save.grid(row=6, column=0, columnspan=2, pady=30, padx=20, sticky="ew")

    def create_entry(self, label_text, row):
        ctk.CTkLabel(self, text=label_text).grid(row=row, column=0, padx=20, pady=10, sticky="w")
        entry = ctk.CTkEntry(self)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="ew")
        return entry

    def fill_fields(self):
        # teacher_data structure: (id, nom, prenom, matiere, tel, salaire_horaire)
        self.nom.insert(0, self.teacher_data[1])
        self.prenom.insert(0, self.teacher_data[2])
        self.matiere.insert(0, self.teacher_data[3] or "")
        self.tel.insert(0, self.teacher_data[4] or "")
        self.salaire_horaire.insert(0, str(self.teacher_data[5]) if self.teacher_data[5] else "")

    def save_teacher(self):
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
            messagebox.showinfo("Succès", "Enseignant modifié avec succès.")
        else:
            self.db_manager.add_teacher(**data)
            messagebox.showinfo("Succès", "Enseignant ajouté avec succès.")
        
        if self.callback:
            self.callback()
        self.destroy()


class TeachersPage(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        self.db_manager = db_manager
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        title = ctk.CTkLabel(self.header_frame, text="Gestion des Enseignants", font=("Arial", 24, "bold"))
        title.pack(side="left")

        self.btn_add = ctk.CTkButton(self.header_frame, text="+ Nouvel Enseignant", command=self.open_add_dialog)
        self.btn_add.pack(side="right")

        # --- Search Bar ---
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Rechercher un enseignant...", width=300)
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.btn_search = ctk.CTkButton(self.search_frame, text="Rechercher", width=100, command=self.perform_search)
        self.btn_search.pack(side="left")
        
        self.btn_reload = ctk.CTkButton(self.search_frame, text="↻", width=40, command=self.load_teachers)
        self.btn_reload.pack(side="left", padx=10)

        # --- Table Header ---
        self.table_header = ctk.CTkFrame(self, height=40)
        self.table_header.grid(row=2, column=0, sticky="new", padx=20, pady=(10,0))
        self.table_header.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.table_header.grid_columnconfigure(5, weight=0, minsize=150)
        
        headers = ["Nom", "Prénom", "Matière", "Téléphone", "Salaire/h", "Actions"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.table_header, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scroll_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.scroll_frame.grid_columnconfigure(5, weight=0, minsize=150)

        self.load_teachers()

    def load_teachers(self, teachers=None):
        # Clear existing rows
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if teachers is None:
            teachers = self.db_manager.get_all_teachers()

        for i, teacher in enumerate(teachers):
            self.create_row(i, teacher)

    def create_row(self, index, teacher):
        # teacher: (id, nom, prenom, matiere, tel, salaire_horaire)
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row_frame.grid(row=index, column=0, columnspan=6, sticky="ew", pady=2)
        row_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        row_frame.grid_columnconfigure(5, weight=0, minsize=150)

        ctk.CTkLabel(row_frame, text=teacher[1]).grid(row=0, column=0)
        ctk.CTkLabel(row_frame, text=teacher[2]).grid(row=0, column=1)
        ctk.CTkLabel(row_frame, text=teacher[3] or "-").grid(row=0, column=2)
        ctk.CTkLabel(row_frame, text=teacher[4] or "-").grid(row=0, column=3)
        ctk.CTkLabel(row_frame, text=f"{teacher[5]} MAD" if teacher[5] else "-").grid(row=0, column=4)

        # Actions
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=5)
        
        btn_edit = ctk.CTkButton(actions_frame, text="✎", width=30, height=30, 
                                 fg_color="#F39C12", hover_color="#D35400",
                                 command=lambda t=teacher: self.open_edit_dialog(t))
        btn_edit.pack(side="left", padx=2)
        
        btn_del = ctk.CTkButton(actions_frame, text="🗑", width=30, height=30, 
                                fg_color="#E74C3C", hover_color="#C0392B",
                                command=lambda id=teacher[0]: self.delete_teacher(id))
        btn_del.pack(side="left", padx=2)

    def open_add_dialog(self):
        TeacherForm(self, self.db_manager, callback=self.load_teachers)

    def open_edit_dialog(self, teacher):
        TeacherForm(self, self.db_manager, teacher_data=teacher, callback=self.load_teachers)

    def delete_teacher(self, teacher_id):
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet enseignant ?"):
            self.db_manager.delete_teacher(teacher_id)
            self.load_teachers()

    def perform_search(self):
        query = self.search_entry.get()
        if query:
            results = self.db_manager.search_teachers(query)
            self.load_teachers(results)
        else:
            self.load_teachers()
