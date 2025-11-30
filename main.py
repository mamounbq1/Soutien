import customtkinter as ctk
from widgets.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.students import StudentsPage
from ui.teachers import TeachersPage
from ui.subjects import SubjectsPage
from ui.groups import GroupsPage
from ui.payments import PaymentsPage
from ui.presence import PresencePage
from database.db_manager import DatabaseManager
import os

# Configuration de base
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestion Centre de Soutien")
        self.geometry("1100x700")

        # Database Initialization
        self.db = DatabaseManager()

        # Layout Grid Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = Sidebar(self, self.change_view)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Main Content Area
        self.current_frame = None
        self.show_dashboard()

    def change_view(self, view_name):
        # Clear current frame
        if self.current_frame:
            self.current_frame.destroy()

        if view_name == "dashboard":
            self.show_dashboard()
        elif view_name == "students":
            self.show_students()
        elif view_name == "teachers":
            self.show_teachers()
        elif view_name == "subjects":
            self.show_subjects()
        elif view_name == "groups":
            self.show_groups()
        elif view_name == "payments":
            self.show_payments()
        elif view_name == "presence":
            self.show_presence()

    def show_dashboard(self):
        self.current_frame = Dashboard(self, self.db)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_students(self):
        self.current_frame = StudentsPage(self, self.db)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_teachers(self):
        self.current_frame = TeachersPage(self, self.db)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_subjects(self):
        self.current_frame = SubjectsPage(self, self.db)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_groups(self):
        self.current_frame = GroupsPage(self, self.db)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_payments(self):
        self.current_frame = PaymentsPage(self, self.db)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_presence(self):
        self.current_frame = PresencePage(self, self.db)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()
