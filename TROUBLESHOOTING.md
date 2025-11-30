# 🔧 Guide de Dépannage - Interface Moderne

## Problèmes Résolus

### ✅ ValueError: ['padx'] are not supported arguments

**Symptôme:**
```
ValueError: ['padx'] are not supported arguments
```

**Cause:**
Le paramètre `padx` était utilisé dans `self.configure()` d'un `CTkButton`, ce qui n'est pas supporté. `padx` est un paramètre de positionnement (grid/pack), pas une propriété du widget.

**Solution:**
✅ **CORRIGÉ** dans le commit `86ca22d`
- Suppression de `self.configure(padx=15)` dans `ModernMenuButton`
- Le padding est maintenant géré par `grid(padx=15)` dans la sidebar

**Version corrigée:**
- Fichier: `widgets/modern_sidebar.py`
- Ligne 39 supprimée

---

## Problèmes Courants et Solutions

### 1. L'application ne démarre pas

#### Problème: ImportError
```
ImportError: No module named 'customtkinter'
```

**Solution:**
```bash
pip install customtkinter
```

#### Problème: ImportError pour config.theme
```
ModuleNotFoundError: No module named 'config'
```

**Solution:**
Assurez-vous d'être dans le bon répertoire:
```bash
cd /path/to/webapp
python main_modern.py
```

---

### 2. Les icônes ne s'affichent pas

#### Problème: Cases vides à la place des icônes
```
□ Dashboard  # Au lieu de 📊 Dashboard
```

**Cause:**
Votre police ne supporte pas les caractères Unicode/Emoji.

**Solution:**
- **Windows:** Utiliser Segoe UI Emoji (installée par défaut)
- **Linux:** Installer `fonts-noto-color-emoji`
  ```bash
  sudo apt-get install fonts-noto-color-emoji
  ```
- **macOS:** Les emojis sont supportés nativement

**Alternative:**
Modifier `config/theme.py` pour utiliser des caractères ASCII:
```python
ICONS = {
    'dashboard': '≡',
    'students': '👤',
    'teachers': '🎓',
    # ... etc
}
```

---

### 3. Les couleurs sont différentes

#### Problème: Les couleurs ne correspondent pas à la documentation

**Cause:**
Mode sombre/clair différent.

**Solution:**
Dans `main_modern.py`, ligne 32:
```python
# Pour mode clair
ctk.set_appearance_mode("light")

# Pour mode sombre
ctk.set_appearance_mode("dark")

# Pour suivre le système
ctk.set_appearance_mode("system")
```

---

### 4. La base de données n'est pas trouvée

#### Problème: 
```
sqlite3.OperationalError: no such table: students
```

**Cause:**
La base de données n'a pas été créée ou est corrompue.

**Solution 1:** Supprimer et recréer la base
```bash
rm database/app.db
python main_modern.py  # La DB sera recréée automatiquement
```

**Solution 2:** Vérifier les permissions
```bash
chmod 755 database/
chmod 644 database/app.db
```

---

### 5. Fenêtre trop petite ou trop grande

#### Problème: La fenêtre n'a pas la bonne taille

**Solution:**
Modifier dans `main_modern.py`:
```python
# Ligne 26 - Taille de départ
self.geometry("1400x800")

# Ligne 27 - Taille minimale
self.minsize(1200, 700)

# Pour plein écran
self.state('zoomed')  # Windows
# ou
self.attributes('-zoomed', True)  # Linux
```

---

### 6. L'ancien et le nouveau design se mélangent

#### Problème: Certains éléments sont modernes, d'autres non

**Cause:**
Vous avez mélangé `main.py` et `main_modern.py`.

**Solution:**
Utilisez exclusivement un des deux:
```bash
# Version MODERNE (recommandée)
python main_modern.py

# Version ANCIENNE
python main.py
```

---

### 7. Erreur lors de l'import de ModernTheme

#### Problème:
```
ImportError: cannot import name 'ModernTheme' from 'config.theme'
```

