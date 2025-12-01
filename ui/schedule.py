"""
Module de gestion de l'emploi du temps
Création et gestion des séances avec validations
"""
import customtkinter as ctk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import ModernTheme
from widgets.modern_components import *
from ui.print_dialogs import PrintScheduleDialog


class ScheduleForm(ctk.CTkToplevel):
    """Formulaire de séance avec validations"""
    
    def __init__(self, parent, db_manager, schedule_data=None, callback=None):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.schedule_data = schedule_data
        self.callback = callback
        
        self.title("📅 Créer une Séance" if not schedule_data else "✏️ Modifier la Séance")
        self.geometry("650x700")
        self.resizable(True, True)
        self.minsize(600, 600)
        
        self.transient(parent)
        self.grab_set()
        
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        self._load_data()
        self._create_ui()
        
        if schedule_data:
            self._fill_fields()
        
        self._center_window()
    
    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _load_data(self):
        self.groups = self.db_manager.get_all_groups()
        self.teachers = self.db_manager.get_all_teachers()
        self.rooms = self.db_manager.get_available_rooms()
    
    def _create_ui(self):
        # Container principal avec header fixe
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 0))
        
        ModernLabel(header_frame, text="📅 Créer une séance", style='heading').pack(pady=(0, 15))
        
        # Frame scrollable pour tout le contenu
        main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=ModernTheme.PRIMARY,
            scrollbar_button_hover_color=ModernTheme.PRIMARY_HOVER
        )
        main.pack(fill="both", expand=True, padx=30, pady=(10, 20))
        
        # SECTION 1: Temporel
        time_card = ModernCard(main)
        time_card.pack(fill="x", pady=(0, 15))
        
        time_content = ctk.CTkFrame(time_card, fg_color="transparent")
        time_content.pack(fill="both", padx=20, pady=20)
        
        ModernLabel(time_content, text="⏰ Informations temporelles", style='subheading').pack(anchor="w", pady=(0, 15))
        
        # Jour
        ModernLabel(time_content, text="Jour *", style='normal').pack(anchor="w", pady=(0, 5))
        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
        self.jour_combo = ModernComboBox(time_content, values=jours)
        self.jour_combo.pack(fill="x", pady=(0, 20))
        
        # Période
        ModernLabel(time_content, text="Période *", style='normal').pack(anchor="w", pady=(0, 8))
        self.periode_var = ctk.StringVar(value="Matin")
        
        periode_frame = ctk.CTkFrame(time_content, fg_color="transparent")
        periode_frame.pack(fill="x", pady=(0, 20))
        
        for periode in ["Matin", "Après-midi", "Soir"]:
            rb = ctk.CTkRadioButton(
                periode_frame,
                text=periode,
                variable=self.periode_var,
                value=periode,
                fg_color=ModernTheme.PRIMARY,
                hover_color=ModernTheme.PRIMARY_HOVER
            )
            rb.pack(side="left", padx=(0, 25))
        
        # Horaires
        ModernLabel(time_content, text="Horaire *", style='normal').pack(anchor="w", pady=(0, 5))
        horaire_frame = ctk.CTkFrame(time_content, fg_color="transparent")
        horaire_frame.pack(fill="x", pady=(0, 10))
        
        self.heure_debut = ModernEntry(horaire_frame, placeholder="08:00", width=100)
        self.heure_debut.pack(side="left")
        
        ModernLabel(horaire_frame, text=" → ", style='normal').pack(side="left", padx=10)
        
        self.heure_fin = ModernEntry(horaire_frame, placeholder="10:00", width=100)
        self.heure_fin.pack(side="left")
        
        # SECTION 2: Assignations
        assign_card = ModernCard(main)
        assign_card.pack(fill="x", pady=(0, 15))
        
        assign_content = ctk.CTkFrame(assign_card, fg_color="transparent")
        assign_content.pack(fill="both", padx=20, pady=20)
        
        ModernLabel(assign_content, text="👥 Assignations", style='subheading').pack(anchor="w", pady=(0, 15))
        
        # Groupe
        ModernLabel(assign_content, text="Groupe *", style='normal').pack(anchor="w", pady=(0, 5))
        group_names = [f"{g[0]} - {g[1]}" for g in self.groups] if self.groups else ["Aucun groupe"]
        self.group_combo = ModernComboBox(assign_content, values=group_names)
        self.group_combo.pack(fill="x", pady=(0, 15))
        
        # Professeur
        ModernLabel(assign_content, text="Professeur *", style='normal').pack(anchor="w", pady=(0, 5))
        teacher_names = [f"{t[0]} - {t[1]} {t[2]}" for t in self.teachers] if self.teachers else ["Aucun prof"]
        self.teacher_combo = ModernComboBox(assign_content, values=teacher_names)
        self.teacher_combo.pack(fill="x", pady=(0, 15))
        
        # Salle
        ModernLabel(assign_content, text="Salle *", style='normal').pack(anchor="w", pady=(0, 5))
        room_names = [f"{r[0]} - {r[1]} ({r[2]} places)" for r in self.rooms] if self.rooms else ["Aucune salle"]
        self.room_combo = ModernComboBox(assign_content, values=room_names)
        self.room_combo.pack(fill="x", pady=(0, 10))
        
        # Note
        note = ModernLabel(main, text="* Champs obligatoires | Les conflits sont vérifiés automatiquement", style='small')
        note.pack(anchor="w", pady=(8, 0))
        
        # Boutons
        btns = ctk.CTkFrame(main, fg_color="transparent")
        btns.pack(fill="x", pady=(15, 10))
        
        ModernButton(btns, "Annuler", "❌", 'outline', command=self.destroy).pack(side="right", padx=(10, 0))
        ModernButton(btns, "Enregistrer", "💾", 'success', command=self._save).pack(side="right")
    
    def _fill_fields(self):
        if self.schedule_data:
            details = self.db_manager.get_schedule_details(self.schedule_data[0])
            if details:
                self.jour_combo.set(details[4])
                self.periode_var.set(details[5])
                self.heure_debut.insert(0, details[6])
                self.heure_fin.insert(0, details[7])
                
                # Group
                for g in self.groups:
                    if g[0] == details[1]:
                        self.group_combo.set(f"{g[0]} - {g[1]}")
                        break
                
                # Teacher
                for t in self.teachers:
                    if t[0] == details[2]:
                        self.teacher_combo.set(f"{t[0]} - {t[1]} {t[2]}")
                        break
                
                # Room
                for r in self.rooms:
                    if r[0] == details[3]:
                        self.room_combo.set(f"{r[0]} - {r[1]} ({r[2]} places)")
                        break
    
    def _save(self):
        jour = self.jour_combo.get()
        periode = self.periode_var.get()
        heure_debut = self.heure_debut.get()
        heure_fin = self.heure_fin.get()
        
        group_sel = self.group_combo.get()
        teacher_sel = self.teacher_combo.get()
        room_sel = self.room_combo.get()
        
        # Validations basiques
        if not all([jour, periode, heure_debut, heure_fin, group_sel, teacher_sel, room_sel]):
            messagebox.showerror("Erreur", "Tous les champs obligatoires doivent être remplis.")
            return
        
        if any(x == "Aucun" for x in [group_sel, teacher_sel, room_sel]):
            messagebox.showerror("Erreur", "Veuillez sélectionner tous les éléments requis.")
            return
        
        # Extraire les IDs
        try:
            group_id = int(group_sel.split(" - ")[0])
            teacher_id = int(teacher_sel.split(" - ")[0])
            room_id = int(room_sel.split(" - ")[0])
        except:
            messagebox.showerror("Erreur", "Sélections invalides.")
            return
        
        # Vérifier horaires
        if heure_fin <= heure_debut:
            messagebox.showerror("Erreur", "L'heure de fin doit être après l'heure de début.")
            return
        
        # Vérifier conflits
        exclude_id = self.schedule_data[0] if self.schedule_data else None
        
        if self.db_manager.check_room_conflict(room_id, jour, heure_debut, heure_fin, exclude_id):
            messagebox.showerror("Conflit", "❌ La salle est déjà occupée à cet horaire.")
            return
        
        if self.db_manager.check_teacher_conflict(teacher_id, jour, heure_debut, heure_fin, exclude_id):
            messagebox.showerror("Conflit", "❌ Le professeur est déjà occupé à cet horaire.")
            return
        
        if self.db_manager.check_group_conflict(group_id, jour, heure_debut, heure_fin, exclude_id):
            messagebox.showerror("Conflit", "❌ Le groupe a déjà un cours à cet horaire.")
            return
        
        # Sauvegarder
        try:
            if self.schedule_data:
                self.db_manager.update_schedule(
                    self.schedule_data[0], group_id, teacher_id, room_id,
                    jour, periode, heure_debut, heure_fin
                )
                messagebox.showinfo("✅ Succès", "Séance modifiée avec succès.")
            else:
                self.db_manager.add_schedule(
                    group_id, teacher_id, room_id,
                    jour, periode, heure_debut, heure_fin
                )
                messagebox.showinfo("✅ Succès", "Séance créée avec succès.")
            
            if self.callback:
                self.callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")


