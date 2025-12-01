"""
Service de gestion des paiements
Couche métier entre l'UI et la base de données
"""

from typing import List, Tuple, Optional
from datetime import datetime
from database.db_compatibility import DatabaseCompatibility
from utils.messages import Messages


class PaymentService:
    """Service pour la gestion des paiements"""
    
    def __init__(self, db_manager):
        """
        Args:
            db_manager: Instance de DatabaseManagerV2 ou DatabaseCompatibility
        """
        self.db = db_manager
    
    # ═══════════════════════════════════════════════════════════
    # ALIAS POUR COMPATIBILITÉ
    # ═══════════════════════════════════════════════════════════
    
    def create_payment(self, id_eleve: int, montant: float,
                      mois: str, annee: int) -> int:
        """Alias pour add_payment"""
        return self.add_payment(id_eleve, montant, mois, str(annee))
    
    def get_payments_by_student(self, student_id: int) -> List[Tuple]:
        """Obtenir les paiements d'un élève"""
        if hasattr(self.db, 'get_payments_by_student'):
            return self.db.get_payments_by_student(student_id)
        elif hasattr(self.db, 'get_paiements_eleve'):
            return self.db.get_paiements_eleve(student_id)
        # Sinon filtrer manuellement
        all_payments = self.get_all_payments()
        # L'id_eleve peut être à différentes positions selon le modèle
        return [p for p in all_payments if (len(p) > 1 and p[1] == student_id)]
    
    def add_payment(self, student_id: int, montant: float, 
                   mois: str, annee: str) -> int:
        """
        Enregistre un nouveau paiement
        
        Args:
            student_id: ID de l'élève
            montant: Montant du paiement
            mois: Mois du paiement
            annee: Année du paiement
        
        Returns:
            ID du paiement créé
        
        Raises:
            ValueError: Si les données sont invalides
        """
        # Validation
        if montant <= 0:
            raise ValueError(Messages.AMOUNT_MUST_BE_POSITIVE)
        
        if not student_id:
            raise ValueError(Messages.PAYMENT_STUDENT_REQUIRED)
        
        return self.db.add_payment(student_id, montant, mois, annee)
    
    def get_all_payments(self, search_query: str = None) -> List[Tuple]:
        """Récupère tous les paiements"""
        if search_query:
            return self.db.search_payments(search_query)
        return self.db.get_all_payments()
    
    def get_payment_by_id(self, payment_id: int) -> Optional[Tuple]:
        """Récupère un paiement par son ID"""
        return self.db.get_payment_details(payment_id)
    
    def delete_payment(self, payment_id: int):
        """Supprime un paiement"""
        self.db.delete_payment(payment_id)
    
    def get_monthly_revenue(self, mois: str = None, annee: str = None) -> float:
        """
        Calcule le revenu pour un mois donné
        
        Args:
            mois: Mois (si None, mois actuel)
            annee: Année (si None, année actuelle)
        
        Returns:
            Montant total des revenus
        """
        if not mois or not annee:
            now = datetime.now()
            mois = mois or now.strftime("%B")
            annee = annee or str(now.year)
        
        return self.db.get_monthly_revenue(mois, annee)
    
    def get_payment_stats(self) -> dict:
        """
        Calcule des statistiques sur les paiements
        
        Returns:
            Dictionnaire avec les statistiques
        """
        payments = self.get_all_payments()
        
        total_amount = sum(p[2] for p in payments if len(p) > 2)  # Colonne montant
        
        stats = {
            'total_payments': len(payments),
            'total_amount': total_amount,
            'average_payment': total_amount / len(payments) if payments else 0,
            'by_month': {},
            'current_month_revenue': self.get_monthly_revenue(),
        }
        
        # Compter par mois
        for payment in payments:
            if len(payment) > 3:
                mois = payment[3]  # Colonne mois
                stats['by_month'][mois] = stats['by_month'].get(mois, 0) + payment[2]
        
        return stats
    
    def check_student_payment_status(self, student_id: int, 
                                    mois: str, annee: str) -> str:
        """
        Vérifie le statut de paiement d'un élève pour un mois donné
        
        Args:
            student_id: ID de l'élève
            mois: Mois à vérifier
            annee: Année à vérifier
        
        Returns:
            'paye', 'partiel', ou 'impaye'
        """
        # Cette méthode nécessite une requête spécifique
        # Pour l'instant, retourne un statut par défaut
        return 'impaye'
