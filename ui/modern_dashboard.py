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
    """Carte de statistique modernisée avec icône et design attractif"""
    
    def __init__(self, master, title, value, icon, color_scheme, **kwargs):
        # Récupérer les couleurs du schéma
        bg_color, hover_color = color_scheme
        
        super().__init__(
            master,
            corner_radius=ModernTheme.BORDER_RADIUS,
            fg_color=bg_color,
            **kwargs
        )
        
        self.configure(height=ModernTheme.CARD_HEIGHT)
        self.grid_columnconfigure(0, weight=1)
        
        # Container avec padding
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Frame pour l'icône et le titre
        top_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Icône
        icon_label = ctk.CTkLabel(
            top_frame,
            text=icon,
            font=ctk.CTkFont(size=32),
            text_color="white"
        )
        icon_label.pack(side="left")
        
        # Titre
        title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_SMALL, weight="normal"),
            text_color="white",
            anchor="w"
        )
        title_label.pack(fill="x")
        
        # Valeur
        value_label = ctk.CTkLabel(
            content_frame,
            text=str(value),
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_XXLARGE, weight="bold"),
            text_color="white",
            anchor="w"
        )
        value_label.pack(fill="x", pady=(5, 0))
        
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
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 25))
        
        # Titre
        title_label = ctk.CTkLabel(
            header_frame,
            text="Tableau de Bord",
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_XXLARGE, weight="bold"),
            text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK)
        )
        title_label.pack(side="left")
        
        # Date actuelle
        date_str = datetime.now().strftime("%A %d %B %Y")
        date_label = ctk.CTkLabel(
            header_frame,
            text=date_str,
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
            text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK)
        )
        date_label.pack(side="right", padx=(0, 10))
    
    def _create_stat_cards(self):
        """Crée les cartes de statistiques"""
        # Données des statistiques
        stats = [
            ("Total Élèves", self._get_student_count(), ModernTheme.ICONS['students'], 0),
            ("Total Enseignants", self._get_teacher_count(), ModernTheme.ICONS['teachers'], 1),
            ("Total Groupes", self._get_group_count(), ModernTheme.ICONS['groups'], 2),
            ("Total Matières", self._get_subject_count(), ModernTheme.ICONS['subjects'], 3),
        ]
        
        # Créer les cartes de la première ligne
        for title, value, icon, col in stats:
            color_scheme = ModernTheme.get_stat_color(col)
            card = ModernStatCard(
                self,
                title=title,
                value=value,
                icon=icon,
                color_scheme=color_scheme
            )
            card.grid(row=1, column=col, padx=8, pady=8, sticky="ew")
        
        # Cartes de la deuxième ligne
        revenue = self._get_monthly_revenue()
        payment_count = self._get_payment_count()
        
        revenue_card = ModernStatCard(
            self,
            title="Revenus ce mois",
            value=f"{revenue} DH",
            icon=ModernTheme.ICONS['payments'],
            color_scheme=ModernTheme.get_stat_color(4)
        )
        revenue_card.grid(row=2, column=0, columnspan=2, padx=8, pady=8, sticky="ew")
        
        payments_card = ModernStatCard(
            self,
            title="Total Paiements",
            value=payment_count,
            icon="📄",
            color_scheme=ModernTheme.get_stat_color(5)
        )
        payments_card.grid(row=2, column=2, columnspan=2, padx=8, pady=8, sticky="ew")
    
    def _create_recent_payments_section(self):
        """Crée la section des paiements récents"""
        # Frame principale
        section_frame = ctk.CTkFrame(
            self,
            corner_radius=ModernTheme.BORDER_RADIUS,
            fg_color=(ModernTheme.BG_CARD_LIGHT, ModernTheme.BG_CARD_DARK)
        )
        section_frame.grid(row=3, column=0, columnspan=4, padx=8, pady=(8, 0), sticky="nsew")
        section_frame.grid_columnconfigure(0, weight=1)
        section_frame.grid_rowconfigure(1, weight=1)
        
        # En-tête de la section
        header_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 15))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="💰 Paiements Récents",
            font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_LARGE, weight="bold"),
            text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
            anchor="w"
        )
        title_label.pack(side="left")
        
        # Bouton refresh
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄",
            width=40,
            height=40,
            corner_radius=ModernTheme.BORDER_RADIUS_SMALL,
            fg_color=(ModernTheme.BG_HOVER_LIGHT, ModernTheme.BG_HOVER_DARK),
            hover_color=(ModernTheme.BORDER_LIGHT, ModernTheme.BORDER_DARK),
            text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
            command=self._refresh_payments
        )
        refresh_btn.pack(side="right")
        
        # Frame scrollable pour le tableau
        self.payments_scroll = ctk.CTkScrollableFrame(
            section_frame,
            fg_color="transparent"
        )
        self.payments_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.payments_scroll.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self._load_recent_payments()
    
    def _load_recent_payments(self):
        """Charge et affiche les paiements récents"""
        try:
            # Nettoyer le contenu existant
            for widget in self.payments_scroll.winfo_children():
                widget.destroy()
            
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.nom || ' ' || s.prenom as student, p.montant, p.mois, p.date_paiement
                FROM paiements p
                JOIN students s ON p.student_id = s.id
                ORDER BY p.date_paiement DESC
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
                no_data_label.grid(row=0, column=0, columnspan=4, pady=40)
                return
            
            # En-têtes du tableau
            headers = ["Élève", "Montant", "Mois", "Date"]
            for i, header in enumerate(headers):
                header_label = ctk.CTkLabel(
                    self.payments_scroll,
                    text=header,
                    font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_SMALL, weight="bold"),
                    text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK),
                    anchor="w"
                )
                header_label.grid(row=0, column=i, padx=15, pady=(0, 10), sticky="w")
            
            # Lignes de données
            for idx, payment in enumerate(payments, start=1):
                row_frame = ctk.CTkFrame(
                    self.payments_scroll,
                    fg_color=(ModernTheme.BG_HOVER_LIGHT if idx % 2 == 0 else "transparent",
                             ModernTheme.BG_HOVER_DARK if idx % 2 == 0 else "transparent"),
                    corner_radius=ModernTheme.BORDER_RADIUS_SMALL
                )
                row_frame.grid(row=idx, column=0, columnspan=4, sticky="ew", pady=2)
                row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
                
                # Élève
                student_label = ctk.CTkLabel(
                    row_frame,
                    text=payment[0],
                    font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
                    text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
                    anchor="w"
                )
                student_label.grid(row=0, column=0, padx=15, pady=8, sticky="w")
                
                # Montant
                montant_label = ctk.CTkLabel(
                    row_frame,
                    text=f"{payment[1]} DH",
                    font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL, weight="bold"),
                    text_color=(ModernTheme.SUCCESS, ModernTheme.SUCCESS),
                    anchor="w"
                )
                montant_label.grid(row=0, column=1, padx=15, pady=8, sticky="w")
                
                # Mois
                mois_label = ctk.CTkLabel(
                    row_frame,
                    text=payment[2],
                    font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
                    text_color=(ModernTheme.TEXT_PRIMARY_LIGHT, ModernTheme.TEXT_PRIMARY_DARK),
                    anchor="w"
                )
                mois_label.grid(row=0, column=2, padx=15, pady=8, sticky="w")
                
                # Date
                date_label = ctk.CTkLabel(
                    row_frame,
                    text=payment[3][:10],
                    font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_SMALL),
                    text_color=(ModernTheme.TEXT_SECONDARY_LIGHT, ModernTheme.TEXT_SECONDARY_DARK),
                    anchor="w"
                )
                date_label.grid(row=0, column=3, padx=15, pady=8, sticky="w")
                
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.payments_scroll,
                text=f"Erreur: {str(e)}",
                font=ctk.CTkFont(size=ModernTheme.FONT_SIZE_NORMAL),
                text_color=(ModernTheme.DANGER, ModernTheme.DANGER)
            )
            error_label.grid(row=0, column=0, columnspan=4, pady=20)
    
    def _refresh_payments(self):
        """Rafraîchit la liste des paiements"""
        self._load_recent_payments()
    
    # === Méthodes de récupération des statistiques ===
    
    def _get_student_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def _get_teacher_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM teachers")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def _get_group_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM groups")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def _get_subject_count(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM subjects")
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
            cursor.execute("SELECT COUNT(*) FROM paiements")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
