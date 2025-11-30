"""
Page de gestion des groupes modernisée
"""
import customtkinter as ctk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import ModernTheme
from widgets.modern_components import *

class GroupForm(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, group_data=None, callback=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.group_data = group_data
        self.callback = callback
        
        self.title("👥 Ajouter un Groupe" if not group_data else "✏️ Modifier le Groupe")
        self.geometry("550x600")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        self.subjects_list = self.db_manager.get_all_subjects()
        self.teachers_list = self.db_manager.get_all_teachers()
        
        self._create_ui()
        if group_data:
            self._fill_fields()
        self._center_window()
    
    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _create_ui(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=30, pady=30)
        
        ModernLabel(main, text="👥 Informations du groupe", style='heading').pack(pady=(0, 25))
        
        card = ModernCard(main)
        card.pack(fill="both", expand=True)
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=25)
        content.grid_columnconfigure(1, weight=1)
        
        ModernLabel(content, text="Nom du Groupe *").grid(row=0, column=0, padx=(0,15), pady=10, sticky="w")
        self.nom = ModernEntry(content, placeholder="Ex: Groupe A")
        self.nom.grid(row=0, column=1, pady=10, sticky="ew")
        
        ModernLabel(content, text="Matière").grid(row=1, column=0, padx=(0,15), pady=10, sticky="w")
        subject_names = [f"{s[0]} - {s[1]}" for s in self.subjects_list] if self.subjects_list else ["Aucune matière"]
        self.matiere_combo = ModernComboBox(content, values=subject_names)
        self.matiere_combo.grid(row=1, column=1, pady=10, sticky="ew")
        
        ModernLabel(content, text="Professeur").grid(row=2, column=0, padx=(0,15), pady=10, sticky="w")
        teacher_names = [f"{t[0]} - {t[1]} {t[2]}" for t in self.teachers_list] if self.teachers_list else ["Aucun enseignant"]
        self.prof_combo = ModernComboBox(content, values=teacher_names)
        self.prof_combo.grid(row=2, column=1, pady=10, sticky="ew")
        
        ModernLabel(content, text="Salle").grid(row=3, column=0, padx=(0,15), pady=10, sticky="w")
        self.salle = ModernEntry(content, placeholder="Ex: Salle 101")
        self.salle.grid(row=3, column=1, pady=10, sticky="ew")
        
        ModernLabel(content, text="* Champs obligatoires", style='small').grid(row=4, column=0, columnspan=2, pady=(15,5), sticky="w")
        
        btns = ctk.CTkFrame(main, fg_color="transparent")
        btns.pack(fill="x", pady=(20,0))
        ModernButton(btns, "Annuler", "❌", 'outline', command=self.destroy).pack(side="right", padx=(10,0))
        ModernButton(btns, "Enregistrer", "💾", 'success', command=self._save).pack(side="right")
    
    def _fill_fields(self):
        if self.group_data:
            details = self.db_manager.get_group_details(self.group_data[0])
            if details:
                self.nom.insert(0, details[1])
                if details[2]:
                    for s in self.subjects_list:
                        if s[0] == details[2]:
                            self.matiere_combo.set(f"{s[0]} - {s[1]}")
                            break
                if details[3]:
                    for t in self.teachers_list:
                        if t[0] == details[3]:
                            self.prof_combo.set(f"{t[0]} - {t[1]} {t[2]}")
                            break
                self.salle.insert(0, details[4] or "")
    
    def _save(self):
        nom = self.nom.get()
        if not nom:
            messagebox.showerror("Erreur", "Le nom du groupe est obligatoire.")
            return
        
        matiere_id = prof_id = None
        mat_sel = self.matiere_combo.get()
        if mat_sel and mat_sel != "Aucune matière":
            try: matiere_id = int(mat_sel.split(" - ")[0])
            except: pass
        
        prof_sel = self.prof_combo.get()
        if prof_sel and prof_sel != "Aucun enseignant":
            try: prof_id = int(prof_sel.split(" - ")[0])
            except: pass
        
        salle = self.salle.get()
        
        if self.group_data:
            self.db_manager.update_group(self.group_data[0], nom, matiere_id, prof_id, salle)
            messagebox.showinfo("✅ Succès", "Groupe modifié avec succès.")
        else:
            self.db_manager.add_group(nom, matiere_id, prof_id, salle)
            messagebox.showinfo("✅ Succès", "Groupe ajouté avec succès.")
        
        if self.callback: self.callback()
        self.destroy()

class GroupsPage(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        self.db_manager = db_manager
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._create_ui()
        self._load_groups()
    
    def _create_ui(self):
        PageHeader(self, "👥 Gestion des Groupes", "Organisez vos groupes de cours", "Nouveau Groupe", self._open_add).grid(row=0, column=0, sticky="ew", pady=(0,20))
        SearchBar(self, "Rechercher un groupe...", self._search, self._load_groups).grid(row=1, column=0, sticky="ew", pady=(0,15))
        
        card = ModernCard(self)
        card.grid(row=2, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)
        
        TableHeader(card, ["Nom du Groupe", "Matière", "Professeur", "Salle", "Actions"]).grid(row=0, column=0, sticky="ew", padx=20, pady=(20,0))
        
        self.scroll_frame = ctk.CTkScrollableFrame(card, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10,20))
        self.scroll_frame.grid_columnconfigure(0, weight=1)
    
    def _load_groups(self, groups=None):
        for w in self.scroll_frame.winfo_children(): w.destroy()
        if groups is None: groups = self.db_manager.get_all_groups()
        if not groups:
            ModernLabel(self.scroll_frame, "Aucun groupe trouvé", 'secondary').pack(pady=40)
            return
        for i, g in enumerate(groups):
            actions = ActionButtons(self.scroll_frame, lambda grp=g: self._edit(grp), lambda id=g[0]: self._delete(id))
            TableRow(self.scroll_frame, [g[1], g[2] or "-", g[3] or "-", g[4] or "-"], actions, i%2==0).pack(fill="x", pady=2)
    
    def _open_add(self): GroupForm(self, self.db_manager, callback=self._load_groups)
    def _edit(self, g): GroupForm(self, self.db_manager, g, self._load_groups)
    def _delete(self, id):
        if messagebox.askyesno("Confirmation", "Supprimer ce groupe ?"):
            self.db_manager.delete_group(id)
            self._load_groups()
            messagebox.showinfo("✅ Succès", "Groupe supprimé.")
    def _search(self, q):
        self._load_groups(self.db_manager.search_groups(q) if q else None)
