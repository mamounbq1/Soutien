"""
ADAPTATEUR DE COMPATIBILITÉ V1 → V2
====================================
Cet adaptateur permet d'utiliser le nouveau DB manager V2
tout en gardant l'ancienne API pour une transition progressive.
"""

from database.db_manager_v2_extended import DatabaseManagerV2Extended
from typing import List, Tuple, Optional

class DatabaseCompatibility(DatabaseManagerV2Extended):
    """
    Adaptateur de compatibilité entre V1 et V2
    
    Fournit une API cohérente en anglais tout en utilisant
    la base de données française en interne
    """
    
    def __init__(self, db_name="database/app.db"):
        super().__init__(db_name)
    
    # ═══════════════════════════════════════════════════════════
    # ALIAS POUR COHÉRENCE DU NOMMAGE (anglais)
    # ═══════════════════════════════════════════════════════════
    
    # Alias élèves (français → anglais)
    def get_student_by_id(self, student_id: int):
        """Alias: get_eleve_by_id"""
        return self._get_student_formatted(self.get_eleve_by_id(student_id))
    
    def delete_student(self, student_id: int):
        """Alias: delete_eleve"""
        return self.delete_eleve(student_id)
    
    # Alias professeurs (français → anglais)
    def get_teacher_by_id_raw(self, teacher_id: int):
        """Alias: get_professeur_by_id (retourne format brut)"""
        return self.get_professeur_by_id(teacher_id)
    
    def delete_teacher(self, teacher_id: int):
        """Alias: delete_professeur"""
        return self.delete_professeur(teacher_id)
    
    # Alias matières (français → anglais)
    def get_subject_by_id(self, subject_id: int):
        """Alias: get_matiere_by_id"""
        return self.get_matiere_by_id(subject_id)
    
    def delete_subject(self, subject_id: int):
        """Alias: delete_matiere"""
        return self.delete_matiere(subject_id)
    
    def _validate_telephone(self, tel: str) -> bool:
        """Valide un numéro de téléphone (format marocain)"""
        if not tel:
            return True  # Optionnel
        # Format: 0612345678 ou +212612345678
        import re
        pattern = r'^(\+212|0)[5-7]\d{8}$'
        return bool(re.match(pattern, tel.replace(" ", "")))
    
    def _validate_montant(self, montant: float) -> bool:
        """Valide un montant (doit être positif)"""
        try:
            return float(montant) >= 0
        except (ValueError, TypeError):
            return False
    
    def _get_student_formatted(self, eleve):
        """Formatte un élève du format V2 au format compatible"""
        if not eleve:
            return None
        
        # Extraire les informations de l'adresse
        parent_tel = ""
        niveau = ""
        filiere = ""
        
        if eleve[4]:  # Si adresse existe
            parts = eleve[4].split(" | ")
            for part in parts:
                if part.startswith("Parent:"):
                    parent_tel = part.replace("Parent:", "").strip()
                elif part.startswith("Niveau:"):
                    niveau = part.replace("Niveau:", "").strip()
                elif part.startswith("Filière:"):
                    filiere = part.replace("Filière:", "").strip()
        
        return (
            eleve[0],  # id
            eleve[1],  # nom
            eleve[2],  # prenom
            niveau,    # niveau
            filiere,   # filiere
            eleve[3] or "",  # tel
            parent_tel,      # parent_tel
            eleve[6] if len(eleve) > 6 else ""  # date_inscription
        )
    
    # ═══════════════════════════════════════════════════════════
    # ADAPTATEURS STUDENTS → ELEVE
    # ═══════════════════════════════════════════════════════════
    
    def add_student(self, nom, prenom, niveau="", filiere="", tel="", parent_tel=""):
        """Adapter l'ancienne API vers la nouvelle"""
        # Validation
        if not nom or not prenom:
            raise ValueError("Le nom et le prénom sont obligatoires")
        
        if tel and not self._validate_telephone(tel):
            raise ValueError(f"Numéro de téléphone invalide: {tel}")
        
        if parent_tel and not self._validate_telephone(parent_tel):
            raise ValueError(f"Numéro de téléphone parent invalide: {parent_tel}")
        
        # Construire l'adresse avec toutes les informations
        adresse_parts = []
        if parent_tel:
            adresse_parts.append(f"Parent: {parent_tel}")
        if niveau:
            adresse_parts.append(f"Niveau: {niveau}")
        if filiere:
            adresse_parts.append(f"Filière: {filiere}")
        adresse = " | ".join(adresse_parts) if adresse_parts else ""
        return self.add_eleve(nom, prenom, tel, adresse, None)
    
    def get_all_students(self):
        """Retourner les élèves avec l'ancien format"""
        eleves = self.get_all_eleves()
        # Convertir: (id_eleve, nom, prenom, telephone, adresse, date_naissance, date_inscription, ...)
        # En: (id, nom, prenom, niveau, filiere, tel, parent_tel, date_inscription)
        result = []
        for eleve in eleves:
            # Extraire les informations de l'adresse
            parent_tel = ""
            niveau = ""
            filiere = ""
            
            if eleve[4]:  # Si adresse existe
                parts = eleve[4].split(" | ")
                for part in parts:
                    if part.startswith("Parent:"):
                        parent_tel = part.replace("Parent:", "").strip()
                    elif part.startswith("Niveau:"):
                        niveau = part.replace("Niveau:", "").strip()
                    elif part.startswith("Filière:"):
                        filiere = part.replace("Filière:", "").strip()
            
            result.append((
                eleve[0],  # id
                eleve[1],  # nom
                eleve[2],  # prenom
                niveau,    # niveau (extrait de adresse)
                filiere,   # filiere (extrait de adresse)
                eleve[3] or "",  # tel
                parent_tel,      # parent_tel (extrait de adresse)
                eleve[6] if len(eleve) > 6 else ""  # date_inscription
            ))
        return result
    
    def get_student_by_id(self, student_id):
        """Adapter get_eleve_by_id"""
        eleve = self.get_eleve_by_id(student_id)
        if not eleve:
            return None
        
        # Extraire les informations de l'adresse
        parent_tel = ""
        niveau = ""
        filiere = ""
        
        if eleve[4]:  # Si adresse existe
            parts = eleve[4].split(" | ")
            for part in parts:
                if part.startswith("Parent:"):
                    parent_tel = part.replace("Parent:", "").strip()
                elif part.startswith("Niveau:"):
                    niveau = part.replace("Niveau:", "").strip()
                elif part.startswith("Filière:"):
                    filiere = part.replace("Filière:", "").strip()
        
        return (
            eleve[0],  # id
            eleve[1],  # nom
            eleve[2],  # prenom
            niveau,    # niveau
            filiere,   # filiere
            eleve[3] or "",  # tel
            parent_tel,      # parent_tel
            eleve[6] if len(eleve) > 6 else ""  # date_inscription
        )
    
    def update_student(self, student_id, nom, prenom, niveau="", filiere="", tel="", parent_tel=""):
        """Adapter update_eleve"""
        # Construire l'adresse avec toutes les informations
        adresse_parts = []
        if parent_tel:
            adresse_parts.append(f"Parent: {parent_tel}")
        if niveau:
            adresse_parts.append(f"Niveau: {niveau}")
        if filiere:
            adresse_parts.append(f"Filière: {filiere}")
        adresse = " | ".join(adresse_parts) if adresse_parts else ""
        return self.update_eleve(student_id, nom, prenom, tel, adresse, None)
    
    def delete_student(self, student_id):
        """Adapter delete_eleve"""
        return self.delete_eleve(student_id)
    
    def search_students(self, query):
        """Adapter search_eleves - Returns same format as get_all_eleves"""
        # Simply return the raw search results from search_eleves
        # This maintains consistency with get_all_eleves format
        return self.search_eleves(query)
        return result
    
    # ═══════════════════════════════════════════════════════════
    # ADAPTATEURS TEACHERS → PROFESSEUR
    # ═══════════════════════════════════════════════════════════
    
    def add_teacher(self, nom, prenom, matiere="", tel="", salaire_horaire=0):
        """Adapter vers add_professeur"""
        # Par défaut, on utilise le paiement à l'heure
        return self.add_professeur(nom, prenom, tel, matiere, 0, salaire_horaire, 'heure')
    
    def get_all_teachers(self):
        """Retourner les professeurs avec l'ancien format"""
        profs = self.get_all_professeurs()
        # Convertir vers ancien format
        result = []
        for prof in profs:
            # (id_prof, nom, prenom, telephone, specialite, salaire_mois, prix_par_heure, type_paiement, ...)
            # → (id, nom, prenom, matiere, tel, salaire_horaire)
            result.append((
                prof[0],  # id
                prof[1],  # nom
                prof[2],  # prenom
                prof[4] or "",  # specialite → matiere
                prof[3] or "",  # telephone
                prof[6] if prof[7] == 'heure' else 0  # prix_par_heure
            ))
        return result
    
    def get_teacher_by_id(self, teacher_id):
        """Adapter get_professeur_by_id"""
        prof = self.get_professeur_by_id(teacher_id)
        if not prof:
            return None
        return (
            prof[0],  # id
            prof[1],  # nom
            prof[2],  # prenom
            prof[4] or "",  # specialite → matiere
            prof[3] or "",  # telephone
            prof[6] if prof[7] == 'heure' else 0  # prix_par_heure
        )
    
    def update_teacher(self, teacher_id, nom, prenom, matiere="", tel="", salaire_horaire=0):
        """Adapter update_professeur"""
        return self.update_professeur(teacher_id, nom, prenom, tel, matiere, 0, salaire_horaire, 'heure')
    
    def delete_teacher(self, teacher_id):
        """Adapter delete_professeur"""
        return self.delete_professeur(teacher_id)
    
    def search_teachers(self, query):
        """Adapter search_professeurs"""
        profs = self.search_professeurs(query)
        result = []
        for prof in profs:
            result.append((
                prof[0],  # id
                prof[1],  # nom
                prof[2],  # prenom
                prof[4] or "",  # specialite → matiere
                prof[3] or "",  # telephone
                prof[6] if len(prof) > 7 and prof[7] == 'heure' else 0  # prix_par_heure
            ))
        return result
    
    # ═══════════════════════════════════════════════════════════
    # ADAPTATEURS SUBJECTS → MATIERE
    # ═══════════════════════════════════════════════════════════
    
    def add_subject(self, nom, description="", tarif_mensuel=0):
        """Adapter vers add_matiere"""
        return self.add_matiere(nom, description, tarif_mensuel)
    
    def get_all_subjects(self):
        """Retourner les matières"""
        return self.get_all_matieres()
    
    def search_subjects(self, query):
        """Adapter search_matieres"""
        return self.search_matieres(query)
    
    def update_subject(self, subject_id, nom, description="", tarif_mensuel=0):
        """Adapter update_matiere"""
        return self.update_matiere(subject_id, nom, description, tarif_mensuel)
    
    def delete_subject(self, subject_id):
        """Adapter delete_matiere"""
        return self.delete_matiere(subject_id)
    
    # ═══════════════════════════════════════════════════════════
    # ADAPTATEURS ROOMS → SALLE
    # ═══════════════════════════════════════════════════════════
    
    def add_room(self, nom, capacite, equipement="", disponible=True):
        """Adapter vers add_salle"""
        return self.add_salle(nom, capacite, equipement, disponible)
    
    def get_all_rooms(self):
        """Retourner les salles"""
        return self.get_all_salles()
    
    def get_available_rooms(self):
        """Adapter get_salles_disponibles"""
        return self.get_salles_disponibles()
    
    def get_room_by_id(self, room_id):
        """Adapter get_salle_by_id"""
        return self.get_salle_by_id(room_id)
    
    def search_rooms(self, query):
        """Adapter search_salles"""
        return self.search_salles(query)
    
    def update_room(self, room_id, nom, capacite, equipement="", disponible=True):
        """Adapter update_salle"""
        return self.update_salle(room_id, nom, capacite, equipement, disponible)
    
    def delete_room(self, room_id):
        """Adapter delete_salle"""
        return self.delete_salle(room_id)
    
    # ═══════════════════════════════════════════════════════════
    # ADAPTATEURS GROUPS → GROUPE
    # ═══════════════════════════════════════════════════════════
    
    def add_group(self, nom, matiere_id, niveau=""):
        """Adapter vers add_groupe"""
        return self.add_groupe(nom, matiere_id, None, None, niveau, "", "", "")
    
    def get_all_groups(self):
        """Retourner les groupes"""
        groupes = self.get_all_groupes()
        # Convertir format si nécessaire
        result = []
        for groupe in groupes:
            # Format attendu: (id, nom, matiere, niveau)
            result.append((
                groupe[0],  # id_groupe
                groupe[1],  # nom_groupe
                groupe[2] if len(groupe) > 2 else "",  # matiere
                groupe[5] if len(groupe) > 5 else ""   # niveau
            ))
        return result
    
    def get_group_details(self, group_id):
        """Adapter get_groupe_by_id"""
        return self.get_groupe_by_id(group_id)
    
    def search_groups(self, query):
        """Adapter search_groupes"""
        groupes = self.search_groupes(query)
        result = []
        for groupe in groupes:
            result.append((
                groupe[0],  # id_groupe
                groupe[1],  # nom_groupe
                groupe[2] if len(groupe) > 2 else "",  # matiere
                groupe[5] if len(groupe) > 5 else ""   # niveau
            ))
        return result
    
    def update_group(self, group_id, nom, matiere_id, niveau=""):
        """Adapter update_groupe"""
        groupe = self.get_groupe_by_id(group_id)
        if not groupe:
            return
        # Garder les anciennes valeurs de prof, salle, horaires
        id_prof = groupe[2] if len(groupe) > 2 else None
        id_salle = groupe[4] if len(groupe) > 4 else None
        jour = groupe[6] if len(groupe) > 6 else ""
        h_debut = groupe[7] if len(groupe) > 7 else ""
        h_fin = groupe[8] if len(groupe) > 8 else ""
        return self.update_groupe(group_id, nom, matiere_id, id_prof, id_salle, niveau, jour, h_debut, h_fin)
    
    def delete_group(self, group_id):
        """Adapter delete_groupe"""
        return self.delete_groupe(group_id)
    
    # ═══════════════════════════════════════════════════════════
    # ADAPTATEURS SCHEDULE → EMPLOI_DU_TEMPS
    # ═══════════════════════════════════════════════════════════
    
    def add_schedule(self, group_id, teacher_id, room_id, jour, periode, heure_debut, heure_fin):
        """Adapter vers add_emploi_du_temps"""
        return self.add_emploi_du_temps(group_id, jour, heure_debut, heure_fin, room_id, teacher_id, periode)
    
    def get_all_schedules(self):
        """Retourner l'emploi du temps"""
        return self.get_all_emploi_du_temps()
    
    def get_schedule_details(self, schedule_id):
        """Adapter get_edt_by_id"""
        return self.get_edt_by_id(schedule_id)
    
    def search_schedules(self, query):
        """Rechercher dans l'emploi du temps"""
        # Note: À implémenter selon besoin
        return []
    
    def update_schedule(self, schedule_id, group_id, teacher_id, room_id, jour, periode, heure_debut, heure_fin):
        """Adapter update_emploi_du_temps"""
        return self.update_emploi_du_temps(schedule_id, group_id, jour, heure_debut, heure_fin, room_id, teacher_id, periode)
    
    def delete_schedule(self, schedule_id):
        """Adapter delete_emploi_du_temps"""
        return self.delete_emploi_du_temps(schedule_id)
    
    # Validations
    def check_room_conflict(self, room_id, jour, heure_debut, heure_fin, exclude_schedule_id=None):
        """Adapter check_salle_conflit"""
        return self.check_salle_conflit(room_id, jour, heure_debut, heure_fin, exclude_schedule_id)
    
    def check_teacher_conflict(self, teacher_id, jour, heure_debut, heure_fin, exclude_schedule_id=None):
        """Adapter check_prof_conflit"""
        return self.check_prof_conflit(teacher_id, jour, heure_debut, heure_fin, exclude_schedule_id)
    
    def check_group_conflict(self, group_id, jour, heure_debut, heure_fin, exclude_schedule_id=None):
        """Adapter check_groupe_conflit"""
        return self.check_groupe_conflit(group_id, jour, heure_debut, heure_fin, exclude_schedule_id)
    
    # ═══════════════════════════════════════════════════════════
    # ADAPTATEURS PAIEMENTS → PAIEMENT_ELEVE
    # ═══════════════════════════════════════════════════════════
    
    def add_payment(self, student_id, montant, mois, annee):
        """Adapter vers PAIEMENT_ELEVE (ancien format = tout payé)"""
        # Validation
        if not self._validate_montant(montant):
            raise ValueError(f"Montant invalide: {montant}. Le montant doit être un nombre positif.")
        
        if float(montant) <= 0:
            raise ValueError("Le montant doit être supérieur à 0")
        
        # Dans l'ancien système, un paiement créé = payé complètement
        return self.add_paiement_eleve(student_id, mois, annee, montant, montant, 'paye')
    
    def get_all_payments(self):
        """Retourner les paiements élèves"""
        paiements = self.get_all_paiements_eleve()
        # Convertir format
        result = []
        for p in paiements:
            # Format attendu: (id, student_name, montant, mois, annee, date_paiement)
            result.append((
                p[0],  # id
                p[1] if len(p) > 1 else "",  # student_name
                p[5] if len(p) > 5 else 0,  # montant_paye
                p[2] if len(p) > 2 else "",  # mois
                p[3] if len(p) > 3 else "",  # annee
                p[6] if len(p) > 6 else ""   # date_paiement
            ))
        return result
    
    def get_payment_details(self, payment_id):
        """Obtenir détails paiement"""
        return self.get_paiement_eleve_by_id(payment_id)
    
    def search_payments(self, query):
        """Rechercher paiements"""
        return self.search_paiements_eleve(query)
    
    def delete_payment(self, payment_id):
        """Supprimer paiement"""
        return self.delete_paiement_eleve(payment_id)
    
    def get_monthly_revenue(self, mois, annee):
        """Calculer revenus du mois"""
        return self.get_revenus_mois(mois, annee)
    
    # ═══════════════════════════════════════════════════════════
    # MÉTHODES SUPPLÉMENTAIRES POUR PRINT DIALOGS & PRESENCE
    # ═══════════════════════════════════════════════════════════
    
    def get_schedule_by_group(self, group_id):
        """Obtenir l'emploi du temps d'un groupe (pour impression)"""
        return super().get_schedule_by_group(group_id)
    
    def get_presence_by_group_date(self, group_id, date):
        """Obtenir la présence pour un groupe à une date"""
        return super().get_presence_by_group_date(group_id, date)
    
    # ═══════════════════════════════════════════════════════════
    # AUTRES MÉTHODES
    # ═══════════════════════════════════════════════════════════
    
    def get_group_students(self, group_id):
        """Obtenir les élèves d'un groupe"""
        inscriptions = self.get_inscriptions_by_groupe(group_id)
        # Convertir format
        result = []
        for insc in inscriptions:
            # Format: (id_inscription, id_eleve, nom, prenom, telephone, mensualite, active, date_inscription)
            # → (id_eleve, nom, prenom, tel, date_inscription)
            result.append((
                insc[1],  # id_eleve
                insc[2],  # nom
                insc[3],  # prenom
                insc[4] if len(insc) > 4 else "",  # telephone
                insc[7] if len(insc) > 7 else ""   # date_inscription
            ))
        return result
    
    def get_students_not_in_group(self, group_id):
        """Obtenir les élèves non inscrits dans un groupe"""
        # Obtenir tous les élèves
        all_eleves = self.get_all_eleves()
        # Obtenir les élèves du groupe
        groupe_eleves = self.get_inscriptions_by_groupe(group_id)
        groupe_eleves_ids = [e[1] for e in groupe_eleves]  # id_eleve
        
        # Filtrer
        result = []
        for eleve in all_eleves:
            if eleve[0] not in groupe_eleves_ids:
                result.append((
                    eleve[0],  # id
                    eleve[1],  # nom
                    eleve[2],  # prenom
                    "",        # niveau
                    "",        # filiere
                    eleve[3] or "",  # tel
                    "",        # parent_tel
                    eleve[6] if len(eleve) > 6 else ""  # date_inscription
                ))
        return result
    
    def remove_inscription(self, student_id, group_id):
        """Désinscrire un élève d'un groupe"""
        # Trouver l'inscription
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_inscription FROM INSCRIPTION
            WHERE id_eleve=? AND id_groupe=?
        """, (student_id, group_id))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return self.delete_inscription(result[0])
        return False

# Test
if __name__ == "__main__":
    db = DatabaseCompatibility()
    print("✅ Adaptateur de compatibilité chargé!")
    print("   Les anciennes méthodes fonctionnent avec la nouvelle DB V2")
