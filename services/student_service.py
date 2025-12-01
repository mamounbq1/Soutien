"""
Service de gestion des élèves
Couche métier entre l'UI et la base de données
"""

from typing import List, Tuple, Optional
from database.db_compatibility import DatabaseCompatibility
from utils.messages import Messages


class StudentService:
    """Service pour la gestion des élèves"""
    
    def __init__(self, db_manager):
        """
        Args:
            db_manager: Instance de DatabaseManagerV2 ou DatabaseCompatibility
        """
        self.db = db_manager
    
    # ═══════════════════════════════════════════════════════════
    # ALIAS POUR COMPATIBILITÉ AVEC DatabaseManagerV2
    # ═══════════════════════════════════════════════════════════
    
    def create_student(self, nom: str, prenom: str, telephone: str = "",
                      niveau: str = "", filiere: str = "") -> int:
        """Alias pour add_student (nommage cohérent)"""
        return self.add_student(nom, prenom, niveau, filiere, telephone, "")
    
    def add_student(self, nom: str, prenom: str, niveau: str = "", 
                   filiere: str = "", tel: str = "", parent_tel: str = "") -> int:
        """
        Ajoute un nouvel élève
        
        Args:
            nom: Nom de l'élève
            prenom: Prénom de l'élève
            niveau: Niveau scolaire
            filiere: Filière
            tel: Téléphone de l'élève
            parent_tel: Téléphone des parents
        
        Returns:
            ID de l'élève créé
        
        Raises:
            ValueError: Si les données sont invalides
        """
        # Validation métier
        if not nom or not prenom:
            raise ValueError(Messages.STUDENT_NAME_REQUIRED)
        
        # Normalisation des données
        nom = nom.strip().title()
        prenom = prenom.strip().title()
        tel = tel.strip() if tel else ""
        parent_tel = parent_tel.strip() if parent_tel else ""
        
        # Déléguer à la couche DB
        return self.db.add_student(nom, prenom, niveau, filiere, tel, parent_tel)
    
    def get_all_students(self, search_query: str = None) -> List[Tuple]:
        """
        Récupère tous les élèves ou filtre par recherche
        
        Args:
            search_query: Texte de recherche (optionnel)
        
        Returns:
            Liste des élèves
        """
        if search_query:
            # Appeler search_eleves ou search_students selon disponibilité
            if hasattr(self.db, 'search_students'):
                return self.db.search_students(search_query)
            elif hasattr(self.db, 'search_eleves'):
                return self.db.search_eleves(search_query)
        
        # Appeler get_all_students ou get_all_eleves selon disponibilité
        if hasattr(self.db, 'get_all_students'):
            return self.db.get_all_students()
        elif hasattr(self.db, 'get_all_eleves'):
            return self.db.get_all_eleves()
        return []
    
    def search_students(self, query: str) -> List[Tuple]:
        """Alias pour recherche"""
        return self.get_all_students(search_query=query)
    
    def get_student_by_id(self, student_id: int) -> Optional[Tuple]:
        """
        Récupère un élève par son ID
        
        Args:
            student_id: ID de l'élève
        
        Returns:
            Tuple avec les données de l'élève ou None
        """
        if hasattr(self.db, 'get_student_by_id'):
            return self.db.get_student_by_id(student_id)
        elif hasattr(self.db, 'get_eleve_by_id'):
            return self.db.get_eleve_by_id(student_id)
        return None
    
    def update_student(self, student_id: int, nom: str, prenom: str,
                      niveau: str = "", filiere: str = "", 
                      tel: str = "", parent_tel: str = ""):
        """
        Met à jour un élève
        
        Args:
            student_id: ID de l'élève à modifier
            nom: Nouveau nom
            prenom: Nouveau prénom
            niveau: Nouveau niveau
            filiere: Nouvelle filière
            tel: Nouveau téléphone
            parent_tel: Nouveau téléphone parent
        
        Raises:
            ValueError: Si les données sont invalides
        """
        if not nom or not prenom:
            raise ValueError(Messages.STUDENT_NAME_REQUIRED)
        
        # Normalisation (strip uniquement)
        nom = nom.strip()
        prenom = prenom.strip()
        
        # Construction adresse composite pour compatibility
        adresse = f"{niveau}|{filiere}|{parent_tel}"
        
        if hasattr(self.db, 'update_student'):
            self.db.update_student(student_id, nom, prenom, niveau, filiere, tel, parent_tel)
        elif hasattr(self.db, 'update_eleve'):
            self.db.update_eleve(student_id, nom, prenom, tel, adresse)
        return True
    
    def delete_student(self, student_id: int) -> bool:
        """
        Supprime un élève
        
        Args:
            student_id: ID de l'élève à supprimer
        
        Returns:
            True si succès
        """
        if hasattr(self.db, 'delete_student'):
            self.db.delete_student(student_id)
        elif hasattr(self.db, 'delete_eleve'):
            self.db.delete_eleve(student_id)
        return True
    
    def get_student_stats(self) -> dict:
        """
        Calcule des statistiques sur les élèves
        
        Returns:
            Dictionnaire avec les statistiques
        """
        students = self.get_all_students()
        
        stats = {
            'total': len(students),
            'by_niveau': {},
            'with_phone': sum(1 for s in students if s[5]),  # Colonne tel
            'with_parent_phone': sum(1 for s in students if s[6]),  # Colonne parent_tel
        }
        
        # Compter par niveau
        for student in students:
            niveau = student[3] or "Non spécifié"  # Colonne niveau
            stats['by_niveau'][niveau] = stats['by_niveau'].get(niveau, 0) + 1
        
        return stats
