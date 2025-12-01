"""
Paramètres - Interface d'administration
Gestion des niveaux scolaires
"""
import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import customtkinter as ctk
from database.db_manager_v2 import DatabaseManagerV2
from widgets.modern_components import (
    ModernButton, ModernLabel, ModernEntry, 
    BorderedTable, ModernCard
)


class ParametresPage(ctk.CTkFrame):
    """Page de gestion des paramètres système"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        self.db_manager = db_manager
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header
        self._create_header()
        
        # Niveaux section
        self._create_niveaux_section()
        
        # Load initial data
        self._load_niveaux()
    
    def _create_header(self):
        """Créer l'en-tête de la page"""
        from config.theme import ModernTheme
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(0, 20))
        
        title = ctk.CTkLabel(
            header_frame,
            text="⚙️ Paramètres",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK)
        )
        title.pack(side=tk.LEFT, pady=5)
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="  •  Gestion des niveaux scolaires",
            font=ctk.CTkFont(size=14),
            text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
        )
        subtitle.pack(side=tk.LEFT, padx=(10, 0), pady=5)
    
    def _create_niveaux_section(self):
        """Créer la section de gestion des niveaux"""
        # Section header
        from config.theme import ModernTheme
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=1, column=0, sticky="ew", padx=25, pady=(0, 10))
        header.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header,
            text="📚 Niveaux Scolaires",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK)
        )
        title.pack(side=tk.LEFT)
        
        # Add button
        add_btn = ModernButton(
            header,
            text="➕ Ajouter Niveau",
            command=self._add_niveau,
            width=180,
            height=40
        )
        add_btn.pack(side=tk.RIGHT, padx=10)
        
        # Table card
        table_card = ModernCard(self)
        table_card.grid(row=2, column=0, sticky="nsew", padx=25, pady=(0, 25))
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(0, weight=1)
        
        # Scrollable container
        scroll_container = ctk.CTkScrollableFrame(
            table_card,
            fg_color="transparent"
        )
        scroll_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        scroll_container.grid_columnconfigure(0, weight=1)
        
        # Table
        self.table = BorderedTable(
            scroll_container,
            headers=["ID", "Nom du Niveau", "Ordre", "Statut", "Actions"],
            column_weights=[1, 3, 1, 1, 2]
        )
        self.table.grid(row=0, column=0, sticky="nsew")
    
    def _load_niveaux(self):
        """Charger la liste des niveaux"""
        try:
            from config.theme import ModernTheme
            self.table.clear()
            niveaux = self.db_manager.get_all_niveaux(actif_only=False)
            
            for niveau in niveaux:
                niveau_id = niveau[0]
                nom = niveau[1]
                ordre = niveau[2]
                actif = niveau[3]
                
                statut = "✅ Actif" if actif else "❌ Inactif"
                
                def create_actions_widget(parent_frame):
                    """Créer les boutons d'action pour une ligne"""
                    niveau_data = niveau  # Capture la variable
                    
                    actions_container = ctk.CTkFrame(parent_frame, fg_color="transparent")
                    
                    # Bouton modifier
                    edit_btn = ctk.CTkButton(
                        actions_container,
                        text="Modifier",
                        width=75,
                        height=26,
                        corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
                        fg_color=(ModernTheme.WARNING, ModernTheme.WARNING),
                        hover_color=("#F57C00", "#F57C00"),
                        font=ctk.CTkFont(size=11),
                        command=lambda: self._edit_niveau(niveau_data)
                    )
                    edit_btn.pack(side="left", padx=(0, 4))
                    
                    # Bouton supprimer
                    delete_btn = ctk.CTkButton(
                        actions_container,
                        text="Supprimer",
                        width=75,
                        height=26,
                        corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
                        fg_color=(ModernTheme.DANGER, ModernTheme.DANGER),
                        hover_color=(ModernTheme.BTN_DANGER_HOVER, ModernTheme.BTN_DANGER_HOVER),
                        font=ctk.CTkFont(size=11),
                        command=lambda: self._delete_niveau(niveau_data)
                    )
                    delete_btn.pack(side="left")
                    
                    return actions_container
                
                self.table.add_row([
                    str(niveau_id),
                    nom,
                    str(ordre),
                    statut,
                    create_actions_widget
                ])
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def _add_niveau(self):
        """Ouvrir le dialogue d'ajout de niveau"""
        NiveauDialog(self, self.db_manager, callback=self._load_niveaux)
    
    def _edit_niveau(self, niveau_data):
        """Modifier un niveau existant"""
        NiveauDialog(
            self, 
            self.db_manager, 
            niveau_data=niveau_data,
            callback=self._load_niveaux
        )
    
    def _delete_niveau(self, niveau_data):
        """Supprimer (désactiver) un niveau"""
        niveau_id = niveau_data[0]
        nom = niveau_data[1]
        
        result = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment désactiver le niveau '{nom}' ?\n\n"
            "Note: Le niveau sera marqué comme inactif mais les données existantes seront préservées."
        )
        
        if result:
            try:
                self.db_manager.delete_niveau(niveau_id)
                messagebox.showinfo("Succès", "Niveau désactivé avec succès")
                self._load_niveaux()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")


