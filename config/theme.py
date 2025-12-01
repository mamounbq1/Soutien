"""
Configuration du thème moderne pour l'application
Palette de couleurs professionnelle et cohérente
"""

class ModernTheme:
    """
    Thème moderne avec palette de couleurs cohérente
    Inspiré des applications professionnelles modernes
    """
    
    # === COULEURS PRINCIPALES ===
    # Couleurs de base
    PRIMARY = "#1E88E5"          # Bleu principal moderne
    PRIMARY_HOVER = "#1565C0"    # Bleu foncé pour hover
    PRIMARY_DARK = "#1565C0"     # Bleu foncé pour hover
    PRIMARY_LIGHT = "#42A5F5"    # Bleu clair
    
    SECONDARY = "#26A69A"        # Turquoise
    SECONDARY_DARK = "#00897B"   # Turquoise foncé
    
    ACCENT = "#FF6B6B"           # Rouge accent moderne
    SUCCESS = "#4CAF50"          # Vert succès
    WARNING = "#FFA726"          # Orange avertissement
    DANGER = "#EF5350"           # Rouge danger
    INFO = "#29B6F6"             # Bleu info
    
    # === COULEURS DE FOND ===
    # Mode clair
    BG_LIGHT = "#F5F7FA"         # Fond principal clair
    BG_CARD_LIGHT = "#FFFFFF"    # Fond des cartes clair
    BG_HOVER_LIGHT = "#E8EAF6"   # Hover clair
    
    # Mode sombre
    BG_DARK = "#1A1D23"          # Fond principal sombre
    BG_CARD_DARK = "#23272F"     # Fond des cartes sombre
    BG_HOVER_DARK = "#2D323B"    # Hover sombre
    
    # === COULEURS DE TEXTE ===
    TEXT_PRIMARY_LIGHT = "#1A1D23"      # Texte principal clair
    TEXT_SECONDARY_LIGHT = "#5F6368"    # Texte secondaire clair
    TEXT_DISABLED_LIGHT = "#9E9E9E"     # Texte désactivé clair
    
    TEXT_PRIMARY_DARK = "#E8EAED"       # Texte principal sombre
    TEXT_SECONDARY_DARK = "#9AA0A6"     # Texte secondaire sombre
    TEXT_DISABLED_DARK = "#5F6368"      # Texte désactivé sombre
    
    # Alias pour compatibilité (mode par défaut = light)
    TEXT_PRIMARY = TEXT_PRIMARY_LIGHT
    TEXT_SECONDARY = TEXT_SECONDARY_LIGHT
    TEXT_DISABLED = TEXT_DISABLED_LIGHT
    
    # === SIDEBAR ===
    SIDEBAR_BG_LIGHT = "#FFFFFF"
    SIDEBAR_BG_DARK = "#1F2937"
    SIDEBAR_HOVER_LIGHT = "#F3F4F6"
    SIDEBAR_HOVER_DARK = "#374151"
    SIDEBAR_ACTIVE_LIGHT = "#E0F2FE"
    SIDEBAR_ACTIVE_DARK = "#1E3A8A"
    
    # === CARTES STATISTIQUES ===
    # Palette moderne pour les statistiques
    STAT_CARD_COLORS = {
        'blue': ('#1E88E5', '#1565C0'),
        'orange': ('#FF9800', '#F57C00'),
        'purple': ('#9C27B0', '#7B1FA2'),
        'teal': ('#00897B', '#00695C'),
        'green': ('#4CAF50', '#388E3C'),
        'lime': ('#7CB342', '#558B2F'),
        'pink': ('#E91E63', '#C2185B'),
        'indigo': ('#3F51B5', '#303F9F'),
    }
    
    # === BOUTONS ===
    BTN_PRIMARY = PRIMARY
    BTN_PRIMARY_HOVER = PRIMARY_DARK
    BTN_SECONDARY = SECONDARY
    BTN_SECONDARY_HOVER = SECONDARY_DARK
    BTN_DANGER = DANGER
    BTN_DANGER_HOVER = "#E53935"
    BTN_SUCCESS = SUCCESS
    BTN_SUCCESS_HOVER = "#43A047"
    
    # === BORDURES ===
    BORDER_LIGHT = "#E0E0E0"
    BORDER_DARK = "#3A3F47"
    BORDER_RADIUS = 12          # Rayon des coins arrondis
    BORDER_RADIUS_SMALL = 8
    BORDER_RADIUS_LARGE = 16
    
    # === OMBRES ===
    SHADOW_LIGHT = "#00000015"
    SHADOW_MEDIUM = "#00000025"
    SHADOW_HEAVY = "#00000040"
    
    # === ESPACEMENTS ===
    SPACING_XS = 4
    SPACING_SM = 8
    SPACING_MD = 12
    SPACING_LG = 16
    SPACING_XL = 20
    SPACING_XXL = 24
    
    # === TYPOGRAPHIE ===
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_SMALL = 10
    FONT_SIZE_NORMAL = 11
    FONT_SIZE_MEDIUM = 12
    FONT_SIZE_LARGE = 13
    FONT_SIZE_XLARGE = 16
    FONT_SIZE_XXLARGE = 20
    
    # === DIMENSIONS ===
    SIDEBAR_WIDTH = 180
    BUTTON_HEIGHT = 28
    INPUT_HEIGHT = 26
    CARD_HEIGHT = 68
    
    # === ICÔNES (Unicode) - Modernes et professionnelles ===
    ICONS = {
        'dashboard': '◈',
        'students': '⚲',
        'teachers': '⚐',
        'subjects': '◫',
        'groups': '▣',
        'payments': '◉',
        'presence': '✓',
        'logout': '⎋',
        'add': '+',
        'edit': '✎',
        'delete': '✕',
        'search': '⌕',
        'refresh': '↻',
        'save': '✓',
        'cancel': '✕',
        'menu': '☰',
        'print': '⎙',
    }
    
    @staticmethod
    def get_stat_color(index):
        """Retourne une couleur de carte statistique basée sur l'index"""
        colors = list(ModernTheme.STAT_CARD_COLORS.values())
        return colors[index % len(colors)]
    
    @staticmethod
    def get_gradient(color1, color2):
        """Retourne un tuple de couleurs pour un gradient"""
        return (color1, color2)


class AnimationConfig:
    """Configuration pour les animations"""
    HOVER_DURATION = 200        # ms
    CLICK_DURATION = 100        # ms
    TRANSITION_DURATION = 300   # ms
    FADE_DURATION = 400         # ms
