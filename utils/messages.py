"""
Messages et labels de l'application
Centralisation pour faciliter la traduction et la maintenance
"""

class Messages:
    """Messages de l'application en français"""
    
    # Messages d'erreur génériques
    ERROR_TITLE = "Erreur"
    SUCCESS_TITLE = "Succès"
    WARNING_TITLE = "Attention"
    INFO_TITLE = "Information"
    
    # Validation
    REQUIRED_FIELDS = "Les champs marqués avec * sont obligatoires"
    INVALID_PHONE = "Numéro de téléphone invalide. Format attendu: 0612345678 ou +212612345678"
    INVALID_AMOUNT = "Le montant doit être un nombre positif"
    INVALID_EMAIL = "Adresse email invalide"
    
    # Élèves
    STUDENT_ADDED = "Élève ajouté avec succès"
    STUDENT_UPDATED = "Élève modifié avec succès"
    STUDENT_DELETED = "Élève supprimé avec succès"
    STUDENT_NAME_REQUIRED = "Le nom et le prénom de l'élève sont obligatoires"
    CONFIRM_DELETE_STUDENT = "Êtes-vous sûr de vouloir supprimer cet élève ?"
    
    # Professeurs
    TEACHER_ADDED = "Professeur ajouté avec succès"
    TEACHER_UPDATED = "Professeur modifié avec succès"
    TEACHER_DELETED = "Professeur supprimé avec succès"
    TEACHER_NAME_REQUIRED = "Le nom et le prénom du professeur sont obligatoires"
    CONFIRM_DELETE_TEACHER = "Êtes-vous sûr de vouloir supprimer ce professeur ?"
    
    # Matières
    SUBJECT_ADDED = "Matière ajoutée avec succès"
    SUBJECT_UPDATED = "Matière modifiée avec succès"
    SUBJECT_DELETED = "Matière supprimée avec succès"
    SUBJECT_NAME_REQUIRED = "Le nom de la matière est obligatoire"
    CONFIRM_DELETE_SUBJECT = "Êtes-vous sûr de vouloir supprimer cette matière ?"
    
    # Salles
    ROOM_ADDED = "Salle ajoutée avec succès"
    ROOM_UPDATED = "Salle modifiée avec succès"
    ROOM_DELETED = "Salle supprimée avec succès"
    ROOM_NAME_REQUIRED = "Le nom de la salle est obligatoire"
    ROOM_CAPACITY_REQUIRED = "La capacité de la salle est obligatoire"
    CONFIRM_DELETE_ROOM = "Êtes-vous sûr de vouloir supprimer cette salle ?"
    
    # Groupes
    GROUP_ADDED = "Groupe ajouté avec succès"
    GROUP_UPDATED = "Groupe modifié avec succès"
    GROUP_DELETED = "Groupe supprimé avec succès"
    GROUP_NAME_REQUIRED = "Le nom du groupe est obligatoire"
    CONFIRM_DELETE_GROUP = "Êtes-vous sûr de vouloir supprimer ce groupe ?"
    
    # Paiements
    PAYMENT_ADDED = "Paiement enregistré avec succès"
    PAYMENT_UPDATED = "Paiement modifié avec succès"
    PAYMENT_DELETED = "Paiement supprimé avec succès"
    PAYMENT_AMOUNT_REQUIRED = "Le montant du paiement est obligatoire"
    PAYMENT_STUDENT_REQUIRED = "Veuillez sélectionner un élève"
    CONFIRM_DELETE_PAYMENT = "Êtes-vous sûr de vouloir supprimer ce paiement ?"
    AMOUNT_MUST_BE_POSITIVE = "Le montant doit être supérieur à 0"
    
    # Emploi du temps
    SCHEDULE_ADDED = "Séance ajoutée à l'emploi du temps"
    SCHEDULE_UPDATED = "Séance modifiée avec succès"
    SCHEDULE_DELETED = "Séance supprimée avec succès"
    SCHEDULE_TIME_REQUIRED = "L'heure de début et de fin sont obligatoires"
    SCHEDULE_CONFLICT_ROOM = "Conflit détecté : la salle est déjà occupée à cet horaire"
    SCHEDULE_CONFLICT_TEACHER = "Conflit détecté : le professeur a déjà un cours à cet horaire"
    SCHEDULE_CONFLICT_GROUP = "Conflit détecté : le groupe a déjà un cours à cet horaire"
    CONFIRM_DELETE_SCHEDULE = "Êtes-vous sûr de vouloir supprimer cette séance ?"
    
    # Présence
    PRESENCE_SAVED = "Présence enregistrée avec succès"
    PRESENCE_UPDATED = "Présence modifiée avec succès"
    NO_STUDENTS_IN_GROUP = "Aucun élève inscrit dans ce groupe"
    SELECT_GROUP_AND_DATE = "Veuillez sélectionner un groupe et une date"
    
    # Base de données
    DB_ERROR = "Erreur de base de données"
    DB_CONNECTION_ERROR = "Impossible de se connecter à la base de données"
    DB_INTEGRITY_ERROR = "Erreur d'intégrité des données"
    
    # Général
    CANCEL = "Annuler"
    SAVE = "Enregistrer"
    DELETE = "Supprimer"
    EDIT = "Modifier"
    ADD = "Ajouter"
    SEARCH = "Rechercher"
    REFRESH = "Actualiser"
    CLOSE = "Fermer"
    YES = "Oui"
    NO = "Non"
    
    # Placeholders
    PH_NAME = "Ex: Alami"
    PH_FIRST_NAME = "Ex: Ahmed"
    PH_PHONE = "Ex: 0612345678"
    PH_PARENT_PHONE = "Ex: 0698765432"
    PH_EMAIL = "Ex: exemple@email.com"
    PH_ADDRESS = "Ex: Rue de la Liberté, Casablanca"
    PH_AMOUNT = "Ex: 500"
    PH_SEARCH = "Rechercher..."
    
    @staticmethod
    def confirm_delete(entity_name: str) -> str:
        """
        Génère un message de confirmation de suppression
        
        Args:
            entity_name: Nom de l'entité (ex: "cet élève", "cette matière")
        
        Returns:
            Message de confirmation
        """
        return f"Êtes-vous sûr de vouloir supprimer {entity_name} ?"
    
    @staticmethod
    def entity_added(entity_type: str) -> str:
        """
        Génère un message de succès d'ajout
        
        Args:
            entity_type: Type d'entité (ex: "Élève", "Professeur")
        
        Returns:
            Message de succès
        """
        return f"{entity_type} ajouté(e) avec succès"
    
    @staticmethod
    def entity_updated(entity_type: str) -> str:
        """
        Génère un message de succès de modification
        
        Args:
            entity_type: Type d'entité
        
        Returns:
            Message de succès
        """
        return f"{entity_type} modifié(e) avec succès"
    
    @staticmethod
    def entity_deleted(entity_type: str) -> str:
        """
        Génère un message de succès de suppression
        
        Args:
            entity_type: Type d'entité
        
        Returns:
            Message de succès
        """
        return f"{entity_type} supprimé(e) avec succès"
