"""
EXTENSION DU DATABASE MANAGER V2
=================================
Contient toutes les méthodes CRUD supplémentaires pour:
- MATIERE, SALLE, GROUPE, INSCRIPTION
- EMPLOI_DU_TEMPS
- PAIEMENT_ELEVE, PAIEMENT_PROF
- PRESENCE
- Méthodes de calcul et statistiques
"""

from database.db_manager_v2 import DatabaseManagerV2
from typing import List, Tuple, Optional, Dict
from datetime import datetime, timedelta
import calendar
import sqlite3

class DatabaseManagerV2Extended(DatabaseManagerV2):
    """Extension du gestionnaire avec toutes les méthodes CRUD"""
    
    # ════════════════════════════════════════════════════════════════
    # MÉTHODES CRUD - MATIERE
    # ════════════════════════════════════════════════════════════════
    
    def add_matiere(self, nom_matiere: str, description: str = "", 
                    tarif_mensuel: float = 0) -> int:
        """Ajouter une matière"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO MATIERE (nom_matiere, description, tarif_mensuel)
            VALUES (?, ?, ?)
        ''', (nom_matiere, description, tarif_mensuel))
        matiere_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return matiere_id

    def get_all_matieres(self) -> List[Tuple]:
        """Obtenir toutes les matières"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM MATIERE ORDER BY nom_matiere')
        data = cursor.fetchall()
        conn.close()
        return data

    def get_matiere_by_id(self, matiere_id: int) -> Optional[Tuple]:
        """Obtenir une matière par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM MATIERE WHERE id_matiere=?', (matiere_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_matiere(self, matiere_id: int, nom_matiere: str, 
                       description: str = "", tarif_mensuel: float = 0):
        """Mettre à jour une matière"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE MATIERE 
            SET nom_matiere=?, description=?, tarif_mensuel=?
            WHERE id_matiere=?
        ''', (nom_matiere, description, tarif_mensuel, matiere_id))
        conn.commit()
        conn.close()

    def delete_matiere(self, matiere_id: int):
        """Supprimer une matière"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM MATIERE WHERE id_matiere=?', (matiere_id,))
        conn.commit()
        conn.close()

    def search_matieres(self, query: str) -> List[Tuple]:
        """Rechercher des matières"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM MATIERE 
            WHERE nom_matiere LIKE ? OR description LIKE ?
            ORDER BY nom_matiere
        ''', (f'%{query}%', f'%{query}%'))
        data = cursor.fetchall()
        conn.close()
        return data

    # ════════════════════════════════════════════════════════════════
    # MÉTHODES CRUD - SALLE
    # ════════════════════════════════════════════════════════════════
    
    def add_salle(self, nom_salle: str, capacite: int, 
                  equipement: str = "", disponible: bool = True) -> int:
        """Ajouter une salle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO SALLE (nom_salle, capacite, equipement, disponible)
            VALUES (?, ?, ?, ?)
        ''', (nom_salle, capacite, equipement, 1 if disponible else 0))
        salle_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return salle_id

    def get_all_salles(self) -> List[Tuple]:
        """Obtenir toutes les salles"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM SALLE ORDER BY nom_salle')
        data = cursor.fetchall()
        conn.close()
        return data

    def get_salle_by_id(self, salle_id: int) -> Optional[Tuple]:
        """Obtenir une salle par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM SALLE WHERE id_salle=?', (salle_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    def get_salles_disponibles(self) -> List[Tuple]:
        """Obtenir les salles disponibles"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM SALLE WHERE disponible=1 ORDER BY nom_salle')
        data = cursor.fetchall()
        conn.close()
        return data

    def update_salle(self, salle_id: int, nom_salle: str, capacite: int,
                     equipement: str = "", disponible: bool = True):
        """Mettre à jour une salle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE SALLE 
            SET nom_salle=?, capacite=?, equipement=?, disponible=?
            WHERE id_salle=?
        ''', (nom_salle, capacite, equipement, 1 if disponible else 0, salle_id))
        conn.commit()
        conn.close()

    def delete_salle(self, salle_id: int):
        """Supprimer une salle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM SALLE WHERE id_salle=?', (salle_id,))
        conn.commit()
        conn.close()

    def search_salles(self, query: str) -> List[Tuple]:
        """Rechercher des salles"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM SALLE 
            WHERE nom_salle LIKE ? OR equipement LIKE ?
            ORDER BY nom_salle
        ''', (f'%{query}%', f'%{query}%'))
        data = cursor.fetchall()
        conn.close()
        return data

    # ════════════════════════════════════════════════════════════════
    # MÉTHODES CRUD - GROUPE
    # ════════════════════════════════════════════════════════════════
    
    def add_groupe(self, nom_groupe: str, id_matiere: int, id_prof: int = None,
                   id_salle: int = None, niveau: str = "", jour: str = "",
                   heure_debut: str = "", heure_fin: str = "",
                   type_groupe: str = "COLLECTIF", capacite_max: int = None) -> int:
        """
        Ajouter un groupe (cours individuel ou collectif)
        
        Args:
            type_groupe: 'INDIVIDUEL' ou 'COLLECTIF' (défaut)
            capacite_max: Nombre max d'élèves (optionnel pour collectif)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO GROUPE (nom_groupe, type_groupe, capacite_max, id_prof, 
                               id_matiere, id_salle, niveau, jour, heure_debut, heure_fin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nom_groupe, type_groupe, capacite_max, id_prof, id_matiere, 
              id_salle, niveau, jour, heure_debut, heure_fin))
        groupe_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return groupe_id

    def get_all_groupes(self) -> List[Tuple]:
        """Obtenir tous les groupes avec leurs relations"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                g.id_groupe, g.nom_groupe, g.type_groupe,
                CASE WHEN g.capacite_max IS NULL THEN '-' ELSE CAST(g.capacite_max AS TEXT) END as capacite,
                m.nom_matiere,
                COALESCE(p.nom || ' ' || p.prenom, '-') as professeur,
                COALESCE(s.nom_salle, '-') as salle,
                g.niveau, g.jour, g.heure_debut, g.heure_fin
            FROM GROUPE g
            LEFT JOIN MATIERE m ON g.id_matiere = m.id_matiere
            LEFT JOIN PROFESSEUR p ON g.id_prof = p.id_prof
            LEFT JOIN SALLE s ON g.id_salle = s.id_salle
            WHERE g.actif = 1
            ORDER BY g.type_groupe, g.nom_groupe
        ''')
        data = cursor.fetchall()
        conn.close()
        return data

    def get_groupe_by_id(self, groupe_id: int) -> Optional[Tuple]:
        """Obtenir un groupe par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM GROUPE WHERE id_groupe=?', (groupe_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_groupe(self, groupe_id: int, nom_groupe: str, id_matiere: int,
                      id_prof: int = None, id_salle: int = None, niveau: str = "",
                      jour: str = "", heure_debut: str = "", heure_fin: str = ""):
        """Mettre à jour un groupe"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE GROUPE 
            SET nom_groupe=?, id_prof=?, id_matiere=?, id_salle=?, niveau=?,
                jour=?, heure_debut=?, heure_fin=?, updated_at=CURRENT_TIMESTAMP
            WHERE id_groupe=?
        ''', (nom_groupe, id_prof, id_matiere, id_salle, niveau,
              jour, heure_debut, heure_fin, groupe_id))
        conn.commit()
        conn.close()

    def delete_groupe(self, groupe_id: int):
        """Supprimer un groupe (CASCADE sur inscriptions et EDT)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM GROUPE WHERE id_groupe=?', (groupe_id,))
        conn.commit()
        conn.close()

    def search_groupes(self, query: str) -> List[Tuple]:
        """Rechercher des groupes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                g.id_groupe, g.nom_groupe, 
                m.nom_matiere,
                COALESCE(p.nom || ' ' || p.prenom, '-') as professeur,
                COALESCE(s.nom_salle, '-') as salle,
                g.niveau, g.jour, g.heure_debut, g.heure_fin
            FROM GROUPE g
            LEFT JOIN MATIERE m ON g.id_matiere = m.id_matiere
            LEFT JOIN PROFESSEUR p ON g.id_prof = p.id_prof
            LEFT JOIN SALLE s ON g.id_salle = s.id_salle
            WHERE g.nom_groupe LIKE ? OR m.nom_matiere LIKE ? OR g.niveau LIKE ?
            ORDER BY g.nom_groupe
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        data = cursor.fetchall()
        conn.close()
        return data

    # ════════════════════════════════════════════════════════════════
    # MÉTHODES CRUD - INSCRIPTION
    # ════════════════════════════════════════════════════════════════
    
    def add_inscription(self, id_eleve: int, id_groupe: int, 
                        mensualite: float = 0) -> Optional[int]:
        """Ajouter une inscription"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Vérifier si l'inscription existe déjà
        cursor.execute('''
            SELECT id_inscription FROM INSCRIPTION 
            WHERE id_eleve=? AND id_groupe=?
        ''', (id_eleve, id_groupe))
        if cursor.fetchone():
            conn.close()
            return None  # Déjà inscrit
        
        cursor.execute('''
            INSERT INTO INSCRIPTION (id_eleve, id_groupe, mensualite, active)
            VALUES (?, ?, ?, 1)
        ''', (id_eleve, id_groupe, mensualite))
        inscription_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return inscription_id

    def get_inscriptions_by_eleve(self, id_eleve: int) -> List[Tuple]:
        """Obtenir les inscriptions d'un élève"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                i.id_inscription, i.date_inscription, i.mensualite, i.active,
                g.nom_groupe, m.nom_matiere, g.niveau
            FROM INSCRIPTION i
            JOIN GROUPE g ON i.id_groupe = g.id_groupe
            JOIN MATIERE m ON g.id_matiere = m.id_matiere
            WHERE i.id_eleve = ?
            ORDER BY i.date_inscription DESC
        ''', (id_eleve,))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_inscriptions_by_groupe(self, id_groupe: int) -> List[Tuple]:
        """Obtenir les élèves inscrits dans un groupe"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                i.id_inscription, e.id_eleve, e.nom, e.prenom, 
                e.telephone, i.mensualite, i.active, i.date_inscription
            FROM INSCRIPTION i
            JOIN ELEVE e ON i.id_eleve = e.id_eleve
            WHERE i.id_groupe = ? AND i.active = 1
            ORDER BY e.nom, e.prenom
        ''', (id_groupe,))
        data = cursor.fetchall()
        conn.close()
        return data

    def update_inscription_mensualite(self, inscription_id: int, mensualite: float):
        """Mettre à jour la mensualité d'une inscription"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE INSCRIPTION 
            SET mensualite=?
            WHERE id_inscription=?
        ''', (mensualite, inscription_id))
        conn.commit()
        conn.close()

    def desactiver_inscription(self, inscription_id: int):
        """Désactiver une inscription"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE INSCRIPTION 
            SET active=0
            WHERE id_inscription=?
        ''', (inscription_id,))
        conn.commit()
        conn.close()

    def activer_inscription(self, inscription_id: int):
        """Activer une inscription"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE INSCRIPTION 
            SET active=1
            WHERE id_inscription=?
        ''', (inscription_id,))
        conn.commit()
        conn.close()

    def delete_inscription(self, inscription_id: int):
        """Supprimer une inscription"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM INSCRIPTION WHERE id_inscription=?', (inscription_id,))
        conn.commit()
        conn.close()

    # ════════════════════════════════════════════════════════════════
    # MÉTHODES CRUD - EMPLOI_DU_TEMPS
    # ════════════════════════════════════════════════════════════════
    
    def add_emploi_du_temps(self, id_groupe: int, jour: str, heure_debut: str,
                            heure_fin: str, id_salle: int = None, 
                            id_prof: int = None, periode: str = "") -> int:
        """Ajouter une séance à l'emploi du temps"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO EMPLOI_DU_TEMPS (id_groupe, jour, heure_debut, heure_fin,
                                         id_salle, id_prof, periode, actif)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        ''', (id_groupe, jour, heure_debut, heure_fin, id_salle, id_prof, periode))
        edt_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return edt_id

    def get_all_emploi_du_temps(self) -> List[Tuple]:
        """Obtenir tout l'emploi du temps"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                e.id_edt, e.jour, e.heure_debut, e.heure_fin,
                g.nom_groupe, m.nom_matiere,
                COALESCE(p.nom || ' ' || p.prenom, '-') as professeur,
                COALESCE(s.nom_salle, '-') as salle,
                e.periode, e.actif
            FROM EMPLOI_DU_TEMPS e
            JOIN GROUPE g ON e.id_groupe = g.id_groupe
            JOIN MATIERE m ON g.id_matiere = m.id_matiere
            LEFT JOIN PROFESSEUR p ON e.id_prof = p.id_prof
            LEFT JOIN SALLE s ON e.id_salle = s.id_salle
            WHERE e.actif = 1
            ORDER BY 
                CASE e.jour
                    WHEN 'Lundi' THEN 1
                    WHEN 'Mardi' THEN 2
                    WHEN 'Mercredi' THEN 3
                    WHEN 'Jeudi' THEN 4
                    WHEN 'Vendredi' THEN 5
                    WHEN 'Samedi' THEN 6
                    WHEN 'Dimanche' THEN 7
                END,
                e.heure_debut
        ''')
        data = cursor.fetchall()
        conn.close()
        return data

    def get_emploi_du_temps_by_groupe(self, id_groupe: int) -> List[Tuple]:
        """Obtenir l'emploi du temps d'un groupe"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                e.id_edt, e.jour, e.heure_debut, e.heure_fin,
                COALESCE(p.nom || ' ' || p.prenom, '-') as professeur,
                COALESCE(s.nom_salle, '-') as salle,
                e.periode
            FROM EMPLOI_DU_TEMPS e
            LEFT JOIN PROFESSEUR p ON e.id_prof = p.id_prof
            LEFT JOIN SALLE s ON e.id_salle = s.id_salle
            WHERE e.id_groupe = ? AND e.actif = 1
            ORDER BY 
                CASE e.jour
                    WHEN 'Lundi' THEN 1
                    WHEN 'Mardi' THEN 2
                    WHEN 'Mercredi' THEN 3
                    WHEN 'Jeudi' THEN 4
                    WHEN 'Vendredi' THEN 5
                    WHEN 'Samedi' THEN 6
                END,
                e.heure_debut
        ''', (id_groupe,))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_emploi_du_temps_by_prof(self, id_prof: int) -> List[Tuple]:
        """Obtenir l'emploi du temps d'un professeur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                e.id_edt, e.jour, e.heure_debut, e.heure_fin,
                g.nom_groupe, m.nom_matiere,
                COALESCE(s.nom_salle, '-') as salle
            FROM EMPLOI_DU_TEMPS e
            JOIN GROUPE g ON e.id_groupe = g.id_groupe
            JOIN MATIERE m ON g.id_matiere = m.id_matiere
            LEFT JOIN SALLE s ON e.id_salle = s.id_salle
            WHERE e.id_prof = ? AND e.actif = 1
            ORDER BY 
                CASE e.jour
                    WHEN 'Lundi' THEN 1
                    WHEN 'Mardi' THEN 2
                    WHEN 'Mercredi' THEN 3
                    WHEN 'Jeudi' THEN 4
                    WHEN 'Vendredi' THEN 5
                    WHEN 'Samedi' THEN 6
                END,
                e.heure_debut
        ''', (id_prof,))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_edt_by_id(self, edt_id: int) -> Optional[Tuple]:
        """Obtenir une séance par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM EMPLOI_DU_TEMPS WHERE id_edt=?', (edt_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_emploi_du_temps(self, edt_id: int, id_groupe: int, jour: str,
                               heure_debut: str, heure_fin: str, id_salle: int = None,
                               id_prof: int = None, periode: str = ""):
        """Mettre à jour une séance"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE EMPLOI_DU_TEMPS 
            SET id_groupe=?, jour=?, heure_debut=?, heure_fin=?, 
                id_salle=?, id_prof=?, periode=?, updated_at=CURRENT_TIMESTAMP
            WHERE id_edt=?
        ''', (id_groupe, jour, heure_debut, heure_fin, id_salle, id_prof, periode, edt_id))
        conn.commit()
        conn.close()

    def delete_emploi_du_temps(self, edt_id: int):
        """Supprimer une séance"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM EMPLOI_DU_TEMPS WHERE id_edt=?', (edt_id,))
        conn.commit()
        conn.close()

    def desactiver_emploi_du_temps(self, edt_id: int):
        """Désactiver une séance"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE EMPLOI_DU_TEMPS 
            SET actif=0
            WHERE id_edt=?
        ''', (edt_id,))
        conn.commit()
        conn.close()

    # Vérifications de conflits
    def check_salle_conflit(self, id_salle: int, jour: str, heure_debut: str,
                            heure_fin: str, exclude_edt_id: int = None) -> bool:
        """Vérifier si la salle est disponible"""
        conn = self.get_connection()
        cursor = conn.cursor()
        query = '''
            SELECT COUNT(*) FROM EMPLOI_DU_TEMPS
            WHERE id_salle = ? AND jour = ? AND actif = 1
            AND ((heure_debut < ? AND heure_fin > ?) 
                 OR (heure_debut < ? AND heure_fin > ?)
                 OR (heure_debut >= ? AND heure_fin <= ?))
        '''
        params = [id_salle, jour, heure_fin, heure_debut, heure_fin, heure_fin, 
                  heure_debut, heure_fin]
        
        if exclude_edt_id:
            query += ' AND id_edt != ?'
            params.append(exclude_edt_id)
        
        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def check_prof_conflit(self, id_prof: int, jour: str, heure_debut: str,
                           heure_fin: str, exclude_edt_id: int = None) -> bool:
        """Vérifier si le professeur est disponible"""
        conn = self.get_connection()
        cursor = conn.cursor()
        query = '''
            SELECT COUNT(*) FROM EMPLOI_DU_TEMPS
            WHERE id_prof = ? AND jour = ? AND actif = 1
            AND ((heure_debut < ? AND heure_fin > ?) 
                 OR (heure_debut < ? AND heure_fin > ?)
                 OR (heure_debut >= ? AND heure_fin <= ?))
        '''
        params = [id_prof, jour, heure_fin, heure_debut, heure_fin, heure_fin,
                  heure_debut, heure_fin]
        
        if exclude_edt_id:
            query += ' AND id_edt != ?'
            params.append(exclude_edt_id)
        
        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def check_groupe_conflit(self, id_groupe: int, jour: str, heure_debut: str,
                             heure_fin: str, exclude_edt_id: int = None) -> bool:
        """Vérifier si le groupe a déjà un cours"""
        conn = self.get_connection()
        cursor = conn.cursor()
        query = '''
            SELECT COUNT(*) FROM EMPLOI_DU_TEMPS
            WHERE id_groupe = ? AND jour = ? AND actif = 1
            AND ((heure_debut < ? AND heure_fin > ?) 
                 OR (heure_debut < ? AND heure_fin > ?)
                 OR (heure_debut >= ? AND heure_fin <= ?))
        '''
        params = [id_groupe, jour, heure_fin, heure_debut, heure_fin, heure_fin,
                  heure_debut, heure_fin]
        
        if exclude_edt_id:
            query += ' AND id_edt != ?'
            params.append(exclude_edt_id)
        
        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    # ════════════════════════════════════════════════════════════════
    # MÉTHODES SUPPLÉMENTAIRES POUR COMPATIBILITÉ UI
    # ════════════════════════════════════════════════════════════════
    
    def get_schedule_by_group(self, group_id: int) -> List[Tuple]:
        """Obtenir l'emploi du temps d'un groupe"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.*, g.nom_groupe, s.nom_salle, p.nom || ' ' || p.prenom as prof_nom
            FROM EMPLOI_DU_TEMPS e
            JOIN GROUPE g ON e.id_groupe = g.id_groupe
            LEFT JOIN SALLE s ON e.id_salle = s.id_salle
            LEFT JOIN PROFESSEUR p ON e.id_prof = p.id_prof
            WHERE e.id_groupe = ? AND e.actif = 1
            ORDER BY e.jour, e.heure_debut
        ''', (group_id,))
        data = cursor.fetchall()
        conn.close()
        return data
    
    def get_revenus_mois(self, mois: str, annee: str) -> float:
        """Calculer le revenu total du mois"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(montant_paye) FROM PAIEMENT_ELEVE
            WHERE mois = ? AND annee = ?
        ''', (mois, annee))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result and result[0] else 0
    
    def get_presence_by_group_date(self, group_id: int, date: str) -> List[Tuple]:
        """Obtenir la présence pour un groupe à une date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, e.nom, e.prenom
            FROM PRESENCE p
            LEFT JOIN ELEVE e ON p.id_eleve = e.id_eleve
            WHERE p.date_seance = ?
        ''', (date,))
        data = cursor.fetchall()
        conn.close()
        return data
    
    # ════════════════════════════════════════════════════════════════
    # MÉTHODES CRUD - PAIEMENT_ELEVE
    # ════════════════════════════════════════════════════════════════
    
    def add_paiement_eleve(self, id_eleve, mois, annee, montant_du, montant_paye=0, statut='impaye'):
        """Ajouter un paiement élève"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Déterminer le statut automatiquement
            if montant_paye >= montant_du:
                statut = 'paye'
            elif montant_paye > 0:
                statut = 'partiel'
            else:
                statut = 'impaye'
            
            cursor.execute("""
                INSERT INTO PAIEMENT_ELEVE (id_eleve, mois, annee, montant_du, montant_paye, statut)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (id_eleve, mois, annee, montant_du, montant_paye, statut))
            paiement_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return paiement_id
        except sqlite3.IntegrityError as e:
            print(f"❌ Erreur d'intégrité lors de l'ajout de paiement: {e}")
            raise
        except sqlite3.Error as e:
            print(f"❌ Erreur DB lors de l'ajout de paiement: {e}")
            raise
    
    def get_all_paiements_eleve(self):
        """Obtenir tous les paiements élèves"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                p.id_paiement_eleve, 
                e.nom || ' ' || e.prenom as eleve,
                p.mois, p.annee, p.montant_du, p.montant_paye, 
                p.date_paiement, p.statut
            FROM PAIEMENT_ELEVE p
            JOIN ELEVE e ON p.id_eleve = e.id_eleve
            ORDER BY p.date_paiement DESC
        """)
        data = cursor.fetchall()
        conn.close()
        return data
    
    def get_paiement_eleve_by_id(self, paiement_id):
        """Obtenir un paiement par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PAIEMENT_ELEVE WHERE id_paiement_eleve=?", (paiement_id,))
        data = cursor.fetchone()
        conn.close()
        return data
    
    def update_paiement_eleve(self, paiement_id, montant_paye):
        """Mettre à jour un paiement élève"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Récupérer le montant dû
        cursor.execute("SELECT montant_du FROM PAIEMENT_ELEVE WHERE id_paiement_eleve=?", (paiement_id,))
        result = cursor.fetchone()
        if not result:
            conn.close()
            return
        
        montant_du = result[0]
        
        # Déterminer le statut
        if montant_paye >= montant_du:
            statut = 'paye'
        elif montant_paye > 0:
            statut = 'partiel'
        else:
            statut = 'impaye'
        
        cursor.execute("""
            UPDATE PAIEMENT_ELEVE 
            SET montant_paye=?, statut=?, updated_at=CURRENT_TIMESTAMP
            WHERE id_paiement_eleve=?
        """, (montant_paye, statut, paiement_id))
        conn.commit()
        conn.close()
    
    def delete_paiement_eleve(self, paiement_id):
        """Supprimer un paiement élève"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PAIEMENT_ELEVE WHERE id_paiement_eleve=?", (paiement_id,))
        conn.commit()
        conn.close()
    
    def search_paiements_eleve(self, query):
        """Rechercher des paiements élèves"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                p.id_paiement_eleve, 
                e.nom || ' ' || e.prenom as eleve,
                p.mois, p.annee, p.montant_du, p.montant_paye, 
                p.date_paiement, p.statut
            FROM PAIEMENT_ELEVE p
            JOIN ELEVE e ON p.id_eleve = e.id_eleve
            WHERE e.nom LIKE ? OR e.prenom LIKE ? OR p.mois LIKE ?
            ORDER BY p.date_paiement DESC
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        data = cursor.fetchall()
        conn.close()
        return data
    
    def get_revenus_mois(self, mois, annee):
        """Calculer les revenus d'un mois"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COALESCE(SUM(montant_paye), 0)
            FROM PAIEMENT_ELEVE
            WHERE mois=? AND annee=?
        """, (mois, annee))
        revenue = cursor.fetchone()[0]
        conn.close()
        return revenue
    
    # ════════════════════════════════════════════════════════════════
    # MÉTHODES CRUD - PAIEMENT_PROF (NOUVEAU!)
    # ════════════════════════════════════════════════════════════════
    
    def add_paiement_prof(self, id_prof, mois, annee, nb_heures=0, 
                          montant_du=0, montant_paye=0, statut='impaye'):
        """Ajouter un paiement professeur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Déterminer le statut
        if montant_paye >= montant_du:
            statut = 'paye'
        elif montant_paye > 0:
            statut = 'partiel'
        else:
            statut = 'impaye'
        
        cursor.execute("""
            INSERT INTO PAIEMENT_PROF (id_prof, mois, annee, nb_heures, 
                                      montant_du, montant_paye, statut)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_prof, mois, annee, nb_heures, montant_du, montant_paye, statut))
        paiement_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return paiement_id
    
    def get_all_paiements_prof(self):
        """Obtenir tous les paiements professeurs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                pp.id_paiement_prof,
                p.nom || ' ' || p.prenom as professeur,
                pp.mois, pp.annee, pp.nb_heures,
                pp.montant_du, pp.montant_paye,
                pp.date_paiement, pp.statut
            FROM PAIEMENT_PROF pp
            JOIN PROFESSEUR p ON pp.id_prof = p.id_prof
            ORDER BY pp.date_paiement DESC
        """)
        data = cursor.fetchall()
        conn.close()
        return data
    
    def calculer_montant_prof(self, id_prof, mois, annee):
        """Calculer le montant dû à un professeur pour un mois"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Récupérer les infos du prof
        cursor.execute("""
            SELECT type_paiement, salaire_mois, prix_par_heure 
            FROM PROFESSEUR 
            WHERE id_prof=?
        """, (id_prof,))
        prof = cursor.fetchone()
        
        if not prof:
            conn.close()
            return 0, 0  # montant_du, nb_heures
        
        type_paiement, salaire_mois, prix_par_heure = prof
        
        if type_paiement == 'fixe':
            # Salaire fixe
            conn.close()
            return salaire_mois, 0
        else:
            # Calcul basé sur les heures
            # Compter les séances du prof ce mois
            cursor.execute("""
                SELECT COUNT(*) * 2 as heures
                FROM EMPLOI_DU_TEMPS
                WHERE id_prof=? AND actif=1
            """, (id_prof,))
            result = cursor.fetchone()
            nb_seances = result[0] if result else 0
            
            # Approximation: 4 semaines par mois
            nb_heures = nb_seances * 4
            montant_du = nb_heures * prix_par_heure
            
            conn.close()
            return montant_du, nb_heures
    
    def update_paiement_prof(self, paiement_id, montant_paye):
        """Mettre à jour un paiement professeur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Récupérer le montant dû
        cursor.execute("""
            SELECT montant_du FROM PAIEMENT_PROF 
            WHERE id_paiement_prof=?
        """, (paiement_id,))
        result = cursor.fetchone()
        if not result:
            conn.close()
            return
        
        montant_du = result[0]
        
        # Déterminer le statut
        if montant_paye >= montant_du:
            statut = 'paye'
        elif montant_paye > 0:
            statut = 'partiel'
        else:
            statut = 'impaye'
        
        cursor.execute("""
            UPDATE PAIEMENT_PROF 
            SET montant_paye=?, statut=?, updated_at=CURRENT_TIMESTAMP
            WHERE id_paiement_prof=?
        """, (montant_paye, statut, paiement_id))
        conn.commit()
        conn.close()
    
    def delete_paiement_prof(self, paiement_id):
        """Supprimer un paiement professeur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PAIEMENT_PROF WHERE id_paiement_prof=?", (paiement_id,))
        conn.commit()
        conn.close()

# Test final
if __name__ == "__main__":
    db = DatabaseManagerV2Extended()
    print("✅ Gestionnaire de base de données V2 COMPLET chargé!")
    print("📋 Toutes les méthodes CRUD disponibles")
