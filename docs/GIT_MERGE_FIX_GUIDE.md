# 🔧 GUIDE: Résoudre le Conflit de Merge Git

## ⚠️ **Problème Actuel**
```
error: You have not concluded your merge (MERGE_HEAD exists).
hint: Please, commit your changes before merging.
fatal: Exiting because of unfinished merge.
```

---

## 🎯 **SOLUTION RAPIDE** (Recommandée)

### **Option 1: Abandonner le Merge et Recommencer**
```bash
cd "C:\Users\DELL\Downloads\WTSP IMG\Soutien-genspark_ai_developer"

# 1. Vérifier l'état
git status

# 2. Abandonner le merge en cours
git merge --abort

# 3. S'assurer que vous êtes sur la bonne branche
git checkout genspark_ai_developer

# 4. Récupérer les dernières modifications
git pull origin genspark_ai_developer

# 5. Lancer l'application
python main.py
```

### **Option 2: Compléter le Merge Manuellement**
```bash
cd "C:\Users\DELL\Downloads\WTSP IMG\Soutien-genspark_ai_developer"

# 1. Voir les fichiers en conflit
git status

# 2. Pour chaque fichier en conflit, choisir:
#    - Garder la version distante: git checkout --theirs <fichier>
#    - Garder la version locale: git checkout --ours <fichier>
#    - Éditer manuellement pour combiner les deux

# 3. Marquer les fichiers comme résolus
git add .

# 4. Terminer le merge
git commit -m "fix: Résolution des conflits de merge"

# 5. Pousser
git push origin genspark_ai_developer
```

---

## 🔍 **Diagnostic Approfondi**

### **Vérifier Quels Fichiers Sont en Conflit**
```bash
# Voir les fichiers non fusionnés
git diff --name-only --diff-filter=U

# Voir le contenu des conflits
git diff
```

### **Types de Marqueurs de Conflit**
Les fichiers en conflit contiennent:
```
<<<<<<< HEAD
votre code local
=======
code distant (remote)
>>>>>>> origin/genspark_ai_developer
```

---

## 🚀 **APRÈS RÉSOLUTION**

### **1. Récupérer les Dernières Corrections**
```bash
git pull origin genspark_ai_developer
```

### **2. Lancer la Migration (Si Nécessaire)**
```bash
# Seulement si app_v2.db n'existe pas
python database/migrate_to_v2.py
```

### **3. Tester l'Application**
```bash
python main.py
```

---

## ✅ **CORRECTIONS APPLIQUÉES DANS CE COMMIT**

Les erreurs suivantes ont été corrigées:

### **1. AttributeError: 'DatabaseCompatibility' object has no attribute 'get_schedule_by_group'**
- **Fichier**: `ui/print_dialogs.py`, ligne 130
- **Solution**: Ajout de la méthode dans `db_manager_v2_extended.py` et `db_compatibility.py`

### **2. AttributeError: 'DatabaseCompatibility' object has no attribute 'get_revenus_mois'**
- **Fichier**: `ui/payments.py`, ligne 260
- **Solution**: Méthode déjà présente via `get_monthly_revenue()`, ajout de référence directe

### **3. AttributeError: 'DatabaseCompatibility' object has no attribute 'get_presence_by_group_date'**
- **Fichier**: `ui/presence.py`, ligne 202
- **Solution**: Ajout de la méthode dans `db_manager_v2_extended.py` et `db_compatibility.py`

---

## 📋 **VÉRIFICATION POST-FIX**

### **Test Python**
```python
from database.db_compatibility import DatabaseCompatibility

db = DatabaseCompatibility()

# Vérifier que toutes les méthodes existent
assert hasattr(db, 'get_schedule_by_group')
assert hasattr(db, 'get_revenus_mois')
assert hasattr(db, 'get_presence_by_group_date')
assert hasattr(db, 'get_monthly_revenue')

print("✅ Toutes les méthodes sont disponibles!")
```

### **Test Complet**
```bash
# Vérifier structure DB
python -c "from database.db_compatibility import DatabaseCompatibility; db = DatabaseCompatibility(); print(f'Élèves: {len(db.get_all_students())}'); print(f'Professeurs: {len(db.get_all_teachers())}')"

# Lancer l'application
python main.py
```

---

## 🆘 **EN CAS DE PROBLÈME**

### **Si le Merge est Complètement Bloqué**
```bash
# DERNIÈRE OPTION: Reset complet (⚠️ PERD LES MODIFICATIONS LOCALES)
git fetch origin
git reset --hard origin/genspark_ai_developer
git pull origin genspark_ai_developer
```

### **Si la Base de Données est Corrompue**
```bash
# Restaurer depuis le backup
cd database/backups
# Trouver le dernier backup
dir /O-D app_backup_*.db
# Copier le backup
copy app_backup_YYYYMMDD_HHMMSS.db ..\app_v2.db
```

---

## 📞 **SUPPORT**

Si les problèmes persistent:
1. Vérifier que vous êtes sur la bonne branche: `git branch`
2. Vérifier l'historique: `git log --oneline -10`
3. Vérifier les remotes: `git remote -v`

**Commit ID des Corrections**: Voir le prochain commit après celui-ci
**Branche**: `genspark_ai_developer`
**Base de Données**: `database/app_v2.db`