class NiveauDialog(ctk.CTkToplevel):
    """Dialogue pour ajouter/modifier un niveau"""
    
    def __init__(self, parent, db_manager, niveau_data=None, callback=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.niveau_data = niveau_data
        self.callback = callback
        
        # Configuration de la fenêtre
        self.title("Modifier le niveau" if niveau_data else "Ajouter un niveau")
        self.geometry("500x450")
        self.resizable(False, False)
        
        # Center window
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
        # Load data if editing
        if niveau_data:
            self._load_data()
    
    def _create_widgets(self):
        """Créer les widgets du dialogue"""
        from config.theme import ModernTheme
        
        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title_text = "✏️ Modifier le niveau" if self.niveau_data else "➕ Ajouter un niveau"
        title = ctk.CTkLabel(
            container,
            text=title_text,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK)
        )
        title.pack(pady=(0, 25))
        
        # Nom du niveau
        nom_label = ctk.CTkLabel(
            container,
            text="Nom du niveau *",
            font=ctk.CTkFont(size=12),
            text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK),
            anchor="w"
        )
        nom_label.pack(fill=tk.X, pady=(10, 5))
        
        self.nom_entry = ModernEntry(
            container,
            placeholder="Ex: Primaire CE1, Lycée 1ère Année..."
        )
        self.nom_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Ordre
        ordre_label = ctk.CTkLabel(
            container,
            text="Ordre d'affichage *",
            font=ctk.CTkFont(size=12),
            text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK),
            anchor="w"
        )
        ordre_label.pack(fill=tk.X, pady=(10, 5))
        
        self.ordre_entry = ModernEntry(
            container,
            placeholder="Ex: 1, 2, 3..."
        )
        self.ordre_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Actif checkbox
        self.actif_var = tk.BooleanVar(value=True)
        actif_check = ctk.CTkCheckBox(
            container,
            text="Niveau actif",
            variable=self.actif_var,
            font=ctk.CTkFont(size=12)
        )
        actif_check.pack(anchor=tk.W, pady=(10, 20))
        
        # Note
        note = ctk.CTkLabel(
            container,
            text="* Champs obligatoires",
            font=ctk.CTkFont(size=10, slant="italic"),
            text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK),
            anchor="w"
        )
        note.pack(fill=tk.X, pady=(5, 20))
        
        # Buttons
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        save_text = "Modifier" if self.niveau_data else "Enregistrer"
        save_btn = ModernButton(
            btn_frame,
            text=save_text,
            command=self._save_niveau,
            width=150,
            height=40
        )
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Annuler",
            command=self.destroy,
            width=150,
            height=40,
            fg_color=(ModernTheme.BTN_SECONDARY, ModernTheme.BTN_SECONDARY),
            hover_color=(ModernTheme.BTN_SECONDARY_HOVER, ModernTheme.BTN_SECONDARY_HOVER)
        )
        cancel_btn.pack(side=tk.RIGHT)
    
    def _load_data(self):
        """Charger les données du niveau à modifier"""
        if self.niveau_data:
            self.nom_entry.insert(0, self.niveau_data[1])
            self.ordre_entry.insert(0, str(self.niveau_data[2]))
            self.actif_var.set(bool(self.niveau_data[3]))
    
    def _save_niveau(self):
        """Sauvegarder le niveau"""
        # Validation
        nom = self.nom_entry.get().strip()
        ordre = self.ordre_entry.get().strip()
        
        if not nom:
            messagebox.showwarning("Validation", "Le nom du niveau est obligatoire")
            self.nom_entry.focus()
            return
        
        if not ordre:
            messagebox.showwarning("Validation", "L'ordre est obligatoire")
            self.ordre_entry.focus()
            return
        
        try:
            ordre = int(ordre)
        except ValueError:
            messagebox.showwarning("Validation", "L'ordre doit être un nombre entier")
            self.ordre_entry.focus()
            return
        
        actif = 1 if self.actif_var.get() else 0
        
        try:
            if self.niveau_data:
                # Update
                niveau_id = self.niveau_data[0]
                self.db_manager.update_niveau(niveau_id, nom, ordre, actif)
                messagebox.showinfo("Succès", "Niveau modifié avec succès")
            else:
                # Insert
                self.db_manager.add_niveau(nom, ordre, actif)
                messagebox.showinfo("Succès", "Niveau ajouté avec succès")
            
            # Callback to refresh parent table
            if self.callback:
                self.callback()
            
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement: {str(e)}")


# Test standalone
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Test - Paramètres")
    root.geometry("1000x700")
    
    db = DatabaseManagerV2()
    page = ParametresPage(root, db)
    page.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()
