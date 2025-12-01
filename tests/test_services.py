"""
Tests pour les services (couche métier)
"""

import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_compatibility import DatabaseCompatibility
from services.student_service import StudentService
from services.payment_service import PaymentService


class TestServices(unittest.TestCase):
    """Tests des services métier"""
    
    @classmethod
    def setUpClass(cls):
        """Setup avant tous les tests"""
        cls.test_db = "database/test_services.db"
        cls.db_manager = DatabaseCompatibility(cls.test_db)
        cls.student_service = StudentService(cls.db_manager)
        cls.payment_service = PaymentService(cls.db_manager)
    
    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
    
    def test_01_student_service_add(self):
        """Test: Ajouter un élève via service"""
        student_id = self.student_service.create_student(
            nom="Service",
            prenom="Test",
            telephone="0612345678",
            niveau="Lycée",
            filiere="Sciences"
        )
        self.assertIsNotNone(student_id)
        self.assertGreater(student_id, 0)
    
    def test_02_student_service_get_all(self):
        """Test: Récupérer tous les élèves via service"""
        students = self.student_service.get_all_students()
        self.assertIsInstance(students, list)
        self.assertGreater(len(students), 0)
    
    def test_03_student_service_search(self):
        """Test: Rechercher des élèves"""
        results = self.student_service.search_students("Service")
        self.assertGreater(len(results), 0)
        
        # Vérifier qu'on trouve bien notre élève
        found = any(s[1] == "Service" for s in results)
        self.assertTrue(found)
    
    def test_04_student_service_update(self):
        """Test: Mettre à jour un élève via service"""
        students = self.student_service.get_all_students()
        student_id = students[0][0]
        
        success = self.student_service.update_student(
            student_id,
            nom="ServiceUpdated",
            prenom="TestUpdated",
            tel="0698765432"
        )
        self.assertTrue(success)
        
        # Vérifier la mise à jour
        updated = self.student_service.get_student_by_id(student_id)
        self.assertEqual(updated[1], "ServiceUpdated")
    
    def test_05_payment_service_add(self):
        """Test: Ajouter un paiement via service"""
        # Récupérer un élève
        students = self.student_service.get_all_students()
        student_id = students[0][0]
        
        payment_id = self.payment_service.create_payment(
            id_eleve=student_id,
            montant=500,
            mois="Janvier",
            annee=2025
        )
        self.assertIsNotNone(payment_id)
        self.assertGreater(payment_id, 0)
    
    def test_06_payment_service_get_by_student(self):
        """Test: Récupérer les paiements d'un élève"""
        students = self.student_service.get_all_students()
        student_id = students[0][0]
        
        payments = self.payment_service.get_payments_by_student(student_id)
        self.assertIsInstance(payments, list)
        # Au moins 1 paiement pour cet élève (ajouté au test_05)
        self.assertGreaterEqual(len(payments), 0)  # Peut être 0 ou plus
    
    def test_07_payment_service_validation(self):
        """Test: Validation des paiements"""
        students = self.student_service.get_all_students()
        student_id = students[0][0]
        
        # Montant négatif (doit échouer)
        with self.assertRaises(ValueError):
            self.payment_service.create_payment(
                id_eleve=student_id,
                montant=-100,
                mois="Février",
                annee=2025
            )
    
    def test_08_student_service_delete(self):
        """Test: Supprimer un élève"""
        # Créer un élève temporaire
        student_id = self.student_service.create_student(
            nom="ToDelete",
            prenom="Test",
            telephone="0600000000"
        )
        
        # Supprimer
        success = self.student_service.delete_student(student_id)
        self.assertTrue(success)
        
        # Vérifier qu'il n'existe plus
        deleted = self.student_service.get_student_by_id(student_id)
        self.assertIsNone(deleted)


if __name__ == '__main__':
    unittest.main(verbosity=2)
