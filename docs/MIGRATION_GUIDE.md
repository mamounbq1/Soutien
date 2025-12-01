# 📘 GUIDE DE MIGRATION - Version 2

## 🎯 Objectif de la Migration

Transformer la structure actuelle de la base de données pour implémenter le nouveau modèle avec:
- Gestion avancée des paiements (élèves ET professeurs)
- Relations optimisées entre tables
- Calcul automatique des heures de cours
- Meilleure séparation GROUPE / EMPLOI_DU_TEMPS

---

## 📊 Comparaison des Modèles

### Modèle Actuel (V1)

```
students (id, nom, prenom, niveau, filiere, tel, parent_tel, date_inscription)
teachers (id, nom, prenom, matiere, tel, salaire_horaire)
subjects (id, nom, description, tarif_mensuel)
rooms (id, nom, capacite, equipement, disponible)
groups (id, nom, matiere_id, niveau)
inscriptions (id, student_id, group_id, date_inscription)
schedule (id, group_id, teacher_id, room_id, jour, periode, heure_debut, heure_fin)
paiements (id, student_id, montant, mois, annee, date_paiement)
presence (id, schedule_id, student_id, date_seance, status)
```

### Nouveau Modèle (V2)

```
ELEVE (id_eleve, nom, prenom, telephone, adresse, date_naissance, date_inscription)
PROFESSEUR (id_prof, nom, prenom, telephone, specialite, salaire_mois, prix_par_heure, type_paiement)
MATIERE (id_matiere, nom_matiere, description, tarif_mensuel)
SALLE (id_salle, nom_salle, capacite, equipement, disponible)
GROUPE (id_groupe, nom_groupe, id_prof, id_matiere, id_salle, niveau, jour, heure_debut, heure_fin)
INSCRIPTION (id_inscription, id_eleve, id_groupe, date_inscription, mensualite)
EMPLOI_DU_TEMPS (id_edt, id_groupe, jour, heure_debut, heure_fin, id_salle, id_prof)
PAIEMENT_ELEVE (id_paiement_eleve, id_eleve, mois, annee, montant_du, montant_paye, statut)
PAIEMENT_PROF (id_paiement_prof, id_prof, mois, annee, nb_heures, montant_du, montant_paye, statut)
PRESENCE (id_presence, id_edt, id_eleve, date_seance, statut, remarque)
```

---

## 🔄 Changements Majeurs

### 1. **ELEVE** (ex-students)
**Nouveaux champs:**
- `adresse` : Adresse complète de l'élève
- `date_naissance` : Date de naissance pour calcul d'âge

**Changements:**
- `tel` → `telephone`
- Suppression de `parent_tel`, `niveau`, `filiere` (déplacés vers INSCRIPTION)

### 2. **PROFESSEUR** (ex-teachers)
**Nouveaux champs:**
- `salaire_mois` : Salaire mensuel fixe
- `prix_par_heure` : Prix horaire
- `type_paiement` : 'fixe' ou 'heure'

**Changements:**
- `matiere` → `specialite`
- `salaire_horaire` remplacé par système flexible

### 3. **GROUPE** (restructuré)
**Nouveaux champs:**
- `id_prof` : Professeur attitré au groupe
- `id_salle` : Salle habituelle du groupe
- `jour`, `heure_debut`, `heure_fin` : Horaire principal

**Impact:**
- Le GROUPE devient une entité complète avec ses relations
- L'EMPLOI_DU_TEMPS gère les séances spécifiques

### 4. **INSCRIPTION** (amélioré)
**Nouveaux champs:**
- `mensualite` : Montant mensuel pour cet élève dans ce groupe
- `active` : Statut actif/inactif

**Utilité:**
- Permet des tarifs personnalisés par élève
- Facilite le calcul automatique des paiements dus

