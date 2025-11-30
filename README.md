# 📚 Système de Gestion pour Centre de Soutien Scolaire

Application complète de gestion pour centres de soutien scolaire, développée avec Python et CustomTkinter.

## ✨ Fonctionnalités

### 📊 Tableau de Bord
- Vue d'ensemble des statistiques clés
- Nombre total d'élèves, enseignants, groupes et matières
- Revenus mensuels et suivi des paiements
- Liste des paiements récents

### 👨‍🎓 Gestion des Élèves
- Ajouter, modifier et supprimer des élèves
- Informations complètes : nom, prénom, niveau, filière, téléphone
- Recherche rapide par nom ou téléphone
- Suivi des inscriptions aux groupes

### 👨‍🏫 Gestion des Enseignants
- Gestion complète du personnel enseignant
- Informations : nom, prénom, matière, téléphone, salaire horaire
- Recherche et filtrage
- Assignation aux groupes

### 📖 Gestion des Matières
- Catalogue des matières enseignées
- Description détaillée de chaque matière
- Tarification mensuelle
- Recherche et modification

### 👥 Gestion des Groupes
- Création et gestion des groupes de cours
- Association matière-professeur-salle
- Gestion des inscriptions
- Suivi des élèves par groupe

### 💰 Paiements & Comptabilité
- Enregistrement des paiements mensuels
- Suivi par élève, mois et année
- Calcul automatique des revenus mensuels
- Historique complet des transactions
- Statistiques financières

### ✓ Feuille de Présence
- Gestion de la présence par groupe et date
- Statuts : Présent, Absent, Retard
- Interface intuitive avec boutons radio
- Sauvegarde et consultation de l'historique
- Enregistrement par séance

## 🗄️ Base de Données

Le système utilise SQLite avec les tables suivantes :
- **students** : Informations des élèves
- **teachers** : Données des enseignants
- **subjects** : Catalogue des matières
- **groups** : Groupes de cours
- **inscriptions** : Relations élèves-groupes
- **paiements** : Historique des paiements
- **presence** : Feuilles de présence
- **users** : Authentification (préparé pour extension)

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Dépendances requises
- customtkinter : Interface graphique moderne
- pillow : Traitement d'images
- matplotlib : Graphiques (pour extensions futures)
- pandas : Analyse de données (pour rapports)
- openpyxl : Export Excel (pour extensions)
- reportlab : Génération de PDF (pour extensions)

## 📦 Lancement de l'application

```bash
python main.py
```

## 📁 Structure du Projet

```
webapp/
├── main.py                 # Point d'entrée de l'application
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation
├── database/
│   ├── db_manager.py      # Gestion de la base de données
│   └── app.db             # Base SQLite (créée automatiquement)
├── ui/
│   ├── dashboard.py       # Tableau de bord
│   ├── students.py        # Module élèves
│   ├── teachers.py        # Module enseignants
│   ├── subjects.py        # Module matières
│   ├── groups.py          # Module groupes
│   ├── payments.py        # Module paiements
│   └── presence.py        # Module présence
├── widgets/
│   └── sidebar.py         # Menu de navigation
└── assets/                # Ressources (images, icônes)
```

## 🎨 Interface Utilisateur

L'application utilise CustomTkinter pour une interface moderne avec :
- Thème adaptatif (clair/sombre)
- Navigation par menu latéral
- Formulaires modaux
- Tableaux scrollables
- Cartes statistiques colorées
- Boutons d'action intuitifs

## 🔐 Sécurité

- Validation des entrées utilisateur
- Confirmation pour les suppressions
- Gestion des erreurs
- Messages informatifs
- Base de données locale sécurisée

## 🛠️ Extensions Futures Possibles

- [ ] Système d'authentification complet
- [ ] Export des données en PDF/Excel
- [ ] Graphiques de statistiques avec matplotlib
- [ ] Envoi de notifications SMS/Email
- [ ] Calendrier des cours
- [ ] Gestion des notes et examens
- [ ] Génération de bulletins
- [ ] Tableau de bord pour parents
- [ ] Mode multi-utilisateurs avec rôles
- [ ] Backup automatique de la base

## 📝 Utilisation

### Premier lancement
Au premier lancement, la base de données est créée automatiquement avec un utilisateur admin par défaut :
- Username : `admin`
- Password : `admin123`

⚠️ **Important** : En production, changez ces identifiants par défaut !

### Workflow typique
1. Ajouter des matières
2. Ajouter des enseignants
3. Créer des groupes (associer matière + enseignant)
4. Inscrire des élèves
5. Enregistrer les présences
6. Gérer les paiements

## 🐛 Résolution de problèmes

### L'application ne démarre pas
- Vérifiez que Python 3.8+ est installé : `python --version`
- Installez les dépendances : `pip install -r requirements.txt`

### Erreur de base de données
- Supprimez le fichier `database/app.db` pour recréer la base
- Vérifiez les permissions d'écriture dans le dossier

### Interface graphique ne s'affiche pas
- Vérifiez que tkinter est installé : `python -m tkinter`
- Sur Linux : `sudo apt-get install python3-tk`

## 👨‍💻 Développement

### Architecture
- **MVC Pattern** : Séparation modèle-vue-contrôleur
- **Modularité** : Chaque module est indépendant
- **Extensibilité** : Facile d'ajouter de nouveaux modules

### Contribuer
1. Forkez le projet
2. Créez une branche feature
3. Committez vos changements
4. Pushez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est développé pour un usage éducatif et professionnel.

## 💡 Support

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue.

---

Développé avec ❤️ pour faciliter la gestion des centres de soutien scolaire.
