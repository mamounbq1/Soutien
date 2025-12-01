"""
Générateur de données de test réalistes
Génère des élèves, professeurs, groupes, paiements, etc.
"""

import sys
import os
import random
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_compatibility import DatabaseCompatibility


class TestDataGenerator:
    """Générateur de données de test"""
    
    NOMS = [
        "Alami", "Benali", "El Idrissi", "Chakir", "Tazi", "Bouazza",
        "Sebbata", "Lamrini", "Kabbaj", "Kadiri", "Bennani", "Fassi",
        "Alaoui", "Berrada", "Chami", "Senhaji", "Tounsi", "Lazrak"
    ]
    
    PRENOMS_M = [
        "Ahmed", "Mohamed", "Omar", "Youssef", "Karim", "Amine",
        "Mehdi", "Hamza", "Reda", "Othmane", "Saad", "Tarik"
    ]
    
    PRENOMS_F = [
        "Fatima", "Amina", "Salma", "Nada", "Imane", "Zineb",
        "Leila", "Sarah", "Khadija", "Malika", "Hind", "Samira"
    ]
    
    NIVEAUX = ["Primaire", "Collège", "Lycée", "Supérieur"]
    
    FILIERES = {
        "Primaire": ["CE1", "CE2", "CM1", "CM2"],
        "Collège": ["1AC", "2AC", "3AC"],
        "Lycée": ["1BAC Sciences", "2BAC Sciences Maths", "2BAC Sciences Physiques"],
        "Supérieur": ["Prépa", "Licence", "Master"]
    }
    
    MATIERES = [
        ("Mathématiques", "Maths pour tous niveaux", 500),
        ("Physique-Chimie", "Sciences physiques", 450),
        ("SVT", "Sciences de la Vie et de la Terre", 400),
        ("Français", "Langue française et littérature", 350),
        ("Anglais", "Langue anglaise", 350),
        ("Arabe", "Langue arabe", 300),
        ("Informatique", "Programmation et bureautique", 600),
        ("Histoire-Géo", "Sciences humaines", 350),
        ("Philosophie", "Réflexion philosophique", 400),
        ("Économie", "Sciences économiques", 450)
    ]
    
    SALLES = [
        ("Salle A1", 20, "Tableau blanc, projecteur"),
        ("Salle A2", 15, "Ordinateurs, tableau interactif"),
        ("Salle B1", 25, "Tableau blanc"),
        ("Salle B2", 12, "Labo chimie, paillasses"),
        ("Salle C1", 30, "Grande salle, projecteur"),
        ("Salle C2", 10, "Salle individuelle"),
    ]
    
    def __init__(self, db_path: str = "database/app.db"):
        self.db = DatabaseCompatibility(db_path)
    
    def generate_phone(self):
        """Générer un numéro de téléphone marocain"""
        prefixes = ["61", "62", "66", "67", "68", "69"]
        number = random.randint(1000000, 9999999)
        return f"0{random.choice(prefixes)}{number}"
    
    def generate_students(self, count: int = 50):
        """Générer des élèves"""
        print(f"📝 Génération de {count} élèves...")
        
        for i in range(count):
            nom = random.choice(self.NOMS)
            is_male = random.choice([True, False])
            prenom = random.choice(self.PRENOMS_M if is_male else self.PRENOMS_F)
            
            niveau = random.choice(self.NIVEAUX)
            filiere = random.choice(self.FILIERES[niveau])
            
            telephone = self.generate_phone()
            tel_parents = self.generate_phone()
            
            try:
                self.db.add_student(
                    nom=nom,
                    prenom=prenom,
                    niveau=niveau,
                    filiere=filiere,
                    tel=telephone,
                    parent_tel=tel_parents
                )
            except Exception as e:
                print(f"❌ Erreur élève {i+1}: {e}")
        
        print(f"✅ {count} élèves générés")
    
    def generate_teachers(self, count: int = 15):
        """Générer des professeurs"""
        print(f"👨‍🏫 Génération de {count} professeurs...")
        
        # D'abord créer les matières
        matiere_ids = {}
        for nom, desc, tarif in self.MATIERES:
            try:
                mat_id = self.db.add_subject(
                    nom=nom,
                    description=desc,
                    tarif_mensuel=tarif
                )
                matiere_ids[nom] = mat_id
            except Exception as e:
                print(f"⚠️  Matière '{nom}' déjà existante ou erreur: {e}")
                # Récupérer l'ID existant
                try:
                    matieres = self.db.get_subjects()
                    for m in matieres:
                        if m[1] == nom:  # m[1] = nom_matiere
                            matiere_ids[nom] = m[0]
                            break
                except:
                    pass
        
        # Ensuite les profs
        for i in range(count):
            nom = random.choice(self.NOMS)
            is_male = random.choice([True, False])
            prenom = random.choice(self.PRENOMS_M if is_male else self.PRENOMS_F)
            
            # Vérifier qu'on a des matières
            if not matiere_ids:
                print("❌ Aucune matière disponible, impossible de créer des profs")
                return
            
            matiere = random.choice(list(matiere_ids.keys()))
            telephone = self.generate_phone()
            salaire_h = random.choice([100, 120, 150, 180, 200, 250])
            
            try:
                self.db.add_teacher(
                    nom=nom,
                    prenom=prenom,
                    matiere=matiere,
                    tel=telephone,
                    salaire_horaire=salaire_h
                )
            except Exception as e:
                print(f"❌ Erreur prof {i+1}: {e}")
        
        print(f"✅ {count} professeurs générés")
    
    def generate_rooms(self):
        """Générer des salles"""
        print(f"🏫 Génération des salles...")
        
        for nom, capacite, equipement in self.SALLES:
            try:
                self.db.add_salle(
                    nom_salle=nom,
                    capacite=capacite,
                    equipement=equipement
                )
            except Exception as e:
                # Salle déjà existante
                pass
        
        print(f"✅ {len(self.SALLES)} salles générées")
    
    def generate_groups(self, count: int = 20):
        """Générer des groupes"""
        print(f"👥 Génération de {count} groupes...")
        
        # Récupérer profs, matières, salles
        profs = self.db.get_all_professeurs()
        matieres = self.db.get_all_matieres()
        salles = self.db.get_all_salles()
        
        if not profs or not matieres:
            print("❌ Impossible de générer des groupes (pas de profs/matières)")
            return
        
        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
        heures = ["08:00", "10:00", "14:00", "16:00"]
        
        for i in range(count):
            prof = random.choice(profs)
            matiere = random.choice(matieres)
            salle = random.choice(salles) if salles else None
            
            niveau = random.choice(self.NIVEAUX)
            jour = random.choice(jours)
            heure = random.choice(heures)
            
            nom_groupe = f"{matiere[1][:4]}-{niveau[:3]}-{i+1}"
            
            try:
                self.db.add_group(
                    nom=nom_groupe,
                    matiere_id=matiere[0],
                    niveau=niveau
                )
            except Exception as e:
                print(f"❌ Erreur groupe {i+1}: {e}")
        
        print(f"✅ {count} groupes générés")
    
    def generate_payments(self, count: int = 100):
        """Générer des paiements"""
        print(f"💰 Génération de {count} paiements...")
        
        eleves = self.db.get_all_eleves()
        if not eleves:
            print("❌ Pas d'élèves pour générer des paiements")
            return
        
        mois = ["Septembre", "Octobre", "Novembre", "Décembre", "Janvier"]
        annee = datetime.now().year
        
        for i in range(count):
            eleve = random.choice(eleves)
            montant = random.choice([400, 500, 600, 700, 800])
            mois_paiement = random.choice(mois)
            
            try:
                self.db.add_paiement_eleve(
                    id_eleve=eleve[0],
                    montant_du=montant,
                    montant_paye=montant,
                    mois=mois_paiement,
                    annee=annee
                )
            except Exception as e:
                print(f"❌ Erreur paiement {i+1}: {e}")
        
        print(f"✅ {count} paiements générés")
    
    def generate_all(self):
        """Générer toutes les données"""
        print("\n" + "="*60)
        print("🚀 GÉNÉRATION COMPLÈTE DES DONNÉES DE TEST")
        print("="*60 + "\n")
        
        self.generate_rooms()
        self.generate_teachers(15)
        self.generate_students(50)
        self.generate_groups(20)
        self.generate_payments(100)
        
        print("\n" + "="*60)
        print("✅ GÉNÉRATION TERMINÉE")
        print("="*60 + "\n")


if __name__ == '__main__':
    generator = TestDataGenerator()
    generator.generate_all()
