"""
Service de gestion des professeurs
Couche métier entre l'UI et la base de données
"""

from typing import List, Tuple, Optional
from database.db_compatibility import DatabaseCompatibility
from utils.messages import Messages


class TeacherService:
    """Service pour la gestion des professeurs"""
    
    def __init__(self, db_manager: DatabaseCompatibility):
        self.db = db_manager
    
    def add_teacher(self, nom: str, prenom: str, matiere: str = "",
                   tel: str = "", salaire_horaire: float = 0) -> int:
        """
        Ajoute un nouveau professeur
        
        Args:
            nom: Nom du professeur
            prenom: Prénom du professeur
            matiere: Matière enseignée
            tel: Téléphone
            salaire_horaire: Salaire horaire
        
        Returns:
            ID du professeur créé
        
        Raises:
            ValueError: Si les données sont invalides
        """
        if not nom or not prenom:
            raise ValueError(Messages.TEACHER_NAME_REQUIRED)
        
        # Normalisation
        nom = nom.strip().title()
        prenom = prenom.strip().title()
        
        # Validation salaire
        if salaire_horaire < 0:
            raise ValueError(Messages.INVALID_AMOUNT)
        
        return self.db.add_teacher(nom, prenom, matiere, tel, salaire_horaire)
    
    def get_all_teachers(self, search_query: str = None) -> List[Tuple]:
        """Récupère tous les professeurs"""
        if search_query:
            return self.db.search_teachers(search_query)
        return self.db.get_all_teachers()
    
    def get_teacher_by_id(self, teacher_id: int) -> Optional[Tuple]:
        """Récupère un professeur par son ID"""
        return self.db.get_teacher_by_id(teacher_id)
    
    def update_teacher(self, teacher_id: int, nom: str, prenom: str,
                      matiere: str = "", tel: str = "", salaire_horaire: float = 0):
        """Met à jour un professeur"""
        if not nom or not prenom:
            raise ValueError(Messages.TEACHER_NAME_REQUIRED)
        
        nom = nom.strip().title()
        prenom = prenom.strip().title()
        
        if salaire_horaire < 0:
            raise ValueError(Messages.INVALID_AMOUNT)
        
        self.db.update_teacher(teacher_id, nom, prenom, matiere, tel, salaire_horaire)
    
    def delete_teacher(self, teacher_id: int):
        """Supprime un professeur"""
        self.db.delete_teacher(teacher_id)
    
    def get_teacher_stats(self) -> dict:
        """Calcule des statistiques sur les professeurs"""
        teachers = self.get_all_teachers()
        
        total_salaire = sum(t[5] for t in teachers if t[5])  # Colonne salaire_horaire
        
        stats = {
            'total': len(teachers),
            'average_salary': total_salaire / len(teachers) if teachers else 0,
            'by_matiere': {},
        }
        
        # Compter par matière
        for teacher in teachers:
            matiere = teacher[3] or "Non spécifié"  # Colonne matiere
            stats['by_matiere'][matiere] = stats['by_matiere'].get(matiere, 0) + 1
        
        return stats
