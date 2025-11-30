import customtkinter as ctk
from tkinter import messagebox

class StudentForm(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, student_data=None, callback=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.student_data = student_data
        self.callback = callback
        self.title("Ajouter un Élève" if not student_data else "Modifier l'Élève")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self.layout_widgets()
        if student_data:
            self.fill_fields()

    def layout_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Title
        lbl_title = ctk.CTkLabel(self, text="Informations de l'élève", font=("Arial", 20, "bold"))
        lbl_title.grid(row=0, column=0, columnspan=2, pady=20)

        # Fields
        self.nom = self.create_entry("Nom:", 1)
        self.prenom = self.create_entry("Prénom:", 2)
        
        # Niveau (Combobox)
        ctk.CTkLabel(self, text="Niveau:").grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.niveau = ctk.CTkComboBox(self, values=["Primaire", "Collège", "Lycée", "Supérieur"])
        self.niveau.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        
        self.filiere = self.create_entry("Filière/Classe:", 4)
        self.tel = self.create_entry("Téléphone:", 5)
        self.parent_tel = self.create_entry("Tél. Parents:", 6)

        # Save Button
        btn_save = ctk.CTkButton(self, text="Enregistrer", command=self.save_student)
        btn_save.grid(row=7, column=0, columnspan=2, pady=30, padx=20, sticky="ew")

    def create_entry(self, label_text, row):
        ctk.CTkLabel(self, text=label_text).grid(row=row, column=0, padx=20, pady=10, sticky="w")
        entry = ctk.CTkEntry(self)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="ew")
        return entry

    def fill_fields(self):
        # student_data structure from DB: (id, nom, prenom, niveau, filiere, tel, parent_tel, date)
        self.nom.insert(0, self.student_data[1])
        self.prenom.insert(0, self.student_data[2])
        self.niveau.set(self.student_data[3])
        self.filiere.insert(0, self.student_data[4])
        self.tel.insert(0, self.student_data[5])
        self.parent_tel.insert(0, self.student_data[6])

    def save_student(self):
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
            messagebox.showinfo("Succès", "Élève modifié avec succès.")
        else:
            self.db_manager.add_student(**data)
            messagebox.showinfo("Succès", "Élève ajouté avec succès.")
        
        if self.callback:
            self.callback()
        self.destroy()


class StudentsPage(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        self.db_manager = db_manager
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Content area expands

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        title = ctk.CTkLabel(self.header_frame, text="Gestion des Élèves", font=("Arial", 24, "bold"))
        title.pack(side="left")

        self.btn_add = ctk.CTkButton(self.header_frame, text="+ Nouvel Élève", command=self.open_add_dialog)
        self.btn_add.pack(side="right")

        # --- Search Bar ---
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Rechercher un élève...", width=300)
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.btn_search = ctk.CTkButton(self.search_frame, text="Rechercher", width=100, command=self.perform_search)
        self.btn_search.pack(side="left")
        
        self.btn_reload = ctk.CTkButton(self.search_frame, text="↻", width=40, command=self.load_students)
        self.btn_reload.pack(side="left", padx=10)

        # --- List Area (Table) ---
        # Using ScrollableFrame to simulate a table rows
        self.table_header = ctk.CTkFrame(self, height=40)
        self.table_header.grid(row=2, column=0, sticky="new", padx=20, pady=(10,0))
        self.table_header.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.table_header.grid_columnconfigure(5, weight=0, minsize=150) # Actions column
        
        headers = ["Nom", "Prénom", "Niveau", "Filière", "Téléphone", "Actions"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.table_header, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scroll_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.scroll_frame.grid_columnconfigure(5, weight=0, minsize=150)

        self.load_students()

    def load_students(self, students=None):
        # Clear existing rows
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if students is None:
            students = self.db_manager.get_all_students()

        for i, student in enumerate(students):
            self.create_row(i, student)

    def create_row(self, index, student):
        # student: (id, nom, prenom, niveau, filiere, tel, parent_tel, date)
        bg_color = "transparent" if index % 2 == 0 else ("#EBEBEB", "#2B2B2B") # Alternating colors light/dark theme
        
        # We can't easily set bg color for the row in grid layout without a container frame per row, 
        # but adding frames is expensive for many rows. 
        # Simple Label grid is better for performance, but styling is harder.
        # Let's use a Frame for each row to handle actions and alignment better.
        
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent") # Let ScrollFrame handle bg
        row_frame.grid(row=index, column=0, columnspan=6, sticky="ew", pady=2)
        row_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        row_frame.grid_columnconfigure(5, weight=0, minsize=150)

        ctk.CTkLabel(row_frame, text=student[1]).grid(row=0, column=0)
        ctk.CTkLabel(row_frame, text=student[2]).grid(row=0, column=1)
        ctk.CTkLabel(row_frame, text=student[3]).grid(row=0, column=2)
        ctk.CTkLabel(row_frame, text=student[4]).grid(row=0, column=3)
        ctk.CTkLabel(row_frame, text=student[5]).grid(row=0, column=4)

        # Actions
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=5)
        
        btn_edit = ctk.CTkButton(actions_frame, text="✎", width=30, height=30, 
                                 fg_color="#F39C12", hover_color="#D35400",
                                 command=lambda s=student: self.open_edit_dialog(s))
        btn_edit.pack(side="left", padx=2)
        
        btn_del = ctk.CTkButton(actions_frame, text="🗑", width=30, height=30, 
                                fg_color="#E74C3C", hover_color="#C0392B",
                                command=lambda id=student[0]: self.delete_student(id))
        btn_del.pack(side="left", padx=2)

    def open_add_dialog(self):
        StudentForm(self, self.db_manager, callback=self.load_students)

    def open_edit_dialog(self, student):
        StudentForm(self, self.db_manager, student_data=student, callback=self.load_students)

    def delete_student(self, student_id):
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet élève ?"):
            self.db_manager.delete_student(student_id)
            self.load_students()

    def perform_search(self):
        query = self.search_entry.get()
        if query:
            results = self.db_manager.search_students(query)
            self.load_students(results)
        else:
            self.load_students()
