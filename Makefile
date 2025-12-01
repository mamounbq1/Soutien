# Makefile pour le Système de Gestion - Centre de Soutien Scolaire

.PHONY: help install run test clean dev build

help:
	@echo "Commandes disponibles:"
	@echo "  make install    - Installer les dépendances"
	@echo "  make run        - Lancer l'application"
	@echo "  make test       - Exécuter les tests"
	@echo "  make clean      - Nettoyer les fichiers temporaires"
	@echo "  make dev        - Installer les dépendances de développement"
	@echo "  make build      - Créer un package de distribution"
	@echo "  make lint       - Vérifier le code avec flake8"
	@echo "  make format     - Formater le code avec black"

install:
	@echo "📦 Installation des dépendances..."
	pip install -r requirements.txt
	@echo "✅ Installation terminée"

dev:
	@echo "📦 Installation des dépendances de développement..."
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 mypy
	@echo "✅ Installation de développement terminée"

run:
	@echo "🚀 Lancement de l'application..."
	python main.py

test:
	@echo "🧪 Exécution des tests..."
	python -m pytest tests/ -v --cov=. --cov-report=term-missing

test-quick:
	@echo "🧪 Exécution rapide des tests..."
	python -m pytest tests/ -v

lint:
	@echo "🔍 Vérification du code..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	@echo "✨ Formatage du code..."
	black . --exclude="/(\.git|__pycache__|\.pytest_cache|venv|env)/"

clean:
	@echo "🧹 Nettoyage des fichiers temporaires..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/
	@echo "✅ Nettoyage terminé"

build:
	@echo "📦 Création du package..."
	python setup.py sdist bdist_wheel
	@echo "✅ Package créé dans dist/"

db-backup:
	@echo "💾 Sauvegarde de la base de données..."
	@mkdir -p database/backups
	@cp database/app.db database/backups/app_backup_$$(date +%Y%m%d_%H%M%S).db
	@echo "✅ Sauvegarde créée"

db-clean-old:
	@echo "🧹 Nettoyage des anciennes sauvegardes (>30 jours)..."
	@find database/backups -name "app_backup_*.db" -mtime +30 -delete 2>/dev/null || true
	@echo "✅ Anciennes sauvegardes supprimées"

drafts-clean:
	@echo "🧹 Nettoyage des brouillons anciens..."
	python -c "from utils.draft_manager import get_draft_manager; get_draft_manager().clean_old_drafts(7)"
	@echo "✅ Brouillons nettoyés"

check:
	@echo "✅ Vérification de l'installation..."
	@python -c "import customtkinter; print('✓ CustomTkinter:', customtkinter.__version__)"
	@python -c "from database.db_compatibility import DatabaseCompatibility; db = DatabaseCompatibility(); print('✓ Database:', db.db_name)"
	@python -c "from config.settings import AppSettings; print('✓ Settings:', AppSettings.APP_VERSION)"
	@echo "✅ Tous les modules sont OK"

all: clean install test

.DEFAULT_GOAL := help
