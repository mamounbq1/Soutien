"""
Configuration globale de l'application
Permet de modifier facilement les paramètres sans toucher au code
"""

import os


class AppSettings:
    """Paramètres généraux de l'application"""
    
    # Informations application
    APP_NAME = "Système de Gestion - Centre de Soutien Scolaire"
    APP_VERSION = "2.0"
    APP_AUTHOR = "Mamoun BQ"
    
    # Base de données
    DB_PATH = "database/app.db"
    DB_BACKUP_DIR = "database/backups"
    DB_AUTO_BACKUP = True
    DB_BACKUP_RETENTION_DAYS = 30
    
    # Interface utilisateur
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 800
    WINDOW_MIN_WIDTH = 1200
    WINDOW_MIN_HEIGHT = 700
    
    # Thème
    DEFAULT_THEME_MODE = "light"  # "light" ou "dark"
    DEFAULT_COLOR_THEME = "blue"
    
    # Tableaux
    TABLE_ROWS_PER_PAGE = 50  # Pagination
    TABLE_MAX_ROWS_BEFORE_SCROLL = 20  # Après 20 lignes, utiliser ScrollableTable
    
    # Formats
    DATE_FORMAT = "%Y-%m-%d"
    DATE_DISPLAY_FORMAT = "%d/%m/%Y"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # Validation
    PHONE_PATTERN = r'^(\+212|0)[5-7]\d{8}$'  # Format marocain
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Paiements
    CURRENCY_SYMBOL = "DH"
    CURRENCY_POSITION = "after"  # "before" ou "after"
    
    # Export/Import
    EXPORT_DIR = "outputs"
    IMPORT_ALLOWED_EXTENSIONS = [".xlsx", ".csv", ".json"]
    
    # Logs
    LOG_ENABLED = True
    LOG_FILE = "app.log"
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    # Performance
    CACHE_ENABLED = True
    CACHE_TTL_SECONDS = 300  # 5 minutes
    
    @classmethod
    def get_db_full_path(cls) -> str:
        """Retourne le chemin complet de la base de données"""
        return os.path.abspath(cls.DB_PATH)
    
    @classmethod
    def ensure_directories(cls):
        """Crée les répertoires nécessaires s'ils n'existent pas"""
        directories = [
            os.path.dirname(cls.DB_PATH),
            cls.DB_BACKUP_DIR,
            cls.EXPORT_DIR,
        ]
        
        for directory in directories:
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)


class ThemeSettings:
    """
    Paramètres de thème personnalisables
    Ces valeurs peuvent surcharger celles de ModernTheme
    """
    
    # Possibilité de personnaliser les couleurs
    CUSTOM_PRIMARY_COLOR = None  # Si None, utilise la valeur par défaut
    CUSTOM_SECONDARY_COLOR = None
    CUSTOM_SUCCESS_COLOR = None
    CUSTOM_DANGER_COLOR = None
    
    # Tailles personnalisables
    CUSTOM_SIDEBAR_WIDTH = None  # Si None, utilise 180
    CUSTOM_BUTTON_HEIGHT = None  # Si None, utilise 28
    CUSTOM_FONT_SIZE = None  # Si None, utilise 11
    
    @classmethod
    def get_sidebar_width(cls) -> int:
        """Retourne la largeur de la sidebar (personnalisée ou par défaut)"""
        from config.theme import ModernTheme
        return cls.CUSTOM_SIDEBAR_WIDTH or ModernTheme.SIDEBAR_WIDTH
    
    @classmethod
    def get_button_height(cls) -> int:
        """Retourne la hauteur des boutons (personnalisée ou par défaut)"""
        from config.theme import ModernTheme
        return cls.CUSTOM_BUTTON_HEIGHT or ModernTheme.BUTTON_HEIGHT


class BusinessSettings:
    """Paramètres métier de l'application"""
    
    # Horaires
    SCHOOL_OPENING_HOUR = 8  # 8h
    SCHOOL_CLOSING_HOUR = 22  # 22h
    SESSION_DURATION_MINUTES = 120  # 2 heures par défaut
    
    # Capacités
    DEFAULT_ROOM_CAPACITY = 20
    MAX_STUDENTS_PER_GROUP = 30
    MIN_STUDENTS_PER_GROUP = 1
    
    # Tarification
    DEFAULT_MONTHLY_FEE = 500  # DH
    DISCOUNT_ENABLED = True
    MAX_DISCOUNT_PERCENT = 50
    
    # Paiements
    PAYMENT_DUE_DAY = 5  # Le 5 de chaque mois
    PAYMENT_REMINDER_DAYS_BEFORE = 3  # Rappel 3 jours avant
    LATE_PAYMENT_FEE_PERCENT = 0  # Pas de frais de retard par défaut
    
    # Présence
    ABSENCE_REQUIRES_JUSTIFICATION = False
    MAX_ABSENCES_BEFORE_WARNING = 3
    
    # Année scolaire
    SCHOOL_YEAR_START_MONTH = 9  # Septembre
    SCHOOL_YEAR_END_MONTH = 6    # Juin
    
    @classmethod
    def get_current_school_year(cls) -> str:
        """Retourne l'année scolaire en cours (ex: 2024-2025)"""
        from datetime import datetime
        now = datetime.now()
        if now.month >= cls.SCHOOL_YEAR_START_MONTH:
            return f"{now.year}-{now.year + 1}"
        else:
            return f"{now.year - 1}-{now.year}"


# Initialiser les répertoires au chargement du module
AppSettings.ensure_directories()
