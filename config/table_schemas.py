"""
Schémas standardisés des tableaux UI
Définit les colonnes et formats pour chaque module
"""

# ═══════════════════════════════════════════════════════════
# SCHÉMAS DES TABLEAUX PAR MODULE
# ═══════════════════════════════════════════════════════════

TABLE_SCHEMAS = {
    # Module Élèves
    "students": {
        "headers": ["ID", "Nom", "Prénom", "Niveau", "Filière", "Téléphone", "Actions"],
        "widths": [50, 150, 150, 100, 120, 120, 150],  # Largeurs relatives
        "alignments": ["center", "left", "left", "center", "left", "center", "center"]
    },
    
    # Module Professeurs
    "teachers": {
        "headers": ["ID", "Nom", "Prénom", "Matière", "Téléphone", "Salaire/h", "Actions"],
        "widths": [50, 150, 150, 150, 120, 100, 150],
        "alignments": ["center", "left", "left", "left", "center", "right", "center"]
    },
    
    # Module Matières
    "subjects": {
        "headers": ["ID", "Nom Matière", "Description", "Tarif/Mois", "Actions"],
        "widths": [50, 200, 300, 120, 150],
        "alignments": ["center", "left", "left", "right", "center"]
    },
    
    # Module Salles
    "rooms": {
        "headers": ["ID", "Nom Salle", "Capacité", "Équipement", "Statut", "Actions"],
        "widths": [50, 150, 100, 250, 100, 150],
        "alignments": ["center", "left", "center", "left", "center", "center"]
    },
    
    # Module Groupes
    "groups": {
        "headers": ["ID", "Nom Groupe", "Type", "Capacité", "Matière", "Niveau", "Élèves", "Actions"],
        "widths": [50, 150, 100, 80, 150, 100, 80, 150],
        "alignments": ["center", "left", "center", "center", "left", "center", "center", "center"]
    },
    
    # Module Paiements Élèves
    "payments": {
        "headers": ["ID", "Élève", "Montant Dû", "Montant Payé", "Mois", "Année", "Statut", "Actions"],
        "widths": [50, 200, 100, 100, 100, 80, 100, 150],
        "alignments": ["center", "left", "right", "right", "center", "center", "center", "center"]
    },
    
    # Module Emploi du Temps
    "schedule": {
        "headers": ["ID", "Groupe", "Jour", "Heure Début", "Heure Fin", "Salle", "Professeur", "Actions"],
        "widths": [50, 150, 100, 100, 100, 150, 150, 150],
        "alignments": ["center", "left", "center", "center", "center", "left", "left", "center"]
    },
    
    # Module Présence
    "presence": {
        "headers": ["ID", "Élève", "Groupe", "Date", "Statut", "Actions"],
        "widths": [50, 200, 150, 120, 100, 150],
        "alignments": ["center", "left", "left", "center", "center", "center"]
    }
}


def get_table_schema(module_name: str) -> dict:
    """
    Obtenir le schéma standardisé d'un tableau
    
    Args:
        module_name: Nom du module (students, teachers, etc.)
    
    Returns:
        Dict avec headers, widths, alignments
    """
    return TABLE_SCHEMAS.get(module_name, {
        "headers": [],
        "widths": [],
        "alignments": []
    })


def get_headers(module_name: str) -> list:
    """Obtenir uniquement les en-têtes d'un module"""
    schema = get_table_schema(module_name)
    return schema.get("headers", [])


def get_widths(module_name: str) -> list:
    """Obtenir uniquement les largeurs d'un module"""
    schema = get_table_schema(module_name)
    return schema.get("widths", [])


def get_alignments(module_name: str) -> list:
    """Obtenir uniquement les alignements d'un module"""
    schema = get_table_schema(module_name)
    return schema.get("alignments", [])
