import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class PaymentForm(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, callback=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.callback = callback
        self.title("Ajouter un Paiement")
        self.geometry("500x500")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Load students for dropdown
        self.students_list = self.db_manager.get_all_students()
        
        self.layout_widgets()

    def layout_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Title
        lbl_title = ctk.CTkLabel(self, text="Enregistrer un paiement", font=("Arial", 20, "bold"))
        lbl_title.grid(row=0, column=0, columnspan=2, pady=20)

        # Élève (Dropdown)
        ctk.CTkLabel(self, text="Élève:").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        student_names = [f"{s[0]} - {s[1]} {s[2]}" for s in self.students_list]
        self.student_combo = ctk.CTkComboBox(self, values=student_names if student_names else ["Aucun élève"])
        self.student_combo.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        
        # Montant
        self.montant = self.create_entry("Montant (MAD):", 2)
        
        # Mois
        ctk.CTkLabel(self, text="Mois:").grid(row=3, column=0, padx=20, pady=10, sticky="w")
        mois_list = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                     "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        self.mois_combo = ctk.CTkComboBox(self, values=mois_list)
        self.mois_combo.set(mois_list[datetime.now().month - 1])  # Current month
        self.mois_combo.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        
        # Année
        ctk.CTkLabel(self, text="Année:").grid(row=4, column=0, padx=20, pady=10, sticky="w")
        current_year = datetime.now().year
        annee_list = [str(y) for y in range(current_year - 2, current_year + 2)]
        self.annee_combo = ctk.CTkComboBox(self, values=annee_list)
        self.annee_combo.set(str(current_year))
        self.annee_combo.grid(row=4, column=1, padx=20, pady=10, sticky="ew")

        # Save Button
        btn_save = ctk.CTkButton(self, text="Enregistrer", command=self.save_payment)
        btn_save.grid(row=5, column=0, columnspan=2, pady=30, padx=20, sticky="ew")

    def create_entry(self, label_text, row):
        ctk.CTkLabel(self, text=label_text).grid(row=row, column=0, padx=20, pady=10, sticky="w")
        entry = ctk.CTkEntry(self)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="ew")
        return entry

    def save_payment(self):
        montant = self.montant.get()
        mois = self.mois_combo.get()
        annee = self.annee_combo.get()
        
        if not montant:
            messagebox.showerror("Erreur", "Le montant est obligatoire.")
            return
        
        # Validate montant
        try:
            montant = float(montant)
        except ValueError:
            messagebox.showerror("Erreur", "Le montant doit être un nombre.")
            return
        
        # Extract student ID
        student_selection = self.student_combo.get()
        if not student_selection or student_selection == "Aucun élève":
            messagebox.showerror("Erreur", "Veuillez sélectionner un élève.")
            return
        
        try:
            student_id = int(student_selection.split(" - ")[0])
        except:
            messagebox.showerror("Erreur", "Élève invalide.")
            return

        self.db_manager.add_payment(student_id, montant, mois, annee)
        messagebox.showinfo("Succès", "Paiement enregistré avec succès.")
        
        if self.callback:
            self.callback()
        self.destroy()


class PaymentsPage(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        self.db_manager = db_manager
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        title = ctk.CTkLabel(self.header_frame, text="Paiements & Comptabilité", font=("Arial", 24, "bold"))
        title.pack(side="left")

        self.btn_add = ctk.CTkButton(self.header_frame, text="+ Nouveau Paiement", command=self.open_add_dialog)
        self.btn_add.pack(side="right")

        # --- Stats ---
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.stats_frame.grid_columnconfigure((0,1), weight=1)
        
        current_month = datetime.now().strftime("%B")
        current_year = str(datetime.now().year)
        
        # Get current month revenue
        mois_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                   "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        current_month_fr = mois_fr[datetime.now().month - 1]
        revenue = self.db_manager.get_monthly_revenue(current_month_fr, current_year)
        
        stat1 = ctk.CTkFrame(self.stats_frame, fg_color="#2CC985")
        stat1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(stat1, text=f"Revenus {current_month_fr} {current_year}", text_color="white", font=("Arial", 14)).pack(pady=(10,0))
        ctk.CTkLabel(stat1, text=f"{revenue} MAD", text_color="white", font=("Arial", 20, "bold")).pack(pady=(0,10))
        
        # Total payments count
        all_payments = self.db_manager.get_all_payments()
        stat2 = ctk.CTkFrame(self.stats_frame, fg_color="#3B8ED0")
        stat2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(stat2, text="Total Paiements", text_color="white", font=("Arial", 14)).pack(pady=(10,0))
        ctk.CTkLabel(stat2, text=str(len(all_payments)), text_color="white", font=("Arial", 20, "bold")).pack(pady=(0,10))

        # --- Search Bar ---
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Rechercher un paiement...", width=300)
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.btn_search = ctk.CTkButton(self.search_frame, text="Rechercher", width=100, command=self.perform_search)
        self.btn_search.pack(side="left")
        
        self.btn_reload = ctk.CTkButton(self.search_frame, text="↻", width=40, command=self.load_payments)
        self.btn_reload.pack(side="left", padx=10)

        # --- Table Header ---
        self.table_header = ctk.CTkFrame(self, height=40)
        self.table_header.grid(row=3, column=0, sticky="new", padx=20, pady=(10,0))
        self.table_header.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.table_header.grid_columnconfigure(5, weight=0, minsize=100)
        
        headers = ["Élève", "Montant", "Mois", "Année", "Date Paiement", "Actions"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.table_header, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scroll_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.scroll_frame.grid_columnconfigure(5, weight=0, minsize=100)

        self.load_payments()

    def load_payments(self, payments=None):
        # Clear existing rows
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if payments is None:
            payments = self.db_manager.get_all_payments()

        for i, payment in enumerate(payments):
            self.create_row(i, payment)

    def create_row(self, index, payment):
        # payment: (id, student_name, montant, mois, annee, date_paiement)
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row_frame.grid(row=index, column=0, columnspan=6, sticky="ew", pady=2)
        row_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        row_frame.grid_columnconfigure(5, weight=0, minsize=100)

        ctk.CTkLabel(row_frame, text=payment[1]).grid(row=0, column=0)
        ctk.CTkLabel(row_frame, text=f"{payment[2]} MAD").grid(row=0, column=1)
        ctk.CTkLabel(row_frame, text=payment[3]).grid(row=0, column=2)
        ctk.CTkLabel(row_frame, text=payment[4]).grid(row=0, column=3)
        ctk.CTkLabel(row_frame, text=payment[5][:10]).grid(row=0, column=4)

        # Actions
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=5)
        
        btn_del = ctk.CTkButton(actions_frame, text="🗑", width=30, height=30, 
                                fg_color="#E74C3C", hover_color="#C0392B",
                                command=lambda id=payment[0]: self.delete_payment(id))
        btn_del.pack(side="left", padx=2)

    def open_add_dialog(self):
        PaymentForm(self, self.db_manager, callback=self.load_payments)

    def delete_payment(self, payment_id):
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce paiement ?"):
            self.db_manager.delete_payment(payment_id)
            self.load_payments()

    def perform_search(self):
        query = self.search_entry.get()
        if query:
            results = self.db_manager.search_payments(query)
            self.load_payments(results)
        else:
            self.load_payments()
