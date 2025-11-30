import customtkinter as ctk
from tkinter import messagebox

class SubjectForm(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, subject_data=None, callback=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.subject_data = subject_data
        self.callback = callback
        self.title("Ajouter une Matière" if not subject_data else "Modifier la Matière")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self.layout_widgets()
        if subject_data:
            self.fill_fields()

    def layout_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Title
        lbl_title = ctk.CTkLabel(self, text="Informations de la matière", font=("Arial", 20, "bold"))
        lbl_title.grid(row=0, column=0, columnspan=2, pady=20)

        # Fields
        self.nom = self.create_entry("Nom:", 1)
        
        # Description (Text Area)
        ctk.CTkLabel(self, text="Description:").grid(row=2, column=0, padx=20, pady=10, sticky="nw")
        self.description = ctk.CTkTextbox(self, height=100)
        self.description.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        
        self.tarif_mensuel = self.create_entry("Tarif Mensuel (MAD):", 3)

        # Save Button
        btn_save = ctk.CTkButton(self, text="Enregistrer", command=self.save_subject)
        btn_save.grid(row=4, column=0, columnspan=2, pady=30, padx=20, sticky="ew")

    def create_entry(self, label_text, row):
        ctk.CTkLabel(self, text=label_text).grid(row=row, column=0, padx=20, pady=10, sticky="w")
        entry = ctk.CTkEntry(self)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="ew")
        return entry

    def fill_fields(self):
        # subject_data: (id, nom, description, tarif_mensuel)
        self.nom.insert(0, self.subject_data[1])
        self.description.insert("1.0", self.subject_data[2] or "")
        self.tarif_mensuel.insert(0, str(self.subject_data[3]) if self.subject_data[3] else "")

    def save_subject(self):
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
            messagebox.showinfo("Succès", "Matière modifiée avec succès.")
        else:
            self.db_manager.add_subject(**data)
            messagebox.showinfo("Succès", "Matière ajoutée avec succès.")
        
        if self.callback:
            self.callback()
        self.destroy()


class SubjectsPage(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        self.db_manager = db_manager
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        title = ctk.CTkLabel(self.header_frame, text="Gestion des Matières", font=("Arial", 24, "bold"))
        title.pack(side="left")

        self.btn_add = ctk.CTkButton(self.header_frame, text="+ Nouvelle Matière", command=self.open_add_dialog)
        self.btn_add.pack(side="right")

        # --- Search Bar ---
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Rechercher une matière...", width=300)
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.btn_search = ctk.CTkButton(self.search_frame, text="Rechercher", width=100, command=self.perform_search)
        self.btn_search.pack(side="left")
        
        self.btn_reload = ctk.CTkButton(self.search_frame, text="↻", width=40, command=self.load_subjects)
        self.btn_reload.pack(side="left", padx=10)

        # --- Table Header ---
        self.table_header = ctk.CTkFrame(self, height=40)
        self.table_header.grid(row=2, column=0, sticky="new", padx=20, pady=(10,0))
        self.table_header.grid_columnconfigure((0,1,2), weight=1)
        self.table_header.grid_columnconfigure(3, weight=0, minsize=150)
        
        headers = ["Nom", "Description", "Tarif Mensuel", "Actions"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.table_header, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scroll_frame.grid_columnconfigure((0,1,2), weight=1)
        self.scroll_frame.grid_columnconfigure(3, weight=0, minsize=150)

        self.load_subjects()

    def load_subjects(self, subjects=None):
        # Clear existing rows
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if subjects is None:
            subjects = self.db_manager.get_all_subjects()

        for i, subject in enumerate(subjects):
            self.create_row(i, subject)

    def create_row(self, index, subject):
        # subject: (id, nom, description, tarif_mensuel)
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row_frame.grid(row=index, column=0, columnspan=4, sticky="ew", pady=2)
        row_frame.grid_columnconfigure((0,1,2), weight=1)
        row_frame.grid_columnconfigure(3, weight=0, minsize=150)

        ctk.CTkLabel(row_frame, text=subject[1]).grid(row=0, column=0)
        desc = subject[2][:50] + "..." if subject[2] and len(subject[2]) > 50 else (subject[2] or "-")
        ctk.CTkLabel(row_frame, text=desc).grid(row=0, column=1)
        ctk.CTkLabel(row_frame, text=f"{subject[3]} MAD" if subject[3] else "-").grid(row=0, column=2)

        # Actions
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=3)
        
        btn_edit = ctk.CTkButton(actions_frame, text="✎", width=30, height=30, 
                                 fg_color="#F39C12", hover_color="#D35400",
                                 command=lambda s=subject: self.open_edit_dialog(s))
        btn_edit.pack(side="left", padx=2)
        
        btn_del = ctk.CTkButton(actions_frame, text="🗑", width=30, height=30, 
                                fg_color="#E74C3C", hover_color="#C0392B",
                                command=lambda id=subject[0]: self.delete_subject(id))
        btn_del.pack(side="left", padx=2)

    def open_add_dialog(self):
        SubjectForm(self, self.db_manager, callback=self.load_subjects)

    def open_edit_dialog(self, subject):
        SubjectForm(self, self.db_manager, subject_data=subject, callback=self.load_subjects)

    def delete_subject(self, subject_id):
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette matière ?"):
            self.db_manager.delete_subject(subject_id)
            self.load_subjects()

    def perform_search(self):
        query = self.search_entry.get()
        if query:
            results = self.db_manager.search_subjects(query)
            self.load_subjects(results)
        else:
            self.load_subjects()
