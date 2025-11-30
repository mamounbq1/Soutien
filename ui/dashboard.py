import customtkinter as ctk

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master, corner_radius=10, fg_color="transparent")
        self.db_manager = db_manager
        
        # Grid configuration
        self.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Title
        self.title = ctk.CTkLabel(self, text="Tableau de Bord", font=ctk.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="w")
        
        # Statistics Cards
        self.create_stat_card("Total Élèves", self.get_student_count(), 1, 0, "#3B8ED0")
        self.create_stat_card("Total Profs", self.get_teacher_count(), 1, 1, "#E19600")
        self.create_stat_card("Revenus Mois", "0 MAD", 1, 2, "#2CC985")
        
        # Recent Activity Placeholder
        self.activity_frame = ctk.CTkFrame(self)
        self.activity_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        ctk.CTkLabel(self.activity_frame, text="Activités Récentes (Placeholder)", font=("Arial", 16)).pack(pady=20)

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
