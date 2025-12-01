"""
Page de gestion des paiements modernisée
Utilise les composants modernes pour un design professionnel
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import ModernTheme
from widgets.modern_components import (
    ModernButton,
    ModernEntry,
    ModernLabel,
    ModernComboBox,
    ModernCard,
    SearchBar,
    PageHeader,
    BorderedTable
)
from ui.print_dialogs import PrintStudentInvoiceDialog
from utils import center_window


class PaymentForm(ctk.CTkToplevel):
    """Formulaire de paiement modernisé"""
    
    def __init__(self, parent, db_manager, callback=None):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.callback = callback
        
        # Configuration de la fenêtre
        self.title("💰 Enregistrer un Paiement")
        self.geometry("550x650")
        self.resizable(False, False)
        
        # Rendre modal
        self.transient(parent)
        self.grab_set()
        
        # Configuration du fond
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        # Charger les étudiants
        self.students_list = self.db_manager.get_all_students()
        
        self._create_ui()
        
        # Centrer la fenêtre
        center_window(self)
    
    def _create_ui(self):
        """Crée l'interface du formulaire"""
        # Container principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # En-tête
        header = ModernLabel(
            main_container,
            text="💰 Enregistrer un paiement",
            style='heading'
        )
        header.pack(pady=(0, 25))
        
        # Carte de formulaire
        form_card = ModernCard(main_container)
        form_card.pack(fill="both", expand=True)
        
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Élève
        ModernLabel(form_content, text="Élève *", style='normal').pack(anchor="w", pady=(0, 5))
        student_names = [f"{s[0]} - {s[1]} {s[2]}" for s in self.students_list]
        self.student_combo = ModernComboBox(
            form_content,
            values=student_names if student_names else ["Aucun élève"]
        )
        self.student_combo.pack(fill="x", pady=(0, 15))
        
        # Montant
        ModernLabel(form_content, text="Montant (DH) *", style='normal').pack(anchor="w", pady=(0, 5))
        self.montant = ModernEntry(form_content, placeholder="Ex: 500")
        self.montant.pack(fill="x", pady=(0, 15))
        
        # Mois
        ModernLabel(form_content, text="Mois *", style='normal').pack(anchor="w", pady=(0, 5))
        mois_list = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                     "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        self.mois_combo = ModernComboBox(form_content, values=mois_list)
        self.mois_combo.set(mois_list[datetime.now().month - 1])
        self.mois_combo.pack(fill="x", pady=(0, 15))
        
        # Année
        ModernLabel(form_content, text="Année *", style='normal').pack(anchor="w", pady=(0, 5))
        current_year = datetime.now().year
        annee_list = [str(y) for y in range(current_year - 2, current_year + 2)]
        self.annee_combo = ModernComboBox(form_content, values=annee_list)
        self.annee_combo.set(str(current_year))
        self.annee_combo.pack(fill="x", pady=(0, 10))
        
        # Note
        note_label = ModernLabel(
            form_content,
            text="* Champs obligatoires",
            style='small'
        )
        note_label.pack(anchor="w", pady=(10, 0))
        
        # Boutons d'action
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
            command=self._save_payment
        )
        save_btn.pack(side="right")
    
    def _save_payment(self):
        """Sauvegarde le paiement"""
        montant = self.montant.get()
        mois = self.mois_combo.get()
        annee = self.annee_combo.get()
        
        if not montant:
            messagebox.showerror("Erreur", "Le montant est obligatoire.")
            return
        
        # Valider le montant
        try:
            montant = float(montant)
        except ValueError:
            messagebox.showerror("Erreur", "Le montant doit être un nombre.")
            return
        
        # Extraire l'ID de l'étudiant
        student_selection = self.student_combo.get()
        if not student_selection or student_selection == "Aucun élève":
            messagebox.showerror("Erreur", "Veuillez sélectionner un élève.")
            return
        
        try:
            student_id = int(student_selection.split(" - ")[0])
        except:
            messagebox.showerror("Erreur", "Élève invalide.")
            return

        self.db_manager.add_payment(student_id, montant, mois, annee)
        messagebox.showinfo("✅ Succès", "Paiement enregistré avec succès.")
        
        if self.callback:
            self.callback()
        self.destroy()


