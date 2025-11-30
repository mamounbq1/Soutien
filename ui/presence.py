import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class PresencePage(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        self.db_manager = db_manager
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.selected_group_id = None
        self.selected_date = datetime.now().strftime("%Y-%m-%d")
        
        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        title = ctk.CTkLabel(self.header_frame, text="Feuille de Présence", font=("Arial", 24, "bold"))
        title.pack(side="left")

        # --- Selection Panel ---
        self.selection_frame = ctk.CTkFrame(self)
        self.selection_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.selection_frame.grid_columnconfigure((0,1,2), weight=1)
        
        # Group Selection
        ctk.CTkLabel(self.selection_frame, text="Groupe:", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        groups = self.db_manager.get_all_groups()
        group_names = [f"{g[0]} - {g[1]}" for g in groups]
        self.group_combo = ctk.CTkComboBox(self.selection_frame, values=group_names if group_names else ["Aucun groupe"], 
                                           command=self.on_group_select, width=250)
        self.group_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Date Selection
        ctk.CTkLabel(self.selection_frame, text="Date:", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.date_entry = ctk.CTkEntry(self.selection_frame, placeholder_text="YYYY-MM-DD")
        self.date_entry.insert(0, self.selected_date)
        self.date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Load Button
        self.btn_load = ctk.CTkButton(self.selection_frame, text="Charger la Présence", command=self.load_presence)
        self.btn_load.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        # --- Presence Table ---
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(1, weight=1)
        
        # Table Header
        self.table_header = ctk.CTkFrame(self.table_frame, height=40)
        self.table_header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,0))
        self.table_header.grid_columnconfigure((0,1,2), weight=1)
        
        headers = ["Nom", "Prénom", "Statut"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.table_header, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)
        
        # Scrollable content
        self.scroll_frame = ctk.CTkScrollableFrame(self.table_frame)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        self.scroll_frame.grid_columnconfigure((0,1,2), weight=1)
        
        # Info label
        self.info_label = ctk.CTkLabel(self.scroll_frame, text="Sélectionnez un groupe et une date pour charger la présence.", 
                                       font=("Arial", 14), text_color="gray")
        self.info_label.grid(row=0, column=0, columnspan=3, pady=50)
        
        # Save Button
        self.btn_save = ctk.CTkButton(self.table_frame, text="Enregistrer la Présence", 
                                      command=self.save_presence, state="disabled")
        self.btn_save.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

    def on_group_select(self, choice):
        if choice and choice != "Aucun groupe":
            try:
                self.selected_group_id = int(choice.split(" - ")[0])
            except:
                self.selected_group_id = None

    def load_presence(self):
        if not self.selected_group_id:
            messagebox.showerror("Erreur", "Veuillez sélectionner un groupe.")
            return
        
        self.selected_date = self.date_entry.get()
        
        # Validate date format
        try:
            datetime.strptime(self.selected_date, "%Y-%m-%d")
        except:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez YYYY-MM-DD.")
            return
        
        # Clear previous content
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Get students in this group
        students = self.db_manager.get_group_students(self.selected_group_id)
        
        if not students:
            ctk.CTkLabel(self.scroll_frame, text="Aucun élève dans ce groupe.", 
                        font=("Arial", 14), text_color="gray").grid(row=0, column=0, columnspan=3, pady=50)
            self.btn_save.configure(state="disabled")
            return
        
        # Check if presence already exists for this date
        existing_presence = self.db_manager.get_presence_by_group_date(self.selected_group_id, self.selected_date)
        presence_dict = {p[1]: p[4] for p in existing_presence}  # student_id: status
        
        # Create rows
        self.presence_widgets = []
        for i, student in enumerate(students):
            # student: (id, nom, prenom, tel, date_inscription)
            student_id = student[0]
            
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            row_frame.grid(row=i, column=0, columnspan=3, sticky="ew", pady=5)
            row_frame.grid_columnconfigure((0,1,2), weight=1)
            
            ctk.CTkLabel(row_frame, text=student[1]).grid(row=0, column=0, padx=5)
            ctk.CTkLabel(row_frame, text=student[2]).grid(row=0, column=1, padx=5)
            
            # Status Radio Buttons
            status_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            status_frame.grid(row=0, column=2, padx=5)
            
            status_var = ctk.StringVar(value=presence_dict.get(student_id, "present"))
            
            rb_present = ctk.CTkRadioButton(status_frame, text="Présent", variable=status_var, value="present")
            rb_present.pack(side="left", padx=5)
            
            rb_absent = ctk.CTkRadioButton(status_frame, text="Absent", variable=status_var, value="absent")
            rb_absent.pack(side="left", padx=5)
            
            rb_late = ctk.CTkRadioButton(status_frame, text="Retard", variable=status_var, value="retard")
            rb_late.pack(side="left", padx=5)
            
            self.presence_widgets.append({
                "student_id": student_id,
                "status_var": status_var
            })
        
        self.btn_save.configure(state="normal")

    def save_presence(self):
        if not self.selected_group_id or not self.presence_widgets:
            messagebox.showerror("Erreur", "Aucune présence à enregistrer.")
            return
        
        # Save each student's presence
        for widget_data in self.presence_widgets:
            student_id = widget_data["student_id"]
            status = widget_data["status_var"].get()
            
            # Check if record exists
            existing = self.db_manager.check_presence_exists(self.selected_group_id, student_id, self.selected_date)
            
            if existing:
                # Update existing record
                self.db_manager.update_presence(existing[0], status)
            else:
                # Create new record
                self.db_manager.add_presence(self.selected_group_id, student_id, self.selected_date, status)
        
        messagebox.showinfo("Succès", "Présence enregistrée avec succès.")
        self.load_presence()  # Reload to show saved data
