import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master, width=200, corner_radius=0)
        self.callback = callback
        
        self.logo_label = ctk.CTkLabel(self, text="Centre Soutien", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.menu_buttons = []
        self.create_menu_button("Dashboard", "dashboard", 1)
        self.create_menu_button("Élèves", "students", 2)
        self.create_menu_button("Enseignants", "teachers", 3)
        self.create_menu_button("Matières", "subjects", 4)
        self.create_menu_button("Groupes", "groups", 5)
        self.create_menu_button("Paiements", "payments", 6)
        self.create_menu_button("Présence", "presence", 7)
        
        self.logout_btn = ctk.CTkButton(self, text="Déconnexion", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: print("Logout clicked"))
        self.logout_btn.grid(row=9, column=0, padx=20, pady=20, sticky="s")
        self.grid_rowconfigure(8, weight=1) # Spacer

    def create_menu_button(self, text, name, row):
        btn = ctk.CTkButton(self, text=text, fg_color="transparent", anchor="w",
                            command=lambda n=name: self.callback(n))
        btn.grid(row=row, column=0, sticky="ew", padx=20, pady=10)
        self.menu_buttons.append(btn)