class PaymentsPage(ctk.CTkFrame):
    """Page de gestion des paiements modernisée"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.db_manager = db_manager
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        self._create_ui()
        self._load_payments()
    
    def _create_ui(self):
        """Crée l'interface utilisateur"""
        # En-tête de page
        header = PageHeader(
            self,
            title="💰 Paiements & Comptabilité",
            subtitle="Gérez les paiements et suivez les revenus",
            add_button_text="Nouveau Paiement",
            add_callback=self._open_add_dialog
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Statistiques
        self._create_stats_section()
        
        # Barre de recherche et bouton d'impression
        search_container = ctk.CTkFrame(self, fg_color="transparent")
        search_container.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        search_container.grid_columnconfigure(0, weight=1)
        
        search_bar = SearchBar(
            search_container,
            placeholder="Rechercher un paiement...",
            search_callback=self._perform_search,
            refresh_callback=self._load_payments
        )
        search_bar.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ModernButton(
            search_container,
            text="🖨️ Facture",
            command=self._open_print_dialog,
            style='primary',
            width=140
        ).grid(row=0, column=1)
        
        # Carte conteneur pour le tableau
        table_card = ModernCard(self)
        table_card.grid(row=3, column=0, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)
        
        # Table BorderedTable avec grille complète
        self.table = BorderedTable(
            table_card,
            headers=["Élève", "Montant", "Mois", "Année", "Date", "Actions"],
            column_weights=[3, 1, 1, 1, 1, 1]  # Élève, Montant, Mois, Année, Date, Actions
        )
        self.table.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    def _create_stats_section(self):
        """Crée la section des statistiques"""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        stats_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Revenus du mois en cours
        current_month = datetime.now().month
        current_year = str(datetime.now().year)
        mois_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                   "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        current_month_fr = mois_fr[current_month - 1]
        revenue = self.db_manager.get_monthly_revenue(current_month_fr, current_year)
        
        revenue_card = ModernCard(stats_frame)
        revenue_card.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        revenue_content = ctk.CTkFrame(revenue_card, fg_color="transparent")
        revenue_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ModernLabel(
            revenue_content,
            text="💵 Revenus ce mois",
            style='secondary'
        ).pack(anchor="w")
        
        ModernLabel(
            revenue_content,
            text=f"{revenue} DH",
            style='heading'
        ).pack(anchor="w", pady=(5, 0))
        
        ModernLabel(
            revenue_content,
            text=f"{current_month_fr} {current_year}",
            style='small'
        ).pack(anchor="w")
        
        # Total des paiements
        all_payments = self.db_manager.get_all_payments()
        
        total_card = ModernCard(stats_frame)
        total_card.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        total_content = ctk.CTkFrame(total_card, fg_color="transparent")
        total_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ModernLabel(
            total_content,
            text="📊 Total Paiements",
            style='secondary'
        ).pack(anchor="w")
        
        ModernLabel(
            total_content,
            text=str(len(all_payments)),
            style='heading'
        ).pack(anchor="w", pady=(5, 0))
        
        ModernLabel(
            total_content,
            text="transactions enregistrées",
            style='small'
        ).pack(anchor="w")
    
    def _load_payments(self, payments=None):
        """Charge et affiche les paiements"""
        self.table.clear()
        
        if payments is None:
            payments = self.db_manager.get_all_payments()
        
        if not payments:
            self.table.add_row([{"text": "Aucun paiement trouvé", "colspan": 6, "fg": ModernTheme.TEXT_SECONDARY}])
            return
        
        # Créer les lignes du tableau
        for payment in payments:
            self._create_payment_row(payment)
    
    def _create_payment_row(self, payment):
        """Crée une ligne pour un paiement"""
        # payment: (id, student_name, montant, mois, annee, date_paiement)
        
        def create_actions_widget(parent):
            actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
            
            delete_btn = ModernButton(
                actions_frame,
                text="Supprimer",
                style="danger",
                width=32, height=26,
                command=lambda: self._delete_payment(payment[0])
            )
            delete_btn.pack(side="left", padx=2)
            
            return actions_frame
        
        data = [
            {"text": payment[1], "font_size": 11},  # Élève
            {"text": f"{payment[2]} DH", "font_size": 11, "fg": ModernTheme.SUCCESS, "font_weight": "bold"},  # Montant
            {"text": payment[3], "font_size": 11},  # Mois
            {"text": payment[4], "font_size": 11},  # Année
            {"text": payment[5][:10], "font_size": 10, "fg": ModernTheme.TEXT_SECONDARY},  # Date
            create_actions_widget  # Actions
        ]
        
        self.table.add_row(data)
    
    def _open_add_dialog(self):
        """Ouvre le dialogue d'ajout"""
        PaymentForm(self, self.db_manager, callback=self._load_payments)
    
    def _delete_payment(self, payment_id):
        """Supprime un paiement"""
        if messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment supprimer ce paiement ?\nCette action est irréversible."
        ):
            self.db_manager.delete_payment(payment_id)
            # Recharger les paiements et les statistiques
            self._load_payments()
            # Recréer la section stats pour mettre à jour les chiffres
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and widget.grid_info().get('row') == 1:
                    widget.destroy()
            self._create_stats_section()
            messagebox.showinfo("✅ Succès", "Paiement supprimé avec succès.")
    
    def _open_print_dialog(self):
        """Ouvre le dialogue d'impression de facture"""
        PrintStudentInvoiceDialog(self, self.db_manager)
    
    def _perform_search(self, query):
        """Effectue une recherche"""
        if query:
            results = self.db_manager.search_payments(query)
            self._load_payments(results)
        else:
            self._load_payments()