### 5. **PAIEMENT_ELEVE** (ex-paiements)
**Nouveaux champs:**
- `montant_du` : Montant total dû
- `montant_paye` : Montant payé
- `statut` : 'paye', 'impaye', 'partiel'
- `remarque` : Notes

**Avantage:**
- Gestion fine des paiements partiels
- Suivi du solde restant

### 6. **PAIEMENT_PROF** (NOUVEAU ⭐)
**Fonctionnalités:**
- Calcul automatique des heures enseignées
- Paiement fixe OU horaire selon `type_paiement`
- Suivi des paiements partiels
- Historique complet

### 7. **EMPLOI_DU_TEMPS** (distinct de GROUPE)
**Différence:**
- GROUPE = entité pédagogique
- EMPLOI_DU_TEMPS = séances programmées

**Avantage:**
- Un groupe peut avoir plusieurs séances hebdomadaires
- Flexibilité pour modifications temporaires

---

## 🛠️ Étapes de Migration

### Étape 1: Backup
```bash
cp database/app.db database/app_backup_$(date +%Y%m%d).db
```

### Étape 2: Test du nouveau schéma
```bash
python database/db_manager_v2.py
```

### Étape 3: Migration des données
```bash
python database/migrate_database.py
```

### Étape 4: Vérification
```bash
python database/verify_migration.py
```

### Étape 5: Mise à jour du code
```bash
# Remplacer les imports
# from database.db_manager import DatabaseManager
# →
# from database.db_manager_v2 import DatabaseManagerV2
```

---

## ⚠️ Points d'Attention

### Données à migrer manuellement:
1. **parent_tel** → Peut être ajouté dans `adresse` ou créer une table CONTACT
2. **niveau, filiere** → Seront gérés via INSCRIPTION
3. **salaire_horaire** → Convertir en `prix_par_heure` ou `salaire_mois`

### Relations à recréer:
1. Lier GROUPE aux PROFESSEUR et SALLE
2. Recalculer les EMPLOI_DU_TEMPS depuis schedule
3. Créer les PAIEMENT_PROF basés sur l'historique

### Validations nécessaires:
1. Vérifier que tous les élèves ont été migrés
2. Confirmer les relations INSCRIPTION
3. Valider les montants dans PAIEMENT_ELEVE
4. Tester les clés étrangères

---

## 📈 Avantages du Nouveau Modèle

✅ **Gestion complète des paiements professeurs**
✅ **Calcul automatique des heures**
✅ **Relations optimisées avec clés étrangères**
✅ **Statuts de paiement (payé/impayé/partiel)**
✅ **Historique complet et traçabilité**
✅ **Séparation claire GROUPE / EMPLOI_DU_TEMPS**
✅ **Support des tarifs personnalisés par élève**
✅ **Flexibilité paiement fixe/horaire pour profs**

---

## 🔧 Fonctionnalités à Implémenter

### Module Paiement Professeurs (NOUVEAU)
- [ ] Calcul automatique nb_heures par mois
- [ ] Génération bulletins de salaire
- [ ] Suivi paiements partiels
- [ ] Historique complet

### Module Inscriptions (AMÉLIORE)
- [ ] Interface gestion inscriptions
- [ ] Tarifs personnalisés
- [ ] Activation/désactivation inscriptions
- [ ] Calcul auto mensualités

### Module Paiements Élèves (AMÉLIORE)
- [ ] Suivi montant_du vs montant_paye
- [ ] Gestion paiements partiels
- [ ] Alertes impayés
- [ ] Reçus automatiques

### Emploi du Temps (OPTIMISE)
- [ ] Vue hebdomadaire améliorée
- [ ] Détection conflits
- [ ] Validation disponibilités
- [ ] Export PDF

---

## 📞 Support

Pour toute question sur la migration:
1. Consulter ce guide
2. Vérifier les logs de migration
3. Contacter l'équipe de développement

**Date de migration:** À définir
**Version:** 2.0.0
**Auteur:** Équipe de développement
