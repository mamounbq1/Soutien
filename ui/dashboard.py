import customtkinter as ctk
from datetime import datetime

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master, corner_radius=10, fg_color="transparent")
        self.db_manager = db_manager
        
        # Grid configuration
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Title
        self.title = ctk.CTkLabel(self, text="Tableau de Bord", font=ctk.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, columnspan=4, padx=20, pady=20, sticky="w")
        
        # Statistics Cards - Row 1
        self.create_stat_card("Total Élèves", self.get_student_count(), 1, 0, "#3B8ED0")
        self.create_stat_card("Total Profs", self.get_teacher_count(), 1, 1, "#E19600")
        self.create_stat_card("Total Groupes", self.get_group_count(), 1, 2, "#8E44AD")
        self.create_stat_card("Total Matières", self.get_subject_count(), 1, 3, "#16A085")
        
        # Statistics Cards - Row 2
        revenue = self.get_monthly_revenue()
        self.create_stat_card("Revenus ce mois", f"{revenue} MAD", 2, 0, "#2CC985")
        self.create_stat_card("Total Paiements", self.get_payment_count(), 2, 1, "#27AE60")
        
        # Recent Payments Section
        self.activity_frame = ctk.CTkFrame(self)
        self.activity_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")
        self.activity_frame.grid_columnconfigure(0, weight=1)
        
        activity_title = ctk.CTkLabel(self.activity_frame, text="Paiements Récents", 
                                      font=("Arial", 18, "bold"))
        activity_title.grid(row=0, column=0, padx=20, pady=(20,10), sticky="w")
        
        # Recent payments list
        self.payments_scroll = ctk.CTkScrollableFrame(self.activity_frame, height=200)
        self.payments_scroll.grid(row=1, column=0, padx=20, pady=(0,20), sticky="nsew")
        self.payments_scroll.grid_columnconfigure((0,1,2,3), weight=1)
        
        self.load_recent_payments()

    def create_stat_card(self, title, value, row, col, color):
        card = ctk.CTkFrame(self, fg_color=color)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(card, text=title, text_color="white", font=("Arial", 14)).pack(pady=(10,0))
        ctk.CTkLabel(card, text=str(value), text_color="white", font=("Arial", 20, "bold")).pack(pady=(0,10))

    def get_student_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0

    def get_teacher_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM teachers")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_group_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM groups")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_subject_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM subjects")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_monthly_revenue(self):
        try:
            mois_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                       "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
            current_month = mois_fr[datetime.now().month - 1]
            current_year = str(datetime.now().year)
            revenue = self.db_manager.get_monthly_revenue(current_month, current_year)
            return revenue
        except:
            return 0
    
    def get_payment_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM paiements")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def load_recent_payments(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.nom || ' ' || s.prenom as student, p.montant, p.mois, p.date_paiement
                FROM paiements p
                JOIN students s ON p.student_id = s.id
                ORDER BY p.date_paiement DESC
                LIMIT 10
            ''')
            payments = cursor.fetchall()
            conn.close()
            
            if not payments:
                ctk.CTkLabel(self.payments_scroll, text="Aucun paiement enregistré", 
                            text_color="gray").grid(row=0, column=0, columnspan=4, pady=20)
                return
            
            # Header
            headers = ["Élève", "Montant", "Mois", "Date"]
            for i, h in enumerate(headers):
                ctk.CTkLabel(self.payments_scroll, text=h, font=("Arial", 11, "bold")).grid(
                    row=0, column=i, padx=10, pady=5, sticky="w")
            
            # Payments rows
            for idx, payment in enumerate(payments, start=1):
                ctk.CTkLabel(self.payments_scroll, text=payment[0]).grid(row=idx, column=0, padx=10, pady=2, sticky="w")
                ctk.CTkLabel(self.payments_scroll, text=f"{payment[1]} MAD").grid(row=idx, column=1, padx=10, pady=2, sticky="w")
                ctk.CTkLabel(self.payments_scroll, text=payment[2]).grid(row=idx, column=2, padx=10, pady=2, sticky="w")
                ctk.CTkLabel(self.payments_scroll, text=payment[3][:10]).grid(row=idx, column=3, padx=10, pady=2, sticky="w")
        except Exception as e:
            ctk.CTkLabel(self.payments_scroll, text=f"Erreur: {str(e)}", 
                        text_color="red").grid(row=0, column=0, columnspan=4, pady=20)
