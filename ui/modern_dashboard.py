"""
Dashboard modernisé avec design professionnel
- Cartes statistiques avec gradient
- Tableau des paiements récents stylisé
- Animations et transitions
"""

import customtkinter as ctk
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import ModernTheme


class ModernStatCard(ctk.CTkFrame):
    """Carte de statistique modernisée - ultra compacte (25% plus petite)"""
    
    def __init__(self, master, title, value, icon, color_scheme, **kwargs):
        # Récupérer les couleurs du schéma
        bg_color, hover_color = color_scheme
        
        super().__init__(
            master,
            corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
            fg_color=bg_color,
            **kwargs
        )
        
        # Hauteur ultra réduite (25% de moins: 90 - 25% = 68px)
        self.configure(height=68)
        self.grid_columnconfigure(0, weight=1)
        
        # Container avec padding ultra réduit
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=8, pady=5)
        
        # Frame pour l'icône et le titre
        top_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 2))
        
        # Icône encore plus petite (18px - 25% de moins que 24px)
        icon_label = ctk.CTkLabel(
            top_frame,
            text=icon,
            font=ctk.CTkFont(size=18),
            text_color="white"
        )
        icon_label.pack(side="left")
        
        # Titre (police lisible)
        title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=ctk.CTkFont(size=10, weight="normal"),
            text_color="white",
            anchor="w"
        )
        title_label.pack(fill="x")
        
        # Valeur (police plus grande pour lisibilité)
        value_label = ctk.CTkLabel(
            content_frame,
            text=str(value),
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white",
            anchor="w"
        )
        value_label.pack(fill="x", pady=(1, 0))
        
        # Effet hover subtil
        self.bind("<Enter>", lambda e: self.configure(fg_color=hover_color))
        self.bind("<Leave>", lambda e: self.configure(fg_color=bg_color))


