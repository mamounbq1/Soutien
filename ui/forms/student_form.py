"""
Formulaire de gestion des élèves (extrait de ui/students.py)
"""

import customtkinter as ctk
from .base_form import BaseForm
from widgets.modern_components import ModernLabel, ModernEntry, ModernComboBox, ModernCard, ModernButton
from utils.messages import Messages


class StudentForm(BaseForm):
    """Formulaire d'élève modernisé"""
    
    def __init__(self, parent, db_manager, student_data=None, callback=None):
        self.db_manager = db_manager
        title = "📝 Ajouter un Élève" if not student_data else "✏️ Modifier l'Élève"
        
        super().__init__(parent, title, width=550, height=700, 
                         data=student_data, callback=callback)
        
        self._create_ui()
        
        if student_data:
            self._fill_fields()
    
    def _get_niveaux(self):
        """Récupérer la liste des niveaux depuis la DB"""
        try:
            niveaux_data = self.db_manager.get_all_niveaux(actif_only=True)
            return [n[1] for n in niveaux_data]  # n[1] = nom_niveau
        except:
            # Fallback values if DB fails
            return ["Primaire", "Collège", "Lycée", "Supérieur"]
    
    def _create_ui(self):
        """Crée l'interface du formulaire"""
        # En-tête
        header = ModernLabel(
            self.main_container,
            text="👨‍🎓 Informations de l'élève",
            style='heading'
        )
        header.pack(pady=(0, 25))
        
        # Carte de formulaire
        form_card = ModernCard(self.main_container)
        form_card.pack(fill="both", expand=True)
        
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Grille pour les champs
        form_content.grid_columnconfigure(1, weight=1)
        
        # Nom
        self.create_field(form_content, "Nom *", 0)
        self.nom = ModernEntry(form_content, placeholder="Ex: Alami")
        self.nom.grid(row=0, column=1, pady=10, sticky="ew")
        
        # Prénom
        self.create_field(form_content, "Prénom *", 1)
        self.prenom = ModernEntry(form_content, placeholder="Ex: Ahmed")
        self.prenom.grid(row=1, column=1, pady=10, sticky="ew")
        
        # Niveau (ComboBox with values from DB)
        self.create_field(form_content, "Niveau", 2)
        niveaux = self._get_niveaux()
        self.niveau = ModernComboBox(
            form_content,
            values=niveaux
        )
        self.niveau.set("")
        self.niveau.grid(row=2, column=1, pady=10, sticky="ew")
        
        # Téléphone
        self.create_field(form_content, "Téléphone", 3)
        self.telephone = ModernEntry(form_content, placeholder="Ex: 0612345678")
        self.telephone.grid(row=3, column=1, pady=10, sticky="ew")
        
        # Téléphone Parents
        self.create_field(form_content, "Tél. Parents", 4)
        self.tel_parents = ModernEntry(form_content, placeholder="Ex: 0698765432")
        self.tel_parents.grid(row=4, column=1, pady=10, sticky="ew")
        
        # Note
        note_label = ModernLabel(
            form_content,
            text="* Champs obligatoires",
            style='small'
        )
        note_label.grid(row=5, column=0, columnspan=2, pady=(15, 0), sticky="w")
        
        # Boutons
        buttons_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=(25, 0))
        
        save_btn = ModernButton(
            buttons_frame,
            text="💾 Enregistrer",
            command=self._save,
            style="primary"
        )
        save_btn.pack(side="left", padx=5)
        
        cancel_btn = ModernButton(
            buttons_frame,
            text="✕ Annuler",
            command=self.destroy,
            style="secondary"
        )
        cancel_btn.pack(side="left", padx=5)
    
    def _fill_fields(self):
        """Remplit les champs avec les données existantes"""
        if not self.data:
            return
        
        # Format: (id, nom, prenom, tel, adresse, ..., classe as niveau)
        # Indices: 0=id, 1=nom, 2=prenom, 3=tel, 4=adresse, 10=classe (shown as niveau)
        student_id = self.data[0]
        nom = self.data[1]
        prenom = self.data[2]
        tel = self.data[3]
        adresse = self.data[4] if len(self.data) > 4 else ""
        niveau = self.data[10] if len(self.data) > 10 else ""
        
        # Extraction tel_parents depuis adresse
        tel_parents = ""
        if adresse:
            parts = adresse.split('|')
            for part in parts:
                if part.startswith("Parent:"):
                    tel_parents = part.replace("Parent:", "").strip()
        
        self.nom.insert(0, nom or "")
        self.prenom.insert(0, prenom or "")
        self.niveau.insert(0, niveau or "")
        self.telephone.insert(0, tel or "")
        self.tel_parents.insert(0, tel_parents)
    
    def _save(self):
        """Enregistrer l'élève"""
        # Validation
        if not self.validate_required({"Nom": self.nom.get(), "Prénom": self.prenom.get()}):
            return
        
        # Construction de l'adresse (juste tel_parents maintenant)
        adresse = ""
        if self.tel_parents.get():
            adresse = f"Parent: {self.tel_parents.get()}"
        
        try:
            if self.data:  # Modification
                student_id = self.data[0]
                self.db_manager.update_eleve(
                    student_id,
                    self.nom.get(),
                    self.prenom.get(),
                    "",  # filiere not used
                    self.niveau.get(),  # niveau stored in classe
                    self.telephone.get(),
                    adresse
                )
                self.show_success(Messages.SUCCESS_UPDATE)
            else:  # Ajout
                self.db_manager.add_eleve(
                    self.nom.get(),
                    self.prenom.get(),
                    "",  # filiere not used
                    self.niveau.get(),  # niveau stored in classe
                    self.telephone.get(),
                    adresse
                )
                self.show_success(Messages.SUCCESS_ADD)
            
            self.close_and_callback()
        
        except Exception as e:
            self.show_error(f"{Messages.ERROR_SAVE}: {str(e)}")
