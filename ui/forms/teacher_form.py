"""
Formulaire de gestion des professeurs avec mode de paiement (Fixe/Heure/Élève)
"""

import customtkinter as ctk
from .base_form import BaseForm
from widgets.modern_components import ModernLabel, ModernEntry, ModernComboBox, ModernCard, ModernButton
from utils.messages import Messages


class TeacherForm(BaseForm):
    """Formulaire de professeur avec choix du mode de paiement"""
    
    def __init__(self, parent, db_manager, teacher_data=None, callback=None):
        self.db_manager = db_manager
        title = "📝 Ajouter un Professeur" if not teacher_data else "✏️ Modifier le Professeur"
        
        super().__init__(parent, title, width=550, height=720, 
                         data=teacher_data, callback=callback)
        
        self._create_ui()
        
        if teacher_data:
            self._fill_fields()
    
    def _create_ui(self):
        """Crée l'interface du formulaire"""
        # En-tête
        header = ModernLabel(
            self.main_container,
            text="👨‍🏫 Informations du professeur",
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
        self.nom = ModernEntry(form_content, placeholder="Ex: Benali")
        self.nom.grid(row=0, column=1, pady=10, sticky="ew")
        
        # Prénom
        self.create_field(form_content, "Prénom *", 1)
        self.prenom = ModernEntry(form_content, placeholder="Ex: Fatima")
        self.prenom.grid(row=1, column=1, pady=10, sticky="ew")
        
        # Matières (récupération depuis DB)
        self.create_field(form_content, "Matière *", 2)
        matieres = self._get_matieres()
        self.matiere = ModernComboBox(form_content, values=matieres)
        self.matiere.grid(row=2, column=1, pady=10, sticky="ew")
        self.matiere.set("")
        
        # Téléphone
        self.create_field(form_content, "Téléphone", 3)
        self.telephone = ModernEntry(form_content, placeholder="Ex: 0661234567")
        self.telephone.grid(row=3, column=1, pady=10, sticky="ew")
        
        # Mode de paiement
        self.create_field(form_content, "Mode de paiement *", 4)
        self.mode_paiement = ModernComboBox(
            form_content,
            values=["Salaire fixe", "Par heure", "Par élève"],
            command=self._on_payment_mode_change
        )
        self.mode_paiement.grid(row=4, column=1, pady=10, sticky="ew")
        self.mode_paiement.set("Par heure")
        
        # Frame pour les champs de tarif (conditionnel)
        self.tarif_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        self.tarif_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)
        self.tarif_frame.grid_columnconfigure(1, weight=1)
        
        # Salaire fixe (mensuel)
        self.salaire_fixe_label = ModernLabel(self.tarif_frame, text="Salaire mensuel (DH):", style='normal')
        self.salaire_fixe = ModernEntry(self.tarif_frame, placeholder="Ex: 5000")
        
        # Prix par heure
        self.prix_heure_label = ModernLabel(self.tarif_frame, text="Prix par heure (DH):", style='normal')
        self.prix_heure = ModernEntry(self.tarif_frame, placeholder="Ex: 150")
        
        # Tarif par élève
        self.tarif_eleve_label = ModernLabel(self.tarif_frame, text="Tarif par élève (DH):", style='normal')
        self.tarif_eleve = ModernEntry(self.tarif_frame, placeholder="Ex: 200")
        
        # Afficher les champs selon le mode par défaut
        self._on_payment_mode_change("Par heure")
        
        # Note
        note_label = ModernLabel(
            form_content,
            text="* Champs obligatoires",
            style='small'
        )
        note_label.grid(row=6, column=0, columnspan=2, pady=(15, 0), sticky="w")
        
        # Boutons
        buttons_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        buttons_frame.grid(row=7, column=0, columnspan=2, pady=(25, 0))
        
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
    
    def _on_payment_mode_change(self, choice):
        """Affiche les champs de tarif selon le mode sélectionné"""
        # Cacher tous les champs
        self.salaire_fixe_label.grid_forget()
        self.salaire_fixe.grid_forget()
        self.prix_heure_label.grid_forget()
        self.prix_heure.grid_forget()
        self.tarif_eleve_label.grid_forget()
        self.tarif_eleve.grid_forget()
        
        # Afficher les champs appropriés
        if choice == "Salaire fixe":
            self.salaire_fixe_label.grid(row=0, column=0, padx=(0, 15), pady=10, sticky="w")
            self.salaire_fixe.grid(row=0, column=1, pady=10, sticky="ew")
        elif choice == "Par heure":
            self.prix_heure_label.grid(row=0, column=0, padx=(0, 15), pady=10, sticky="w")
            self.prix_heure.grid(row=0, column=1, pady=10, sticky="ew")
        elif choice == "Par élève":
            self.tarif_eleve_label.grid(row=0, column=0, padx=(0, 15), pady=10, sticky="w")
            self.tarif_eleve.grid(row=0, column=1, pady=10, sticky="ew")
    
    def _get_matieres(self):
        """Récupérer la liste des matières"""
        try:
            matieres_data = self.db_manager.get_all_matieres()
            return [m[1] for m in matieres_data]  # m[1] = nom_matiere
        except:
            return []
    
    def _fill_fields(self):
        """Remplit les champs avec les données existantes"""
        if not self.data:
            return
        
        # Format: (id_prof, nom, prenom, tel, specialite, salaire_mois, prix_heure, tarif_eleve, type_paiement, ...)
        # Indices: 0=id, 1=nom, 2=prenom, 3=tel, 4=specialite, 5=salaire_mois, 6=prix_heure, 7=tarif_eleve, 8=type_paiement
        
        self.nom.insert(0, self.data[1] or "")
        self.prenom.insert(0, self.data[2] or "")
        self.telephone.insert(0, self.data[3] or "")
        
        # Matière depuis specialite
        if len(self.data) > 4 and self.data[4]:
            self.matiere.set(self.data[4])
        
        # Mode de paiement et tarifs
        type_paiement = self.data[8] if len(self.data) > 8 else "heure"
        salaire_mois = self.data[5] if len(self.data) > 5 else 0
        prix_heure = self.data[6] if len(self.data) > 6 else 0
        tarif_eleve = self.data[7] if len(self.data) > 7 else 0
        
        if type_paiement == "fixe":
            self.mode_paiement.set("Salaire fixe")
            self.salaire_fixe.insert(0, str(salaire_mois) if salaire_mois else "")
        elif type_paiement == "eleve":
            self.mode_paiement.set("Par élève")
            self.tarif_eleve.insert(0, str(tarif_eleve) if tarif_eleve else "")
        else:  # heure
            self.mode_paiement.set("Par heure")
            self.prix_heure.insert(0, str(prix_heure) if prix_heure else "")
    
    def _save(self):
        """Enregistrer le professeur"""
        # Validation
        if not self.validate_required({
            "Nom": self.nom.get(),
            "Prénom": self.prenom.get(),
            "Matière": self.matiere.get(),
            "Mode de paiement": self.mode_paiement.get()
        }):
            return
        
        # Déterminer le type de paiement et les montants
        mode = self.mode_paiement.get()
        salaire_mois = 0
        prix_heure = 0
        tarif_eleve = 0
        type_paiement = "heure"
        
        try:
            if mode == "Salaire fixe":
                type_paiement = "fixe"
                salaire_mois = float(self.salaire_fixe.get()) if self.salaire_fixe.get() else 0
                if salaire_mois < 0:
                    self.show_error("Le salaire ne peut pas être négatif")
                    return
            elif mode == "Par heure":
                type_paiement = "heure"
                prix_heure = float(self.prix_heure.get()) if self.prix_heure.get() else 0
                if prix_heure < 0:
                    self.show_error("Le prix horaire ne peut pas être négatif")
                    return
            elif mode == "Par élève":
                type_paiement = "eleve"
                tarif_eleve = float(self.tarif_eleve.get()) if self.tarif_eleve.get() else 0
                if tarif_eleve < 0:
                    self.show_error("Le tarif par élève ne peut pas être négatif")
                    return
        except ValueError:
            self.show_error("Les montants doivent être des nombres")
            return
        
        try:
            if self.data:  # Modification
                teacher_id = self.data[0]
                # Appeler directement la DB
                conn = self.db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE PROFESSEUR 
                    SET nom=?, prenom=?, telephone=?, specialite=?, 
                        salaire_mois=?, prix_par_heure=?, tarif_par_eleve=?, 
                        type_paiement=?, updated_at=CURRENT_TIMESTAMP
                    WHERE id_prof=?
                ''', (self.nom.get(), self.prenom.get(), self.telephone.get(),
                      self.matiere.get(), salaire_mois, prix_heure, tarif_eleve,
                      type_paiement, teacher_id))
                conn.commit()
                conn.close()
                self.show_success(Messages.SUCCESS_UPDATE)
            else:  # Ajout
                conn = self.db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO PROFESSEUR (nom, prenom, telephone, specialite, 
                                           salaire_mois, prix_par_heure, tarif_par_eleve, type_paiement)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (self.nom.get(), self.prenom.get(), self.telephone.get(),
                      self.matiere.get(), salaire_mois, prix_heure, tarif_eleve, type_paiement))
                conn.commit()
                conn.close()
                self.show_success(Messages.SUCCESS_ADD)
            
            self.close_and_callback()
        
        except Exception as e:
            self.show_error(f"{Messages.ERROR_SAVE}: {str(e)}")