**Solution:**
Vérifier la structure:
```
webapp/
├── config/
│   ├── __init__.py  ← Doit exister (peut être vide)
│   └── theme.py
```

Si `__init__.py` manque:
```bash
touch config/__init__.py
```

---

### 8. Les boutons ne répondent pas au clic

#### Problème: Clic sans effet

**Vérifications:**
1. Vérifier la console pour les erreurs
2. Vérifier que les callbacks sont définis:
   ```python
   btn = ModernButton(
       parent,
       text="Test",
       command=self.my_function  # ← Doit exister
   )
   ```

**Debug:**
Ajouter un print dans le callback:
```python
def my_function(self):
    print("Bouton cliqué!")  # Pour debug
    # ... reste du code
```

---

### 9. Performance lente avec beaucoup de données

#### Problème: L'interface rame avec 1000+ élèves

**Solutions:**

**1. Pagination:**
```python
# Au lieu de charger tout
students = self.db_manager.get_all_students()

# Charger par page
students = self.db_manager.get_students_page(page=1, per_page=50)
```

**2. Lazy loading:**
Charger les données seulement quand nécessaire.

**3. Virtualisation:**
N'afficher que les lignes visibles dans le ScrollableFrame.

---

### 10. Les formulaires ne se centrent pas

#### Problème: Les modals apparaissent en haut à gauche

**Solution:**
Vérifier que `_center_window()` est appelé:
```python
class MyForm(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # ... setup ...
        self._center_window()  # ← Important!
    
    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
```

---

## 🔍 Debugging Tips

### 1. Activer le mode debug
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. Vérifier la version de CustomTkinter
```python
import customtkinter
print(customtkinter.__version__)
# Devrait être >= 5.0.0
```

### 3. Tester les composants individuellement
```python
# Tester juste la sidebar
from widgets.modern_sidebar import ModernSidebar
import customtkinter as ctk

app = ctk.CTk()
sidebar = ModernSidebar(app, lambda x: print(x))
sidebar.pack()
app.mainloop()
```

### 4. Vérifier les imports
```bash
python -c "from config.theme import ModernTheme; print('✅ OK')"
python -c "from widgets.modern_sidebar import ModernSidebar; print('✅ OK')"
python -c "from ui.modern_dashboard import ModernDashboard; print('✅ OK')"
```

---

## 📞 Obtenir de l'Aide

### Vérifications Avant de Demander de l'Aide

1. ✅ Version de Python >= 3.8
   ```bash
   python --version
   ```

2. ✅ CustomTkinter installé
   ```bash
   pip show customtkinter
   ```

3. ✅ Structure des fichiers correcte
   ```bash
   ls -R webapp/
   ```

4. ✅ Permissions correctes
   ```bash
   ls -la database/
   ```

5. ✅ Console pour les erreurs
   Toujours exécuter depuis le terminal pour voir les erreurs

---

## 🆘 Problèmes Non Listés

Si votre problème n'est pas listé:

1. **Vérifier la console** pour le message d'erreur complet
2. **Chercher l'erreur** dans les fichiers mentionnés
3. **Vérifier les logs** si activés
4. **Comparer avec l'exemple** dans `ui/modern_students_example.py`
5. **Revenir à l'ancienne version** si nécessaire:
   ```bash
   python main.py  # Version stable
   ```

---

## ✅ Checklist de Santé de l'Application

Utilisez cette checklist pour vérifier que tout fonctionne:

```bash
# 1. Dépendances
□ pip install -r requirements.txt

# 2. Structure
□ ls config/theme.py
□ ls widgets/modern_sidebar.py
□ ls ui/modern_dashboard.py

# 3. Compilation
□ python -m py_compile main_modern.py

# 4. Base de données
□ ls database/app.db

# 5. Lancement
□ python main_modern.py
```

Si tous les points passent ✅, l'application devrait fonctionner!

---

**Dernière mise à jour:** 30 Novembre 2025  
**Version:** 2.0.0 (Interface Moderne)  
**Bug fixé:** ValueError padx - Commit 86ca22d
