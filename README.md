# 🎓 Système de Gestion - Centre de Soutien Scolaire

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2%2B-green.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()

Application moderne et professionnelle pour la gestion complète d'un centre de soutien scolaire.

---

## ✨ Caractéristiques

### 🎨 Design Moderne
- Interface utilisateur professionnelle et intuitive
- Palette de 8 couleurs harmonieuses
- 11 composants réutilisables
- Support mode clair/sombre
- Feedback visuel riche

### 📊 Modules Complets
- **Dashboard** : Vue d'ensemble avec statistiques en temps réel
- **Élèves** : Gestion complète des étudiants
- **Enseignants** : Gestion de l'équipe pédagogique
- **Matières** : Catalogue des matières avec tarification
- **Groupes** : Organisation des classes et horaires
- **Paiements** : Comptabilité et suivi des revenus
- **Présence** : Feuille de présence interactive

---

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances
```bash
# Cloner le repository
git clone https://github.com/mamounbq1/Soutien.git
cd Soutien

# Installer les dépendances
pip install -r requirements.txt
```

### Dépendances
```txt
customtkinter>=5.2.0
pillow>=10.0.0
matplotlib>=3.7.0
pandas>=2.0.0
openpyxl>=3.1.0
reportlab>=4.0.0
```

---

## 📖 Utilisation

### Lancement de l'application
```bash
python main.py
```

### Première utilisation
Au premier lancement, l'application :
1. Crée automatiquement la base de données SQLite
2. Initialise toutes les tables nécessaires
3. Crée un utilisateur admin par défaut

### Navigation
L'application comprend 7 modules accessibles via la sidebar :
- 📊 Dashboard
- 👨‍🎓 Élèves
- 👨‍🏫 Enseignants
- 📚 Matières
- 👥 Groupes
- 💰 Paiements
- 📋 Présence

---

## 🏗️ Architecture

```
webapp/
├── config/
│   ├── __init__.py
│   └── theme.py              # Système de design centralisé
│
├── database/
│   ├── app.db                # Base de données SQLite
│   └── db_manager.py         # Gestionnaire de base de données
│
├── widgets/
│   ├── modern_sidebar.py     # Navigation moderne
│   └── modern_components.py  # 11 composants réutilisables
│
├── ui/
│   ├── modern_dashboard.py   # Tableau de bord
│   ├── students.py           # Gestion élèves
│   ├── teachers.py           # Gestion enseignants
│   ├── subjects.py           # Gestion matières
│   ├── groups.py             # Gestion groupes
│   ├── payments.py           # Paiements & comptabilité
│   └── presence.py           # Feuille de présence
│
├── main.py                   # Point d'entrée de l'application
└── requirements.txt          # Dépendances Python
```

---

## 🎨 Système de Design

### Palette de Couleurs
```python
PRIMARY = "#1E88E5"     # Bleu principal
SUCCESS = "#4CAF50"     # Vert succès
WARNING = "#FF9800"     # Orange avertissement
DANGER = "#EF5350"      # Rouge danger
INFO = "#29B6F6"        # Bleu info
SECONDARY = "#78909C"   # Gris secondaire
ACCENT = "#AB47BC"      # Violet accent
NEUTRAL = "#9E9E9E"     # Gris neutre
```

### Composants Modernes
1. **ModernButton** - Boutons stylisés (5 styles)
2. **ModernEntry** - Champs de saisie avec placeholders
3. **ModernLabel** - Labels (6 styles)
4. **ModernComboBox** - Dropdowns modernes
5. **ModernTextBox** - Zones de texte
6. **ModernCard** - Cartes avec ombres
7. **PageHeader** - En-têtes de page
8. **SearchBar** - Barre de recherche
9. **TableHeader** - En-têtes de tableau
10. **TableRow** - Lignes de tableau
11. **ActionButtons** - Boutons d'action

---

## 📚 Documentation