class SchedulePage(ctk.CTkFrame):
    """Page de gestion de l'emploi du temps"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.db_manager = db_manager
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self._create_ui()
        self._load_schedules()
    
    def _create_ui(self):
        header = PageHeader(
            self,
            title="📅 Emploi du Temps",
            subtitle="Gérez les séances de cours avec validation automatique",
            add_button_text="Nouvelle Séance",
            add_callback=self._open_add_dialog
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Barre de recherche et bouton d'impression
        search_container = ctk.CTkFrame(self, fg_color="transparent")
        search_container.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        search_container.grid_columnconfigure(0, weight=1)
        
        search_bar = SearchBar(
            search_container,
            placeholder="Rechercher une séance...",
            search_callback=self._perform_search,
            refresh_callback=self._load_schedules
        )
        search_bar.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ModernButton(
            search_container,
            text="🖨️ Imprimer",
            command=self._open_print_dialog,
            style='primary',
            width=140
        ).grid(row=0, column=1)
        
        table_card = ModernCard(self)
        table_card.grid(row=2, column=0, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)
        
        # Table BorderedTable avec grille complète
        self.table = BorderedTable(
            table_card,
            headers=["Jour", "Période", "Horaire", "Groupe", "Prof", "Salle", "Actions"],
            column_weights=[1, 1, 1, 2, 2, 1, 1]  # Jour, Période, Horaire, Groupe, Prof, Salle, Actions
        )
        self.table.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    def _load_schedules(self, schedules=None):
        self.table.clear()
        
        if schedules is None:
            schedules = self.db_manager.get_all_schedules()
        
        if not schedules:
            self.table.add_row([{"text": "Aucune séance trouvée", "colspan": 7, "fg": ModernTheme.TEXT_SECONDARY}])
            return
        
        for schedule in schedules:
            self._create_schedule_row(schedule)
    
    def _create_schedule_row(self, schedule):
        def create_actions_widget(parent):
            actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
            
            edit_btn = ModernButton(
                actions_frame,
                text="Modifier",
                style="outline",
                width=32, height=26,
                command=lambda: self._open_edit_dialog(schedule)
            )
            edit_btn.pack(side="left", padx=2)
            
            delete_btn = ModernButton(
                actions_frame,
                text="Supprimer",
                style="danger",
                width=32, height=26,
                command=lambda: self._delete_schedule(schedule[0])
            )
            delete_btn.pack(side="left", padx=2)
            
            return actions_frame
        
        data = [
            {"text": schedule[1], "font_size": 11},  # Jour
            {"text": schedule[2], "font_size": 11},  # Période
            {"text": f"{schedule[3]}-{schedule[4]}", "font_size": 11},  # Horaire
            {"text": schedule[5], "font_size": 11},  # Groupe
            {"text": schedule[7], "font_size": 11},  # Prof
            {"text": schedule[8], "font_size": 11},  # Salle
            create_actions_widget  # Actions
        ]
        
        self.table.add_row(data)
    
    def _open_add_dialog(self):
        ScheduleForm(self, self.db_manager, callback=self._load_schedules)
    
    def _open_edit_dialog(self, schedule):
        ScheduleForm(self, self.db_manager, schedule_data=schedule, callback=self._load_schedules)
    
    def _delete_schedule(self, schedule_id):
        if messagebox.askyesno("Confirmation", "Supprimer cette séance ?"):
            self.db_manager.delete_schedule(schedule_id)
            self._load_schedules()
            messagebox.showinfo("✅ Succès", "Séance supprimée.")
    
    def _perform_search(self, query):
        if query:
            results = self.db_manager.search_schedules(query)
            self._load_schedules(results)
        else:
            self._load_schedules()
    
    def _open_print_dialog(self):
        """Ouvrir le dialogue d'impression d'emploi du temps"""
        PrintScheduleDialog(self, self.db_manager)
