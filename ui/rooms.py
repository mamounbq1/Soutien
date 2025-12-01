"""
Module de gestion des salles
Design moderne avec composants réutilisables
"""

import customtkinter as ctk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import ModernTheme
from widgets.modern_components import (
    ModernButton,
    ModernEntry,
    ModernLabel,
    ModernComboBox,
    ModernTextBox,
    ModernCard,
    SearchBar,
    PageHeader,
    BorderedTable,
    ActionButtons
)


class RoomForm(ctk.CTkToplevel):
    """Formulaire de salle modernisé"""
    
    def __init__(self, parent, db_manager, room_data=None, callback=None):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.room_data = room_data
        self.callback = callback
        
        self.title("🏫 Ajouter une Salle" if not room_data else "✏️ Modifier la Salle")
        self.geometry("550x600")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        self._create_ui()
        
        if room_data:
            self._fill_fields()
        
        self._center_window()
    
    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_ui(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        header = ModernLabel(
            main_container,
            text="🏫 Informations de la salle",
            style='heading'
        )
        header.pack(pady=(0, 25))
        
        form_card = ModernCard(main_container)
        form_card.pack(fill="both", expand=True)
        
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Nom
        ModernLabel(form_content, text="Nom *", style='normal').pack(anchor="w", pady=(0, 5))
        self.nom = ModernEntry(form_content, placeholder="Ex: Salle 101")
        self.nom.pack(fill="x", pady=(0, 15))
        
        # Capacité
        ModernLabel(form_content, text="Capacité (élèves) *", style='normal').pack(anchor="w", pady=(0, 5))
        self.capacite = ModernEntry(form_content, placeholder="Ex: 25")
        self.capacite.pack(fill="x", pady=(0, 15))
        
        # Équipement
        ModernLabel(form_content, text="Équipement", style='normal').pack(anchor="w", pady=(0, 5))
        self.equipement = ModernTextBox(form_content, height=100)
        self.equipement.pack(fill="x", pady=(0, 15))
        
        # Disponible
        self.disponible_var = ctk.BooleanVar(value=True)
        self.disponible_check = ctk.CTkCheckBox(
            form_content,
            text="Salle disponible",
            variable=self.disponible_var,
            fg_color=ModernTheme.SUCCESS,
            hover_color=ModernTheme.BTN_SUCCESS_HOVER
        )
        self.disponible_check.pack(anchor="w", pady=(0, 10))
        
        note_label = ModernLabel(
            form_content,
            text="* Champs obligatoires",
            style='small'
        )
        note_label.pack(anchor="w", pady=(10, 0))
        
        buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        cancel_btn = ModernButton(
            buttons_frame,
            text="Annuler",
            icon="❌",
            style='outline',
            command=self.destroy
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = ModernButton(
            buttons_frame,
            text="Enregistrer",
            icon="💾",
            style='success',
            command=self._save_room
        )
        save_btn.pack(side="right")
    
    def _fill_fields(self):
        if self.room_data:
            self.nom.insert(0, self.room_data[1])
            self.capacite.insert(0, str(self.room_data[2]))
            self.equipement.insert("1.0", self.room_data[3] or "")
            self.disponible_var.set(bool(self.room_data[4]))
    
    def _save_room(self):
        data = {
            "nom": self.nom.get(),
            "capacite": self.capacite.get(),
            "equipement": self.equipement.get("1.0", "end-1c"),
            "disponible": self.disponible_var.get()
        }
        
        if not data["nom"]:
            messagebox.showerror("Erreur", "Le nom de la salle est obligatoire.")
            return
        
        try:
            data["capacite"] = int(data["capacite"])
            if data["capacite"] <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "La capacité doit être un nombre positif.")
            return

        try:
            if self.room_data:
                self.db_manager.update_room(self.room_data[0], **data)
                messagebox.showinfo("✅ Succès", "Salle modifiée avec succès.")
            else:
                self.db_manager.add_room(**data)
                messagebox.showinfo("✅ Succès", "Salle ajoutée avec succès.")
            
            if self.callback:
                self.callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement: {str(e)}")


class RoomsPage(ctk.CTkFrame):
    """Page de gestion des salles modernisée"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.db_manager = db_manager
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self._create_ui()
        self._load_rooms()
    
    def _create_ui(self):
        header = PageHeader(
            self,
            title="🏫 Gestion des Salles",
            subtitle="Gérez les salles de cours avec capacités et équipements",
            add_button_text="Nouvelle Salle",
            add_callback=self._open_add_dialog
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        search_bar = SearchBar(
            self,
            placeholder="Rechercher une salle...",
            search_callback=self._perform_search,
            refresh_callback=self._load_rooms
        )
        search_bar.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        table_card = ModernCard(self)
        table_card.grid(row=2, column=0, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(0, weight=1)
        
        scroll_container = ctk.CTkScrollableFrame(
            table_card,
            fg_color="transparent"
        )
        scroll_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        scroll_container.grid_columnconfigure(0, weight=1)
        
        self.table = BorderedTable(
            scroll_container,
            headers=["Nom", "Capacité", "Équipement", "Statut", "Actions"],
            column_weights=[2, 1, 2, 1, 1]
        )
        self.table.grid(row=0, column=0, sticky="nsew")
    
    def _load_rooms(self, rooms=None):
        self.table.clear_rows()
        
        if rooms is None:
            rooms = self.db_manager.get_all_rooms()
        
        if not rooms:
            no_data_label = ctk.CTkLabel(
                self.table,
                text="Aucune salle enregistrée",
                font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
                text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
            )
            no_data_label.grid(row=1, column=0, columnspan=5, pady=40)
            return
        
        for room in rooms:
            self._add_room_row(room)
    
    def _add_room_row(self, room):
        room_id = room[0]
        
        def create_actions_widget(cell_frame):
            actions_container = ctk.CTkFrame(cell_frame, fg_color="transparent")
            
            edit_btn = ctk.CTkButton(
                actions_container,
                text="Modifier",
                width=70,
                height=26,
                corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
                fg_color=(ModernTheme.WARNING, ModernTheme.WARNING),
                hover_color=("#F57C00", "#F57C00"),
                font=ctk.CTkFont(size=11),
                command=lambda: self._open_edit_dialog(room)
            )
            edit_btn.pack(side="left", padx=(0, 4))
            
            delete_btn = ctk.CTkButton(
                actions_container,
                text="Supprimer",
                width=75,
                height=26,
                corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
                fg_color=(ModernTheme.DANGER, ModernTheme.DANGER),
                hover_color=(ModernTheme.BTN_DANGER_HOVER, ModernTheme.BTN_DANGER_HOVER),
                font=ctk.CTkFont(size=11),
                command=lambda: self._delete_room(room_id)
            )
            delete_btn.pack(side="left")
            
            return actions_container
        
        equip = room[3][:40] + "..." if room[3] and len(room[3]) > 40 else (room[3] or "-")
        status = "✅ Disponible" if room[4] else "⚠️ Maintenance"
        
        self.table.add_row([
            room[1],
            f"{room[2]} élèves",
            equip,
            status,
            create_actions_widget
        ])
    
    def _open_add_dialog(self):
        RoomForm(self, self.db_manager, callback=self._load_rooms)
    
    def _open_edit_dialog(self, room):
        RoomForm(
            self,
            self.db_manager,
            room_data=room,
            callback=self._load_rooms
        )
    
    def _delete_room(self, room_id):
        if messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment supprimer cette salle ?\nCette action est irréversible."
        ):
            self.db_manager.delete_room(room_id)
            self._load_rooms()
            messagebox.showinfo("✅ Succès", "Salle supprimée avec succès.")
    
    def _perform_search(self, query):
        if query:
            results = self.db_manager.search_rooms(query)
            self._load_rooms(results)
        else:
            self._load_rooms()