class ModernDashboard(ctk.CTkFrame):
    """
    Dashboard modernisé avec design professionnel
    - Cartes statistiques attractives
    - Tableau stylisé
    - Layout responsive
    """
    
    def __init__(self, master, db_manager):
        super().__init__(
            master,
            corner_radius=0,
            fg_color="transparent"
        )
        
        self.db_manager = db_manager
        
        # Configuration de la grille
        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="col")
        self.grid_rowconfigure(3, weight=1)
        
        self._create_header()
        self._create_stat_cards()
        self._create_recent_payments_section()
    
    def _create_header(self):
        """Crée l'en-tête du dashboard"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 15))
        
        # Titre (réduit de 25%)
        title_label = ctk.CTkLabel(
            header_frame,
            text="Tableau de Bord",
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_XXLARGE, weight="bold"),
            text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK)
        )
        title_label.pack(side="left")
        
        # Date actuelle (réduit de 25%)
        date_str = datetime.now().strftime("%A %d %B %Y")
        date_label = ctk.CTkLabel(
            header_frame,
            text=date_str,
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
            text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
        )
        date_label.pack(side="right", padx=(0, 8))
    
    def _create_stat_cards(self):
        """Crée les cartes de statistiques avec lazy loading (OPTIMISÉ)"""
        # Stocker les références aux cartes pour mise à jour ultérieure
        self.stat_cards = {}
        self.stat_value_labels = {}
        
        # Configuration des cartes (sans valeurs initialement)
        stats_config = [
            ("Total Élèves", ModernTheme.ICONS['students'], 0),
            ("Total Enseignants", ModernTheme.ICONS['teachers'], 1),
            ("Total Groupes", ModernTheme.ICONS['groups'], 2),
            ("Total Matières", ModernTheme.ICONS['subjects'], 3),
        ]
        
        # Créer les cartes avec placeholder "..."
        for title, icon, col in stats_config:
            color_scheme = ModernTheme.get_stat_color(col)
            card = self._create_stat_card_placeholder(
                self,
                title=title,
                icon=icon,
                color_scheme=color_scheme
            )
            card.grid(row=1, column=col, padx=8, pady=8, sticky="ew")
            self.stat_cards[title] = card
        
        # Cartes de la deuxième ligne (aussi avec placeholders)
        revenue_card = self._create_stat_card_placeholder(
            self,
            title="Revenus ce mois",
            icon=ModernTheme.ICONS['payments'],
            color_scheme=ModernTheme.get_stat_color(4)
        )
        revenue_card.grid(row=2, column=0, columnspan=2, padx=8, pady=8, sticky="ew")
        self.stat_cards["Revenus ce mois"] = revenue_card
        
        payments_card = self._create_stat_card_placeholder(
            self,
            title="Total Paiements",
            icon="📄",
            color_scheme=ModernTheme.get_stat_color(5)
        )
        payments_card.grid(row=2, column=2, columnspan=2, padx=8, pady=8, sticky="ew")
        self.stat_cards["Total Paiements"] = payments_card
        
        # Charger les données réelles après 50ms (asynchrone)
        self.after(50, self._load_all_stats_async)
    
    def _create_stat_card_placeholder(self, master, title, icon, color_scheme):
        """Créer une carte avec placeholder '...' pour chargement rapide"""
        bg_color, hover_color = color_scheme
        
        card = ctk.CTkFrame(
            master,
            corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
            fg_color=bg_color,
            height=68
        )
        card.grid_columnconfigure(0, weight=1)
        
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=8, pady=5)
        
        top_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 2))
        
        icon_label = ctk.CTkLabel(
            top_frame,
            text=icon,
            font=ctk.CTkFont(size=18),
            text_color="white"
        )
        icon_label.pack(side="left")
        
        title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=ctk.CTkFont(size=10, weight="normal"),
            text_color="white",
            anchor="w"
        )
        title_label.pack(fill="x")
        
        # Label de valeur avec placeholder
        value_label = ctk.CTkLabel(
            content_frame,
            text="...",  # Placeholder
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white",
            anchor="w"
        )
        value_label.pack(fill="x", pady=(1, 0))
        
        # Stocker la référence au label de valeur
        self.stat_value_labels[title] = value_label
        
        # Effet hover
        card.bind("<Enter>", lambda e: card.configure(fg_color=hover_color))
        card.bind("<Leave>", lambda e: card.configure(fg_color=bg_color))
        
        return card
    
    def _load_all_stats_async(self):
        """Charger toutes les stats en UNE SEULE requête SQL (OPTIMISÉ)"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            # UNE SEULE REQUÊTE pour toutes les statistiques
            cursor.execute('''
                SELECT 
                    (SELECT COUNT(*) FROM ELEVE) as students,
                    (SELECT COUNT(*) FROM PROFESSEUR) as teachers,
                    (SELECT COUNT(*) FROM GROUPE) as groups,
                    (SELECT COUNT(*) FROM MATIERE) as subjects,
                    (SELECT COUNT(*) FROM PAIEMENT_ELEVE) as payments
            ''')
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                # Mettre à jour les cartes avec les valeurs réelles
                self._update_stat_value("Total Élèves", str(row[0]))
                self._update_stat_value("Total Enseignants", str(row[1]))
                self._update_stat_value("Total Groupes", str(row[2]))
                self._update_stat_value("Total Matières", str(row[3]))
                self._update_stat_value("Total Paiements", str(row[4]))
            
            # Charger les revenus séparément (calcul plus complexe)
            self.after(100, self._load_revenue_async)
            
        except Exception as e:
            print(f"Erreur chargement stats: {e}")
            # En cas d'erreur, afficher "0" au lieu de "..."
            for title in self.stat_value_labels:
                self._update_stat_value(title, "0")
    
    def _load_revenue_async(self):
        """Charger les revenus séparément"""
        try:
            revenue = self._get_monthly_revenue()
            self._update_stat_value("Revenus ce mois", f"{revenue} DH")
        except Exception as e:
            print(f"Erreur chargement revenus: {e}")
            self._update_stat_value("Revenus ce mois", "0 DH")
    
    def _update_stat_value(self, title, value):
        """Mettre à jour la valeur d'une carte de statistique"""
        if title in self.stat_value_labels:
            self.stat_value_labels[title].configure(text=str(value))
    
    def _create_recent_payments_section(self):
        """Crée la section des paiements récents"""
        # Frame principale (padding réduit)
        section_frame = ctk.CTkFrame(
            self,
            corner_radius=ModernTheme.BORDER_RADIUS,
            fg_color=(ModernTheme.BG_CARD_LIGHT, ModernTheme.BG_CARD_DARK)
        )
        section_frame.grid(row=3, column=0, columnspan=4, padx=8, pady=(8, 0), sticky="nsew")
        section_frame.grid_columnconfigure(0, weight=1)
        section_frame.grid_rowconfigure(1, weight=1)
        
        # En-tête de la section (padding réduit)
        header_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="💰 Paiements Récents",
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_LARGE, weight="bold"),
            text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
            anchor="w"
        )
        title_label.pack(side="left")
        
        # Bouton refresh (plus compact)
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄",
            width=32,
            height=32,
            corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
            fg_color=(ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK),
            hover_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK),
            text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
            font=ctk.CTkFont(size=16),
            command=self._refresh_payments
        )
        refresh_btn.pack(side="right")
        
        # Frame scrollable pour le tableau (padding réduit)
        self.payments_scroll = ctk.CTkScrollableFrame(
            section_frame,
            fg_color="transparent"
        )
        self.payments_scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        # Configuration de la grille - 5 colonnes simples
        self.payments_scroll.grid_columnconfigure(0, weight=2)  # Élève (plus large)
        self.payments_scroll.grid_columnconfigure(1, weight=1)  # Montant
        self.payments_scroll.grid_columnconfigure(2, weight=1)  # Mois
        self.payments_scroll.grid_columnconfigure(3, weight=1)  # Date
        self.payments_scroll.grid_columnconfigure(4, weight=1)  # Actions
        
        # Afficher un message "Chargement..." initialement
        loading_label = ctk.CTkLabel(
            self.payments_scroll,
            text="⏳ Chargement des paiements...",
            font=ctk.CTkFont(size=12),
            text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
        )
        loading_label.grid(row=0, column=0, columnspan=5, pady=20)
        
        # Charger les paiements après 200ms (asynchrone)
        self.after(200, self._load_recent_payments)
    
    def _load_recent_payments(self):
        """Charge et affiche les paiements récents"""
        try:
            # Nettoyer le contenu existant
            for widget in self.payments_scroll.winfo_children():
                widget.destroy()
            
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT pe.id_paiement_eleve, e.nom || ' ' || e.prenom as student, pe.montant_paye, pe.mois, 
                       pe.date_paiement, pe.id_eleve, e.nom, e.prenom, ''
                FROM PAIEMENT_ELEVE pe
                JOIN ELEVE e ON pe.id_eleve = e.id_eleve
                ORDER BY pe.date_paiement DESC
                LIMIT 10
            ''')
            payments = cursor.fetchall()
            conn.close()
            
            if not payments:
                # Message si aucun paiement
                no_data_label = ctk.CTkLabel(
                    self.payments_scroll,
                    text="Aucun paiement enregistré",
                    font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
                    text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
                )
                no_data_label.grid(row=0, column=0, columnspan=5, pady=20)
                return
            
            # En-têtes du tableau
            headers = ["Élève", "Montant", "Mois", "Date", "Actions"]
            for col, header in enumerate(headers):
                # Frame pour chaque en-tête avec bordure
                header_frame = ctk.CTkFrame(
                    self.payments_scroll,
                    fg_color=(ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK),
                    corner_radius=0,
                    border_width=1,
                    border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK)
                )
                header_frame.grid(row=0, column=col, sticky="nsew", padx=0, pady=0)
                
                header_label = ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=ctk.CTkFont(size=10, weight="bold"),
                    text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK),
                    anchor="w"
                )
                header_label.pack(padx=8, pady=6, fill="both", expand=True)
            
            # Lignes de données avec bordures
            for idx, payment in enumerate(payments, start=1):
                payment_id, student_name, montant, mois, date_paiement, student_id, nom, prenom, niveau = payment
                
                # Couleur alternée
                if idx % 2 == 0:
                    row_color = (ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK)
                else:
                    row_color = "transparent"
                
                # Données de la ligne
                row_data = [
                    student_name,
                    f"{montant} DH",
                    mois,
                    date_paiement[:10],
                    None  # Actions (bouton)
                ]
                
                for col, data in enumerate(row_data):
                    # Frame pour chaque cellule avec bordure
                    cell_frame = ctk.CTkFrame(
                        self.payments_scroll,
                        fg_color=row_color,
                        corner_radius=0,
                        border_width=1,
                        border_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK)
                    )
                    cell_frame.grid(row=idx, column=col, sticky="nsew", padx=0, pady=0)
                    
                    if col == 4:  # Colonne Actions
                        # Bouton Imprimer Reçu
                        print_btn = ctk.CTkButton(
                            cell_frame,
                            text="🖨️ Reçu",
                            width=70,
                            height=26,
                            corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
                            fg_color=(ModernTheme.PRIMARY, ModernTheme.PRIMARY),
                            hover_color=(ModernTheme.PRIMARY_DARK, ModernTheme.PRIMARY_DARK),
                            font=ctk.CTkFont(size=10),
                            command=lambda p_id=payment_id, s_nom=nom, s_prenom=prenom, s_niv=niveau, 
                                   p_mois=mois, p_montant=montant, p_date=date_paiement: 
                                   self._print_receipt(p_id, s_nom, s_prenom, s_niv, p_mois, p_montant, p_date)
                        )
                        print_btn.pack(padx=6, pady=4)
                    else:
                        # Label texte
                        text_color = (ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK)
                        font_size = 11
                        font_weight = "normal"
                        
                        # Couleur spéciale pour montant
                        if col == 1:  # Montant
                            text_color = (ModernTheme.SUCCESS, ModernTheme.SUCCESS)
                            font_weight = "bold"
                        elif col == 3:  # Date
                            text_color = (ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
                            font_size = 10
                        
                        cell_label = ctk.CTkLabel(
                            cell_frame,
                            text=data,
                            font=ctk.CTkFont(size=font_size, weight=font_weight),
                            text_color=text_color,
                            anchor="w"
                        )
                        cell_label.pack(padx=8, pady=6, fill="both", expand=True)
                
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.payments_scroll,
                text=f"Erreur: {str(e)}",
                font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
                text_color=(ModernTheme.DANGER, ModernTheme.DANGER)
            )
            error_label.grid(row=0, column=0, columnspan=5, pady=20)
    
    def _print_receipt(self, payment_id, nom, prenom, niveau, mois, montant, date_paiement):
        """Génère et ouvre le reçu de paiement"""
        try:
            from utils.pdf_generator import PDFGenerator
            
            # Préparer les données
            student_data = {
                'nom': nom,
                'prenom': prenom,
                'niveau': niveau
            }
            
            payment_data = {
                'montant': montant,
                'mois': mois,
                'annee': date_paiement[:4],
                'date_paiement': date_paiement,
                'reference': f"PAY-{payment_id:05d}"
            }
            
            # Générer le PDF
            pdf_gen = PDFGenerator()
            pdf_path = pdf_gen.generate_student_invoice(student_data, payment_data)
            
            # Ouvrir le PDF
            import subprocess
            import platform
            if platform.system() == 'Windows':
                os.startfile(pdf_path)
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', pdf_path])
            else:
                subprocess.Popen(['xdg-open', pdf_path])
                
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Erreur", f"Impossible de générer le reçu:\n{str(e)}")
    
    def _refresh_payments(self):
        """Rafraîchit la liste des paiements"""
        self._load_recent_payments()
    
    # === Méthodes de récupération des statistiques ===
    
    def _get_student_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM ELEVE")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def _get_teacher_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM PROFESSEUR")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def _get_group_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM GROUPE")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def _get_subject_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM MATIERE")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def _get_monthly_revenue(self):
        try:
            mois_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                       "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
            current_month = mois_fr[datetime.now().month - 1]
            current_year = str(datetime.now().year)
            revenue = self.db_manager.get_monthly_revenue(current_month, current_year)
            return revenue
        except:
            return 0
    
    def _get_payment_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM PAIEMENT_ELEVE")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
