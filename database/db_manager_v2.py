"""
DATABASE MANAGER V2 - Nouveau Modèle
=====================================
Conforme aux spécifications du modèle souhaité avec:
- Tables restructurées (ELEVE, PROFESSEUR, GROUPE, etc.)
- Clés étrangères optimisées
- Support des paiements professeurs
- Calcul automatique des heures
- Gestion avancée des groupes et emploi du temps
"""

import sqlite3
import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Tuple, Dict

class DatabaseManagerV2:
    """Gestionnaire de base de données - Version 2 (Modèle optimisé)"""
    
    def __init__(self, db_name="database/app.db"):
        self.db_name = db_name
        self.check_db_exists()
    
    def _hash_password(self, password: str) -> str:
        """Hash un mot de passe avec SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def check_db_exists(self):
        """Vérifie et crée la structure si nécessaire"""
        if not os.path.exists(os.path.dirname(self.db_name)):
            os.makedirs(os.path.dirname(self.db_name))
        
        if not os.path.exists(self.db_name):
            self.create_tables_v2()

    def get_connection(self):
        """Obtenir une connexion à la base de données"""
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON")  # Activer les clés étrangères
        return conn

    def create_tables_v2(self):
        """Créer toutes les tables selon le nouveau modèle"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # ═══════════════════════════════════════════════════════════
        # TABLE ELEVE (Nouveau modèle)
        # ═══════════════════════════════════════════════════════════
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ELEVE (
            id_eleve INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            filiere TEXT,
            classe TEXT,
            telephone TEXT,
            adresse TEXT,
            date_naissance DATE,
            date_inscription DATE DEFAULT (datetime('now','localtime')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # ═══════════════════════════════════════════════════════════
        # TABLE PROFESSEUR (Nouveau modèle avec type de paiement)
        # ═══════════════════════════════════════════════════════════
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PROFESSEUR (
            id_prof INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            telephone TEXT,
            specialite TEXT,
            salaire_mois REAL DEFAULT 0,
            prix_par_heure REAL DEFAULT 0,
            tarif_par_eleve REAL DEFAULT 0,
            type_paiement TEXT DEFAULT 'heure' CHECK(type_paiement IN ('fixe', 'heure', 'eleve')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # ═══════════════════════════════════════════════════════════
        # TABLE MATIERE
        # ═══════════════════════════════════════════════════════════
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS MATIERE (
            id_matiere INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_matiere TEXT NOT NULL UNIQUE,
            description TEXT,
            tarif_mensuel REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # ═══════════════════════════════════════════════════════════
        # TABLE SALLE
        # ═══════════════════════════════════════════════════════════
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS SALLE (
            id_salle INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_salle TEXT NOT NULL UNIQUE,
            capacite INTEGER NOT NULL,
            equipement TEXT,
            disponible BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # ═══════════════════════════════════════════════════════════
        # TABLE GROUPE (Cours individuels ou collectifs)
        # - type_groupe: 'INDIVIDUEL' (1 élève) ou 'COLLECTIF' (plusieurs)
        # - capacite_max: Nombre max d'élèves (NULL pour individuel)
        # ═══════════════════════════════════════════════════════════
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS GROUPE (
            id_groupe INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_groupe TEXT NOT NULL UNIQUE,
            type_groupe TEXT DEFAULT 'COLLECTIF' CHECK(type_groupe IN ('INDIVIDUEL', 'COLLECTIF')),
            capacite_max INTEGER,
            id_prof INTEGER,
            id_matiere INTEGER NOT NULL,
            id_salle INTEGER,
            niveau TEXT,
            jour TEXT,
            heure_debut TEXT,
            heure_fin TEXT,
            actif BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_prof) REFERENCES PROFESSEUR(id_prof) ON DELETE SET NULL,
            FOREIGN KEY(id_matiere) REFERENCES MATIERE(id_matiere) ON DELETE RESTRICT,
            FOREIGN KEY(id_salle) REFERENCES SALLE(id_salle) ON DELETE SET NULL
        )
        ''')

        # ═══════════════════════════════════════════════════════════
        # TABLE INSCRIPTION (Relation Élève-Groupe avec mensualité)
        # ═══════════════════════════════════════════════════════════
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS INSCRIPTION (
            id_inscription INTEGER PRIMARY KEY AUTOINCREMENT,
            id_eleve INTEGER NOT NULL,
            id_groupe INTEGER NOT NULL,
            date_inscription DATE DEFAULT (datetime('now','localtime')),
            mensualite REAL DEFAULT 0,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_eleve) REFERENCES ELEVE(id_eleve) ON DELETE CASCADE,
            FOREIGN KEY(id_groupe) REFERENCES GROUPE(id_groupe) ON DELETE CASCADE,
            UNIQUE(id_eleve, id_groupe)
        )
        ''')

        # ═══════════════════════════════════════════════════════════
        # TABLE PAIEMENT_ELEVE (Nouveau modèle avec statut)
        # ═══════════════════════════════════════════════════════════
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PAIEMENT_ELEVE (
            id_paiement_eleve INTEGER PRIMARY KEY AUTOINCREMENT,
            id_eleve INTEGER NOT NULL,
            mois TEXT NOT NULL,
            annee TEXT NOT NULL,
            montant_du REAL NOT NULL,
            montant_paye REAL DEFAULT 0,
            date_paiement DATE DEFAULT (datetime('now','localtime')),
            statut TEXT DEFAULT 'impaye' CHECK(statut IN ('paye', 'impaye', 'partiel')),
            remarque TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_eleve) REFERENCES ELEVE(id_eleve) ON DELETE CASCADE
        )
        ''')

        # ═══════════════════════════════════════════════════════════
        # TABLE PAIEMENT_PROF (NOUVEAU - Gestion paiements professeurs)
        # ═══════════════════════════════════════════════════════════
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PAIEMENT_PROF (
            id_paiement_prof INTEGER PRIMARY KEY AUTOINCREMENT,
            id_prof INTEGER NOT NULL,
            mois TEXT NOT NULL,
            annee TEXT NOT NULL,
            nb_heures REAL DEFAULT 0,
            montant_du REAL NOT NULL,
            montant_paye REAL DEFAULT 0,
            date_paiement DATE DEFAULT (datetime('now','localtime')),
            statut TEXT DEFAULT 'impaye' CHECK(statut IN ('paye', 'impaye', 'partiel')),
            remarque TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_prof) REFERENCES PROFESSEUR(id_prof) ON DELETE CASCADE,
            UNIQUE(id_prof, mois, annee)
        )
        ''')

        # ═══════════════════════════════════════════════════════════
        # TABLE EMPLOI_DU_TEMPS (Distinct du GROUPE)
        # ═══════════════════════════════════════════════════════════
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS EMPLOI_DU_TEMPS (
            id_edt INTEGER PRIMARY KEY AUTOINCREMENT,
            id_groupe INTEGER NOT NULL,
            jour TEXT NOT NULL,
            heure_debut TEXT NOT NULL,
            heure_fin TEXT NOT NULL,
            id_salle INTEGER,
            id_prof INTEGER,
            periode TEXT,
            actif BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_groupe) REFERENCES GROUPE(id_groupe) ON DELETE CASCADE,
            FOREIGN KEY(id_salle) REFERENCES SALLE(id_salle) ON DELETE SET NULL,
            FOREIGN KEY(id_prof) REFERENCES PROFESSEUR(id_prof) ON DELETE SET NULL
        )
        ''')

        # ═══════════════════════════════════════════════════════════
        # TABLE PRESENCE (Suivi des présences)
        # ═══════════════════════════════════════════════════════════
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PRESENCE (
            id_presence INTEGER PRIMARY KEY AUTOINCREMENT,
            id_edt INTEGER NOT NULL,
            id_eleve INTEGER NOT NULL,
            date_seance DATE NOT NULL,
            statut TEXT DEFAULT 'present' CHECK(statut IN ('present', 'absent', 'retard', 'justifie')),
            remarque TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_edt) REFERENCES EMPLOI_DU_TEMPS(id_edt) ON DELETE CASCADE,
            FOREIGN KEY(id_eleve) REFERENCES ELEVE(id_eleve) ON DELETE CASCADE,
            UNIQUE(id_edt, id_eleve, date_seance)
        )
        ''')

        # ═══════════════════════════════════════════════════════════
        # TABLE USERS (Authentification)
        # ═══════════════════════════════════════════════════════════
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Insert default admin if not exists
        cursor.execute("SELECT * FROM USERS WHERE username='admin'")
        if not cursor.fetchone():
            hashed_password = self._hash_password('admin123')
            cursor.execute("INSERT INTO USERS (username, password, role) VALUES ('admin', ?, 'admin')", (hashed_password,))

        # Créer des index pour optimiser les performances
        self._create_indexes(cursor)

        conn.commit()
        conn.close()
        print("✅ Base de données V2 initialisée avec succès!")

    def _create_indexes(self, cursor):
        """Créer des index pour optimiser les requêtes"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_eleve_nom ON ELEVE(nom, prenom)",
            "CREATE INDEX IF NOT EXISTS idx_prof_nom ON PROFESSEUR(nom, prenom)",
            "CREATE INDEX IF NOT EXISTS idx_inscription_eleve ON INSCRIPTION(id_eleve)",
            "CREATE INDEX IF NOT EXISTS idx_inscription_groupe ON INSCRIPTION(id_groupe)",
            "CREATE INDEX IF NOT EXISTS idx_paiement_eleve ON PAIEMENT_ELEVE(id_eleve, mois, annee)",
            "CREATE INDEX IF NOT EXISTS idx_paiement_prof ON PAIEMENT_PROF(id_prof, mois, annee)",
            "CREATE INDEX IF NOT EXISTS idx_edt_groupe ON EMPLOI_DU_TEMPS(id_groupe)",
            "CREATE INDEX IF NOT EXISTS idx_edt_jour ON EMPLOI_DU_TEMPS(jour, heure_debut)",
            "CREATE INDEX IF NOT EXISTS idx_presence_date ON PRESENCE(date_seance)",
        ]
        for index_sql in indexes:
            cursor.execute(index_sql)
    
    def check_foreign_keys(self) -> List[Tuple]:
        """
        Vérifier l'intégrité des contraintes de clés étrangères
        
        Returns:
            Liste des violations (vide si tout est OK)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_key_check")
        violations = cursor.fetchall()
        conn.close()
        return violations

    # ════════════════════════════════════════════════════════════════
    # MÉTHODES CRUD - ELEVE
    # ════════════════════════════════════════════════════════════════
    
    def add_eleve(self, nom: str, prenom: str, filiere: str = None, classe: str = None,
                  telephone: str = None, adresse: str = None, date_naissance: str = None) -> int:
        """Ajouter un élève"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ELEVE (nom, prenom, filiere, classe, telephone, adresse, date_naissance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nom, prenom, filiere, classe, telephone, adresse, date_naissance))
            eleve_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return eleve_id
        except sqlite3.IntegrityError as e:
            print(f"❌ Erreur d'intégrité lors de l'ajout d'élève: {e}")
            raise
        except sqlite3.Error as e:
            print(f"❌ Erreur DB lors de l'ajout d'élève: {e}")
            raise

    def get_all_eleves(self, limit: int = None, offset: int = 0) -> List[Tuple]:
        """
        Obtenir tous les élèves de la base de données
        
        Args:
            limit: Nombre maximum d'élèves à retourner (None = tous)
            offset: Nombre d'élèves à sauter (pour pagination)
        
        Returns:
            List[Tuple]: Liste de tuples contenant les informations des élèves
                Format: (id_eleve, nom, prenom, telephone, adresse, date_naissance, 
                        date_inscription, created_at, updated_at)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM ELEVE ORDER BY nom, prenom'
        if limit is not None:
            query += f' LIMIT {limit} OFFSET {offset}'
        
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data

    def get_eleve_by_id(self, eleve_id: int) -> Optional[Tuple]:
        """Obtenir un élève par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ELEVE WHERE id_eleve=?', (eleve_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_eleve(self, eleve_id: int, nom: str, prenom: str, filiere: str = None,
                     classe: str = None, telephone: str = None, adresse: str = None, 
                     date_naissance: str = None):
        """
        Mettre à jour les informations d'un élève
        
        Args:
            eleve_id: ID de l'élève à mettre à jour
            nom: Nouveau nom
            prenom: Nouveau prénom
            filiere: Filière (optionnel)
            classe: Classe (optionnel)
            telephone: Nouveau numéro de téléphone (optionnel)
            adresse: Nouvelle adresse (optionnel)
            date_naissance: Nouvelle date de naissance format YYYY-MM-DD (optionnel)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE ELEVE 
            SET nom=?, prenom=?, filiere=?, classe=?, telephone=?, adresse=?, date_naissance=?, 
                updated_at=CURRENT_TIMESTAMP
            WHERE id_eleve=?
        ''', (nom, prenom, filiere, classe, telephone, adresse, date_naissance, eleve_id))
        conn.commit()
        conn.close()

    def delete_eleve(self, eleve_id: int):
        """Supprimer un élève (CASCADE sur inscriptions et paiements)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM ELEVE WHERE id_eleve=?', (eleve_id,))
        conn.commit()
        conn.close()

    def search_eleves(self, query: str) -> List[Tuple]:
        """Rechercher des élèves"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM ELEVE 
            WHERE nom LIKE ? OR prenom LIKE ? OR telephone LIKE ?
            ORDER BY nom, prenom
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        data = cursor.fetchall()
        conn.close()
        return data

    # ════════════════════════════════════════════════════════════════
    # MÉTHODES CRUD - PROFESSEUR
    # ════════════════════════════════════════════════════════════════
    
    def add_professeur(self, nom: str, prenom: str, telephone: str = None,
                       specialite: str = None, salaire_mois: float = 0,
                       prix_par_heure: float = 0, type_paiement: str = 'heure') -> int:
        """Ajouter un professeur"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO PROFESSEUR (nom, prenom, telephone, specialite, 
                                       salaire_mois, prix_par_heure, type_paiement)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nom, prenom, telephone, specialite, salaire_mois, prix_par_heure, type_paiement))
            prof_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return prof_id
        except sqlite3.IntegrityError as e:
            print(f"❌ Erreur d'intégrité lors de l'ajout de professeur: {e}")
            raise
        except sqlite3.Error as e:
            print(f"❌ Erreur DB lors de l'ajout de professeur: {e}")
            raise

    def get_all_professeurs(self, limit: int = None, offset: int = 0) -> List[Tuple]:
        """
        Obtenir tous les professeurs de la base de données
        
        Args:
            limit: Nombre maximum de professeurs à retourner (None = tous)
            offset: Nombre de professeurs à sauter (pour pagination)
        
        Returns:
            List[Tuple]: Liste de tuples contenant les informations des professeurs
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM PROFESSEUR ORDER BY nom, prenom'
        if limit is not None:
            query += f' LIMIT {limit} OFFSET {offset}'
        
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data

    def get_professeur_by_id(self, prof_id: int) -> Optional[Tuple]:
        """Obtenir un professeur par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM PROFESSEUR WHERE id_prof=?', (prof_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_professeur(self, prof_id: int, nom: str, prenom: str, telephone: str = None,
                          specialite: str = None, salaire_mois: float = 0,
                          prix_par_heure: float = 0, type_paiement: str = 'heure'):
        """Mettre à jour un professeur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE PROFESSEUR 
            SET nom=?, prenom=?, telephone=?, specialite=?, 
                salaire_mois=?, prix_par_heure=?, type_paiement=?,
                updated_at=CURRENT_TIMESTAMP
            WHERE id_prof=?
        ''', (nom, prenom, telephone, specialite, salaire_mois, prix_par_heure, type_paiement, prof_id))
        conn.commit()
        conn.close()

    def delete_professeur(self, prof_id: int):
        """Supprimer un professeur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM PROFESSEUR WHERE id_prof=?', (prof_id,))
        conn.commit()
        conn.close()

    def search_professeurs(self, query: str) -> List[Tuple]:
        """Rechercher des professeurs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM PROFESSEUR 
            WHERE nom LIKE ? OR prenom LIKE ? OR specialite LIKE ?
            ORDER BY nom, prenom
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        data = cursor.fetchall()
        conn.close()
        return data

    # ════════════════════════════════════════════════════════════════
    # Méthodes supplémentaires dans le prochain fichier...
    # ════════════════════════════════════════════════════════════════

    # ==================== NIVEAU METHODS ====================
    
    def get_all_niveaux(self, actif_only=True):
        """Récupérer tous les niveaux"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if actif_only:
                cursor.execute("SELECT id_niveau, nom_niveau, ordre FROM NIVEAU WHERE actif=1 ORDER BY ordre")
            else:
                cursor.execute("SELECT id_niveau, nom_niveau, ordre, actif FROM NIVEAU ORDER BY ordre")
            niveaux = cursor.fetchall()
            conn.close()
            return niveaux
        except Exception as e:
            print(f"❌ Erreur get_all_niveaux: {e}")
            return []
    
    def add_niveau(self, nom_niveau: str, ordre: int = 999):
        """Ajouter un niveau"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO NIVEAU (nom_niveau, ordre) VALUES (?, ?)",
                (nom_niveau, ordre)
            )
            niveau_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return niveau_id
        except sqlite3.IntegrityError:
            print(f"❌ Le niveau '{nom_niveau}' existe déjà")
            return None
        except Exception as e:
            print(f"❌ Erreur add_niveau: {e}")
            return None
    
    def update_niveau(self, id_niveau: int, nom_niveau: str, ordre: int = None):
        """Mettre à jour un niveau"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if ordre is not None:
                cursor.execute(
                    "UPDATE NIVEAU SET nom_niveau=?, ordre=? WHERE id_niveau=?",
                    (nom_niveau, ordre, id_niveau)
                )
            else:
                cursor.execute(
                    "UPDATE NIVEAU SET nom_niveau=? WHERE id_niveau=?",
                    (nom_niveau, id_niveau)
                )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Erreur update_niveau: {e}")
            return False
    
    def delete_niveau(self, id_niveau: int):
        """Supprimer un niveau (soft delete - désactiver)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE NIVEAU SET actif=0 WHERE id_niveau=?", (id_niveau,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Erreur delete_niveau: {e}")
            return False

# Quick test
if __name__ == "__main__":
    db = DatabaseManagerV2()
    print("✅ Nouvelle base de données V2 créée!")
    print("📋 Tables créées avec succès selon le nouveau modèle")

