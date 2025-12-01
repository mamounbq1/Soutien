"""
Tests unitaires pour les opérations de base de données
"""

import unittest
import sys
import os
import tempfile

# Ajouter le chemin parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager_v2 import DatabaseManagerV2
from database.db_compatibility import DatabaseCompatibility


class TestDatabaseManager(unittest.TestCase):
    """Tests pour le gestionnaire de base de données"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        # Créer une base de données temporaire pour les tests
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        # Supprimer le fichier pour forcer la création des tables
        os.unlink(self.temp_db.name)
        self.db = DatabaseManagerV2(self.temp_db.name)
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_add_eleve(self):
        """Test ajout d'un élève"""
        eleve_id = self.db.add_eleve("Alami", "Ahmed", "0612345678")
        self.assertIsNotNone(eleve_id)
        self.assertGreater(eleve_id, 0)
    
    def test_get_all_eleves(self):
        """Test récupération de tous les élèves"""
        # Ajouter quelques élèves
        self.db.add_eleve("Alami", "Ahmed")
        self.db.add_eleve("Benali", "Fatima")
        
        # Récupérer tous les élèves
        eleves = self.db.get_all_eleves()
        self.assertEqual(len(eleves), 2)
    
    def test_search_eleves(self):
        """Test recherche d'élèves"""
        self.db.add_eleve("Alami", "Ahmed")
        self.db.add_eleve("Benali", "Fatima")
        
        # Rechercher par nom
        results = self.db.search_eleves("Alami")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Alami")
    
    def test_update_eleve(self):
        """Test mise à jour d'un élève"""
        eleve_id = self.db.add_eleve("Alami", "Ahmed")
        self.db.update_eleve(eleve_id, "Alami", "Mohamed", "0612345678")
        
        eleve = self.db.get_eleve_by_id(eleve_id)
        self.assertEqual(eleve[2], "Mohamed")
    
    def test_delete_eleve(self):
        """Test suppression d'un élève"""
        eleve_id = self.db.add_eleve("Alami", "Ahmed")
        self.db.delete_eleve(eleve_id)
        
        eleve = self.db.get_eleve_by_id(eleve_id)
        self.assertIsNone(eleve)
    
    def test_add_professeur(self):
        """Test ajout d'un professeur"""
        prof_id = self.db.add_professeur("Idrissi", "Karim", "0698765432", "Mathématiques")
        self.assertIsNotNone(prof_id)
        self.assertGreater(prof_id, 0)


class TestDatabaseCompatibility(unittest.TestCase):
    """Tests pour l'adaptateur de compatibilité"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        # Supprimer le fichier pour forcer la création des tables
        os.unlink(self.temp_db.name)
        self.db = DatabaseCompatibility(self.temp_db.name)
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_validate_telephone(self):
        """Test validation numéro de téléphone"""
        self.assertTrue(self.db._validate_telephone("0612345678"))
        self.assertTrue(self.db._validate_telephone("+212612345678"))
        self.assertFalse(self.db._validate_telephone("123"))
        self.assertFalse(self.db._validate_telephone("abcdefghij"))
    
    def test_validate_montant(self):
        """Test validation montant"""
        self.assertTrue(self.db._validate_montant(100))
        self.assertTrue(self.db._validate_montant(0))
        self.assertFalse(self.db._validate_montant(-50))
        self.assertFalse(self.db._validate_montant("abc"))
    
    def test_add_student_with_validation(self):
        """Test ajout élève avec validation"""
        # Doit réussir
        student_id = self.db.add_student("Alami", "Ahmed", "Lycée", "1ère Bac", "0612345678")
        self.assertIsNotNone(student_id)
        
        # Doit échouer (téléphone invalide)
        with self.assertRaises(ValueError):
            self.db.add_student("Benali", "Fatima", "Lycée", "1ère Bac", "123")
    
    def test_add_payment_with_validation(self):
        """Test ajout paiement avec validation"""
        # Ajouter un élève d'abord
        student_id = self.db.add_student("Alami", "Ahmed")
        
        # Doit réussir
        payment_id = self.db.add_payment(student_id, 500, "Janvier", "2024")
        self.assertIsNotNone(payment_id)
        
        # Doit échouer (montant négatif)
        with self.assertRaises(ValueError):
            self.db.add_payment(student_id, -100, "Février", "2024")


class TestUtilsFunctions(unittest.TestCase):
    """Tests pour les fonctions utilitaires"""
    
    def test_validate_phone_number(self):
        """Test validation numéro de téléphone"""
        from utils import validate_phone_number
        
        self.assertTrue(validate_phone_number("0612345678"))
        self.assertTrue(validate_phone_number("+212612345678"))
        self.assertFalse(validate_phone_number("123"))
        self.assertTrue(validate_phone_number(""))  # Optionnel
    
    def test_validate_amount(self):
        """Test validation montant"""
        from utils import validate_amount
        
        self.assertTrue(validate_amount(100))
        self.assertTrue(validate_amount(0))
        self.assertFalse(validate_amount(-50))
        self.assertFalse(validate_amount("abc"))


if __name__ == '__main__':
    unittest.main()