### Documents disponibles
- **README.md** (ce fichier) - Documentation principale
- **MODERN_UI_GUIDE.md** - Guide d'utilisation de l'UI moderne
- **COMPLETE_MODERNIZATION.md** - Détails de la modernisation
- **FINAL_SUMMARY.md** - Résumé complet du projet
- **UI_UX_SUMMARY.md** - Résumé des améliorations UI/UX
- **VISUAL_IMPROVEMENTS.md** - Comparaisons avant/après
- **TROUBLESHOOTING.md** - Guide de dépannage

---

## 💡 Fonctionnalités Principales

### 📊 Dashboard
- 6 cartes statistiques avec dégradés
- Revenus mensuels automatiques
- Liste des paiements récents
- Mise à jour en temps réel

### 👨‍🎓 Gestion des Élèves
- Ajout/modification/suppression d'élèves
- Recherche rapide
- Validation des données
- Historique des inscriptions

### 👨‍🏫 Gestion des Enseignants
- Gestion complète du personnel
- Salaire horaire
- Matières enseignées
- Recherche multi-critères

### 📚 Gestion des Matières
- Catalogue complet
- Tarification flexible
- Descriptions détaillées
- Gestion des prix

### 👥 Gestion des Groupes
- Organisation des classes
- Affectation matière/enseignant
- Gestion des salles
- Inscriptions des élèves

### 💰 Paiements & Comptabilité
- Enregistrement des paiements
- Statistiques en temps réel
- Revenus mensuels
- Historique complet
- Recherche de paiements

### 📋 Feuille de Présence
- Suivi par groupe et date
- États : Présent/Absent/Retard
- Couleurs contextuelles
- Sauvegarde automatique

---

## 🔧 Personnalisation

### Changer le thème
Dans `main.py`, ligne 38 :
```python
ctk.set_appearance_mode("light")  # ou "dark"
```

### Modifier les couleurs
Dans `config/theme.py` :
```python
class ModernTheme:
    PRIMARY = "#votre_couleur"
    # Modifier les autres couleurs...
```

### Ajouter un nouveau module
1. Créer un fichier dans `ui/`
2. Utiliser les composants de `widgets/modern_components.py`
3. Ajouter l'importation dans `main.py`
4. Ajouter la méthode de navigation

---

## 🧪 Tests

### Compilation du code
```bash
python -m py_compile main.py
```

### Vérification des imports
```bash
python -c "import customtkinter; print('✅ CustomTkinter OK')"
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📝 Changelog

### Version 2.0 - Complete Modern Edition (2025-11-30)
- ✅ Modernisation complète de tous les modules
- ✅ Système de design centralisé
- ✅ 11 composants réutilisables
- ✅ Documentation exhaustive
- ✅ Production ready

### Version 1.0 - Initial Release
- Fonctionnalités de base
- Design standard
- 7 modules fonctionnels

---

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👥 Auteurs

- **Mamoun BQ** - Développeur principal
- **GenSpark AI** - Assistant de développement

---

## 🙏 Remerciements

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) pour le framework UI
- La communauté Python pour les excellentes bibliothèques
- Tous les contributeurs du projet

---

## 📞 Support

Pour toute question ou problème :
- 📧 Email : contact@example.com
- 🐛 Issues : [GitHub Issues](https://github.com/mamounbq1/Soutien/issues)
- 📖 Documentation : Voir les fichiers `.md` dans le projet

---

## 🎯 Roadmap

### Prochaines fonctionnalités
- [ ] Export des données en PDF
- [ ] Génération de rapports
- [ ] Notifications par email
- [ ] Sauvegarde automatique
- [ ] Interface multi-langues
- [ ] Mode hors-ligne

---

## ⭐ Si vous aimez ce projet

N'hésitez pas à :
- ⭐ Mettre une étoile sur GitHub
- 🍴 Fork le projet
- 💬 Partager vos retours
- 🐛 Signaler les bugs

---

**Version** : 2.0 - Complete Modern Edition  
**Statut** : ✅ Production Ready  
**Dernière mise à jour** : 2025-11-30

🎉 **Merci d'utiliser notre application !**
