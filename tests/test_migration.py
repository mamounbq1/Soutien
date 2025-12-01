"""
Tests pour valider la migration V1 → V2
"""

import unittest
import os
import sqlite3
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager_v2 import DatabaseManagerV2


class TestMigration(unittest.TestCase):
    """Tests de migration et compatibilité DB"""
    
    @classmethod
    def setUpClass(cls):
        """Setup avant tous les tests"""
        cls.test_db = "database/test_migration.db"
        cls.db_manager = DatabaseManagerV2(cls.test_db)
    
    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
    
    def test_01_v2_structure_creation(self):
        """Test: Création de la structure V2"""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        # Vérifier les tables créées
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        
        required_tables = [
            'ELEVE', 'PROFESSEUR', 'MATIERE', 'SALLE', 'GROUPE',
            'INSCRIPTION', 'EMPLOI_DU_TEMPS', 'PAIEMENT_ELEVE',
            'PAIEMENT_PROF', 'PRESENCE', 'USERS'
        ]
        
        for table in required_tables:
            self.assertIn(table, tables, f"Table {table} manquante")
        
        conn.close()
    
    def test_02_foreign_keys_enabled(self):
        """Test: Vérifier que les clés étrangères sont activées"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys")
        fk_status = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(fk_status, 1, "Foreign keys non activées")
    
    def test_03_foreign_key_integrity(self):
        """Test: Vérifier l'intégrité des FK"""
        violations = self.db_manager.check_foreign_keys()
        self.assertEqual(len(violations), 0, f"Violations FK détectées: {violations}")
    
    def test_04_groupe_type_constraint(self):
        """Test: Contrainte CHECK sur type_groupe"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        # Ajouter une matière d'abord
        cursor.execute("INSERT INTO MATIERE (nom_matiere, tarif_mensuel) VALUES ('Math Test', 500)")
        matiere_id = cursor.lastrowid
        
        # Tester type valide
        cursor.execute("""
            INSERT INTO GROUPE (nom_groupe, type_groupe, id_matiere)
            VALUES ('Test Groupe', 'INDIVIDUEL', ?)
        """, (matiere_id,))
        conn.commit()
        
        # Tester type invalide (doit échouer)
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO GROUPE (nom_groupe, type_groupe, id_matiere)
                VALUES ('Test Invalide', 'AUTRE', ?)
            """, (matiere_id,))
            conn.commit()
        
        conn.close()
    
    def test_05_cascade_delete_protection(self):
        """Test: Protection CASCADE sur suppressions critiques"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        # Créer une matière avec groupe
        cursor.execute("INSERT INTO MATIERE (nom_matiere, tarif_mensuel) VALUES ('Physique', 400)")
        matiere_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO GROUPE (nom_groupe, id_matiere, type_groupe)
            VALUES ('Groupe Physique', ?, 'COLLECTIF')
        """, (matiere_id,))
        conn.commit()
        
        # Tenter de supprimer la matière (doit échouer car RESTRICT)
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("DELETE FROM MATIERE WHERE id_matiere=?", (matiere_id,))
            conn.commit()
        
        conn.close()
    
    def test_06_indexes_created(self):
        """Test: Vérifier que les index sont créés"""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [i[0] for i in cursor.fetchall()]
        
        required_indexes = [
            'idx_eleve_nom', 'idx_prof_nom', 'idx_inscription_eleve',
            'idx_paiement_eleve', 'idx_edt_groupe'
        ]
        
        for index in required_indexes:
            self.assertIn(index, indexes, f"Index {index} manquant")
        
        conn.close()
    
    def test_07_password_hashing(self):
        """Test: Vérifier que les mots de passe sont hashés"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT password FROM USERS WHERE username='admin'")
        password = cursor.fetchone()[0]
        conn.close()
        
        # Le mot de passe ne doit pas être en clair
        self.assertNotEqual(password, 'admin123', "Mot de passe en clair!")
        self.assertGreater(len(password), 20, "Hash trop court")
    
    def test_08_data_consistency(self):
        """Test: Cohérence des données après insertions"""
        # Ajouter élève
        eleve_id = self.db_manager.add_eleve("Test", "Élève", "0612345678")
        
        # Ajouter professeur
        prof_id = self.db_manager.add_professeur("Test", "Prof", "0698765432", "Math", 200)
        
        # Vérifier que les IDs sont valides
        self.assertIsNotNone(eleve_id)
        self.assertIsNotNone(prof_id)
        
        # Vérifier la récupération
        eleves = self.db_manager.get_all_eleves()
        profs = self.db_manager.get_all_professeurs()
        
        self.assertGreater(len(eleves), 0)
        self.assertGreater(len(profs), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
