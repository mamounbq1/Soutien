"""
SCRIPT DE MIGRATION V1 → V2
============================
Ce script migre automatiquement les données de l'ancienne structure vers le nouveau modèle.

ATTENTION: Créer un backup avant d'exécuter!
"""

import sqlite3
import os
import sys
import shutil
from datetime import datetime
from typing import Dict, List, Tuple

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DatabaseMigration:
    """Gestionnaire de migration de base de données"""
    
    def __init__(self, old_db="database/app.db", new_db="database/app_v2.db"):
        self.old_db = old_db
        self.new_db = new_db
        self.backup_dir = "database/backups"
        self.migration_log = []
        
    def log(self, message: str):
        """Logger les actions"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        self.migration_log.append(log_msg)
        print(log_msg)
    
    def create_backup(self):
        """Créer un backup de l'ancienne base"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{self.backup_dir}/app_backup_{timestamp}.db"
        
        if os.path.exists(self.old_db):
            shutil.copy2(self.old_db, backup_file)
            self.log(f"✅ Backup créé: {backup_file}")
            return backup_file
        else:
            self.log("⚠️ Ancienne base de données non trouvée")
            return None
    
    def migrate(self):
        """Processus complet de migration"""
        self.log("=" * 60)
        self.log("DÉBUT DE LA MIGRATION V1 → V2")
        self.log("=" * 60)
        
        # Étape 1: Backup
        self.log("\n📦 ÉTAPE 1: Création du backup...")
        backup_file = self.create_backup()
        if not backup_file:
            self.log("❌ Impossible de créer le backup. Migration annulée.")
            return False
        
        # Étape 2: Créer nouvelle structure
        self.log("\n🏗️ ÉTAPE 2: Création de la nouvelle structure...")
        from database.db_manager_v2 import DatabaseManagerV2
        db_v2 = DatabaseManagerV2(self.new_db)
        self.log("✅ Nouvelle structure créée")
        
        # Étape 3: Migrer les données
        self.log("\n🔄 ÉTAPE 3: Migration des données...")
        
        try:
            conn_old = sqlite3.connect(self.old_db)
            conn_new = sqlite3.connect(self.new_db)
            
            # 3.1 Migrer MATIERE (subjects → MATIERE)
            self.log("\n  📚 Migration MATIERE...")
            self._migrate_subjects(conn_old, conn_new)
            
            # 3.2 Migrer SALLE (rooms → SALLE)
            self.log("\n  🏫 Migration SALLE...")
            self._migrate_rooms(conn_old, conn_new)
            
            # 3.3 Migrer PROFESSEUR (teachers → PROFESSEUR)
            self.log("\n  👨‍🏫 Migration PROFESSEUR...")
            self._migrate_teachers(conn_old, conn_new)
            
            # 3.4 Migrer ELEVE (students → ELEVE)
            self.log("\n  👨‍🎓 Migration ELEVE...")
            self._migrate_students(conn_old, conn_new)
            
            # 3.5 Migrer GROUPE (groups → GROUPE)
            self.log("\n  👥 Migration GROUPE...")
            self._migrate_groups(conn_old, conn_new)
            
            # 3.6 Migrer INSCRIPTION (inscriptions → INSCRIPTION)
            self.log("\n  📝 Migration INSCRIPTION...")
            self._migrate_inscriptions(conn_old, conn_new)
            
            # 3.7 Migrer EMPLOI_DU_TEMPS (schedule → EMPLOI_DU_TEMPS)
            self.log("\n  📅 Migration EMPLOI_DU_TEMPS...")
            self._migrate_schedule(conn_old, conn_new)
            
            # 3.8 Migrer PAIEMENT_ELEVE (paiements → PAIEMENT_ELEVE)
            self.log("\n  💰 Migration PAIEMENT_ELEVE...")
            self._migrate_paiements(conn_old, conn_new)
            
            # 3.9 Créer PAIEMENT_PROF initial (vide pour l'instant)
            self.log("\n  💵 Initialisation PAIEMENT_PROF...")
            self.log("    ℹ️ Table créée (données à remplir manuellement)")
            
            conn_old.close()
            conn_new.close()
            
            self.log("\n✅ Migration des données terminée avec succès!")
            
        except Exception as e:
            self.log(f"\n❌ ERREUR lors de la migration: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
            return False
        
        # Étape 4: Vérification
        self.log("\n🔍 ÉTAPE 4: Vérification des données...")
        self._verify_migration()
        
        # Étape 5: Rapport final
        self.log("\n" + "=" * 60)
        self.log("MIGRATION TERMINÉE")
        self.log("=" * 60)
        self._generate_report()
        
        return True
    
    def _migrate_subjects(self, conn_old, conn_new):
        """Migrer subjects → MATIERE"""
        cursor_old = conn_old.cursor()
        cursor_new = conn_new.cursor()
        
        cursor_old.execute("SELECT id, nom, description, tarif_mensuel FROM subjects")
        subjects = cursor_old.fetchall()
        
        migrated = 0
        for subject in subjects:
            old_id, nom, description, tarif = subject
            try:
                cursor_new.execute('''
                    INSERT INTO MATIERE (id_matiere, nom_matiere, description, tarif_mensuel)
                    VALUES (?, ?, ?, ?)
                ''', (old_id, nom, description or "", tarif or 0))
                migrated += 1
            except Exception as e:
                self.log(f"    ⚠️ Erreur matière {nom}: {str(e)}")
        
        conn_new.commit()
        self.log(f"    ✅ {migrated}/{len(subjects)} matières migrées")
    
    def _migrate_rooms(self, conn_old, conn_new):
        """Migrer rooms → SALLE"""
        cursor_old = conn_old.cursor()
        cursor_new = conn_new.cursor()
        
        cursor_old.execute("SELECT id, nom, capacite, equipement, disponible FROM rooms")
        rooms = cursor_old.fetchall()
        
        migrated = 0
        for room in rooms:
            old_id, nom, capacite, equipement, disponible = room
            try:
                cursor_new.execute('''
                    INSERT INTO SALLE (id_salle, nom_salle, capacite, equipement, disponible)
                    VALUES (?, ?, ?, ?, ?)
                ''', (old_id, nom, capacite, equipement or "", disponible))
                migrated += 1
            except Exception as e:
                self.log(f"    ⚠️ Erreur salle {nom}: {str(e)}")
        
        conn_new.commit()
        self.log(f"    ✅ {migrated}/{len(rooms)} salles migrées")
    
    def _migrate_teachers(self, conn_old, conn_new):
        """Migrer teachers → PROFESSEUR"""
        cursor_old = conn_old.cursor()
        cursor_new = conn_new.cursor()
        
        cursor_old.execute("SELECT id, nom, prenom, matiere, tel, salaire_horaire FROM teachers")
        teachers = cursor_old.fetchall()
        
        migrated = 0
        for teacher in teachers:
            old_id, nom, prenom, matiere, tel, salaire_horaire = teacher
            try:
                # Par défaut, on considère le paiement à l'heure
                cursor_new.execute('''
                    INSERT INTO PROFESSEUR (id_prof, nom, prenom, telephone, specialite, 
                                          salaire_mois, prix_par_heure, type_paiement)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (old_id, nom, prenom, tel or "", matiere or "", 
                      0, salaire_horaire or 0, 'heure'))
                migrated += 1
            except Exception as e:
                self.log(f"    ⚠️ Erreur prof {nom} {prenom}: {str(e)}")
        
        conn_new.commit()
        self.log(f"    ✅ {migrated}/{len(teachers)} professeurs migrés")
    
    def _migrate_students(self, conn_old, conn_new):
        """Migrer students → ELEVE"""
        cursor_old = conn_old.cursor()
        cursor_new = conn_new.cursor()
        
        cursor_old.execute("SELECT id, nom, prenom, tel, date_inscription FROM students")
        students = cursor_old.fetchall()
        
        migrated = 0
        for student in students:
            old_id, nom, prenom, tel, date_inscription = student
            try:
                cursor_new.execute('''
                    INSERT INTO ELEVE (id_eleve, nom, prenom, telephone, adresse, 
                                      date_naissance, date_inscription)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (old_id, nom, prenom, tel or "", "", None, date_inscription))
                migrated += 1
            except Exception as e:
                self.log(f"    ⚠️ Erreur élève {nom} {prenom}: {str(e)}")
        
        conn_new.commit()
        self.log(f"    ✅ {migrated}/{len(students)} élèves migrés")
        self.log(f"    ℹ️ Note: adresse et date_naissance à renseigner manuellement")
    
    def _migrate_groups(self, conn_old, conn_new):
        """Migrer groups → GROUPE"""
        cursor_old = conn_old.cursor()
        cursor_new = conn_new.cursor()
        
        cursor_old.execute("SELECT id, nom, matiere_id, niveau FROM groups")
        groups = cursor_old.fetchall()
        
        migrated = 0
        for group in groups:
            old_id, nom, matiere_id, niveau = group
            try:
                # Pour l'instant, id_prof et id_salle sont NULL (à renseigner manuellement)
                cursor_new.execute('''
                    INSERT INTO GROUPE (id_groupe, nom_groupe, id_prof, id_matiere, 
                                       id_salle, niveau, jour, heure_debut, heure_fin)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (old_id, nom, None, matiere_id, None, niveau or "", 
                      None, None, None))
                migrated += 1
            except Exception as e:
                self.log(f"    ⚠️ Erreur groupe {nom}: {str(e)}")
        
        conn_new.commit()
        self.log(f"    ✅ {migrated}/{len(groups)} groupes migrés")
        self.log(f"    ℹ️ Note: id_prof, id_salle et horaires à renseigner")
    
    def _migrate_inscriptions(self, conn_old, conn_new):
        """Migrer inscriptions → INSCRIPTION"""
        cursor_old = conn_old.cursor()
        cursor_new = conn_new.cursor()
        
        cursor_old.execute("SELECT id, student_id, group_id, date_inscription FROM inscriptions")
        inscriptions = cursor_old.fetchall()
        
        migrated = 0
        for inscription in inscriptions:
            old_id, student_id, group_id, date_inscription = inscription
            try:
                # Mensualité par défaut à 0 (à renseigner manuellement)
                cursor_new.execute('''
                    INSERT INTO INSCRIPTION (id_inscription, id_eleve, id_groupe, 
                                            date_inscription, mensualite, active)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (old_id, student_id, group_id, date_inscription, 0, 1))
                migrated += 1
            except Exception as e:
                self.log(f"    ⚠️ Erreur inscription {old_id}: {str(e)}")
        
        conn_new.commit()
        self.log(f"    ✅ {migrated}/{len(inscriptions)} inscriptions migrées")
        self.log(f"    ℹ️ Note: mensualité à renseigner pour chaque inscription")
    
    def _migrate_schedule(self, conn_old, conn_new):
        """Migrer schedule → EMPLOI_DU_TEMPS"""
        cursor_old = conn_old.cursor()
        cursor_new = conn_new.cursor()
        
        cursor_old.execute("""
            SELECT id, group_id, teacher_id, room_id, jour, periode, 
                   heure_debut, heure_fin
            FROM schedule
        """)
        schedules = cursor_old.fetchall()
        
        migrated = 0
        for schedule in schedules:
            old_id, group_id, teacher_id, room_id, jour, periode, h_debut, h_fin = schedule
            try:
                cursor_new.execute('''
                    INSERT INTO EMPLOI_DU_TEMPS (id_edt, id_groupe, jour, heure_debut, 
                                                heure_fin, id_salle, id_prof, periode, actif)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (old_id, group_id, jour, h_debut, h_fin, room_id, teacher_id, 
                      periode or "", 1))
                migrated += 1
            except Exception as e:
                self.log(f"    ⚠️ Erreur emploi du temps {old_id}: {str(e)}")
        
        conn_new.commit()
        self.log(f"    ✅ {migrated}/{len(schedules)} séances migrées")
    
    def _migrate_paiements(self, conn_old, conn_new):
        """Migrer paiements → PAIEMENT_ELEVE"""
        cursor_old = conn_old.cursor()
        cursor_new = conn_new.cursor()
        
        cursor_old.execute("SELECT id, student_id, montant, mois, annee, date_paiement FROM paiements")
        paiements = cursor_old.fetchall()
        
        migrated = 0
        for paiement in paiements:
            old_id, student_id, montant, mois, annee, date_paiement = paiement
            try:
                # montant_du = montant_paye car c'est un ancien paiement effectué
                cursor_new.execute('''
                    INSERT INTO PAIEMENT_ELEVE (id_paiement_eleve, id_eleve, mois, annee,
                                               montant_du, montant_paye, date_paiement, statut)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (old_id, student_id, mois, annee, montant, montant, 
                      date_paiement, 'paye'))
                migrated += 1
            except Exception as e:
                self.log(f"    ⚠️ Erreur paiement {old_id}: {str(e)}")
        
        conn_new.commit()
        self.log(f"    ✅ {migrated}/{len(paiements)} paiements élèves migrés")
    
    def _verify_migration(self):
        """Vérifier que la migration s'est bien passée"""
        conn_new = sqlite3.connect(self.new_db)
        cursor = conn_new.cursor()
        
        tables = [
            ('ELEVE', 'id_eleve'),
            ('PROFESSEUR', 'id_prof'),
            ('MATIERE', 'id_matiere'),
            ('SALLE', 'id_salle'),
            ('GROUPE', 'id_groupe'),
            ('INSCRIPTION', 'id_inscription'),
            ('EMPLOI_DU_TEMPS', 'id_edt'),
            ('PAIEMENT_ELEVE', 'id_paiement_eleve'),
        ]
        
        for table, id_col in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            self.log(f"    ✅ {table}: {count} enregistrements")
        
        conn_new.close()
    
    def _generate_report(self):
        """Générer un rapport de migration"""
        report_file = f"{self.backup_dir}/migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.migration_log))
        
        self.log(f"\n📄 Rapport sauvegardé: {report_file}")
        self.log(f"\n✅ Base de données V2 prête: {self.new_db}")
        self.log(f"📦 Backup disponible dans: {self.backup_dir}")

# Point d'entrée
if __name__ == "__main__":
    print("\n" + "="*60)
    print("  MIGRATION BASE DE DONNÉES V1 → V2")
    print("="*60)
    print("\n⚠️  ATTENTION: Cette opération va créer une nouvelle base de données.")
    print("   L'ancienne base sera sauvegardée automatiquement.\n")
    
    response = input("Continuer la migration? (oui/non): ").strip().lower()
    
    if response in ['oui', 'o', 'yes', 'y']:
        migrator = DatabaseMigration()
        success = migrator.migrate()
        
        if success:
            print("\n✅ Migration réussie!")
            print(f"   Nouvelle base: {migrator.new_db}")
            print(f"   Backup: {migrator.backup_dir}")
        else:
            print("\n❌ Migration échouée. Consultez les logs.")
    else:
        print("\n❌ Migration annulée.")
