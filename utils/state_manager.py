"""
Gestionnaire d'état centralisé de l'application
Permet de partager des données entre modules sans couplage fort
"""

from typing import Any, Dict, Callable, List
from datetime import datetime


class StateManager:
    """
    Singleton pour gérer l'état global de l'application
    
    Usage:
        state = StateManager()
        state.set('current_user', user_data)
        user = state.get('current_user')
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._state: Dict[str, Any] = {}
        self._observers: Dict[str, List[Callable]] = {}
        self._history: List[Dict] = []
        self._initialized = True
        
        # État initial
        self._initialize_default_state()
    
    def _initialize_default_state(self):
        """Initialiser l'état par défaut"""
        self._state = {
            'app_name': 'Centre de Soutien',
            'version': '2.0',
            'current_user': None,
            'is_authenticated': False,
            'current_page': 'dashboard',
            'selected_items': {},
            'filters': {},
            'sort_by': {},
            'last_refresh': {},
            'notifications': [],
            'theme': 'light',
            'language': 'fr'
        }
    
    def set(self, key: str, value: Any, notify: bool = True):
        """
        Définir une valeur dans l'état
        
        Args:
            key: Clé de l'état
            value: Valeur à stocker
            notify: Notifier les observateurs (True par défaut)
        """
        old_value = self._state.get(key)
        self._state[key] = value
        
        # Historique
        self._history.append({
            'timestamp': datetime.now(),
            'key': key,
            'old_value': old_value,
            'new_value': value
        })
        
        # Limiter l'historique à 100 entrées
        if len(self._history) > 100:
            self._history = self._history[-100:]
        
        # Notifier les observateurs
        if notify and key in self._observers:
            for callback in self._observers[key]:
                try:
                    callback(key, value, old_value)
                except Exception as e:
                    print(f"❌ Erreur callback observateur {key}: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtenir une valeur de l'état
        
        Args:
            key: Clé de l'état
            default: Valeur par défaut si clé inexistante
        
        Returns:
            Valeur stockée ou default
        """
        return self._state.get(key, default)
    
    def remove(self, key: str):
        """Supprimer une clé de l'état"""
        if key in self._state:
            del self._state[key]
        if key in self._observers:
            del self._observers[key]
    
    def observe(self, key: str, callback: Callable):
        """
        Observer les changements d'une clé
        
        Args:
            key: Clé à observer
            callback: Fonction appelée lors du changement
                      Signature: callback(key, new_value, old_value)
        """
        if key not in self._observers:
            self._observers[key] = []
        self._observers[key].append(callback)
    
    def unobserve(self, key: str, callback: Callable):
        """Arrêter d'observer une clé"""
        if key in self._observers:
            try:
                self._observers[key].remove(callback)
            except ValueError:
                pass
    
    def get_history(self, key: str = None, limit: int = 10) -> List[Dict]:
        """
        Obtenir l'historique des changements
        
        Args:
            key: Filtrer par clé (None = tout)
            limit: Nombre max d'entrées
        
        Returns:
            Liste des changements
        """
        history = self._history
        if key:
            history = [h for h in history if h['key'] == key]
        return history[-limit:]
    
    def reset(self):
        """Réinitialiser l'état (sauf utilisateur)"""
        current_user = self._state.get('current_user')
        is_authenticated = self._state.get('is_authenticated')
        
        self._initialize_default_state()
        
        self._state['current_user'] = current_user
        self._state['is_authenticated'] = is_authenticated
    
    def clear_all(self):
        """Effacer complètement l'état"""
        self._state.clear()
        self._observers.clear()
        self._history.clear()
        self._initialize_default_state()
    
    def export_state(self) -> Dict:
        """Exporter l'état complet (pour sauvegarde)"""
        return self._state.copy()
    
    def import_state(self, state: Dict):
        """Importer un état (restauration)"""
        self._state = state.copy()
    
    # ═══════════════════════════════════════════════════════════
    # MÉTHODES DE COMMODITÉ
    # ═══════════════════════════════════════════════════════════
    
    def set_current_user(self, user_data: Dict):
        """Définir l'utilisateur actuel"""
        self.set('current_user', user_data)
        self.set('is_authenticated', True)
    
    def logout(self):
        """Déconnecter l'utilisateur"""
        self.set('current_user', None)
        self.set('is_authenticated', False)
    
    def is_authenticated(self) -> bool:
        """Vérifier si un utilisateur est connecté"""
        return self.get('is_authenticated', False)
    
    def get_current_user(self) -> Dict:
        """Obtenir l'utilisateur actuel"""
        return self.get('current_user', {})
    
    def set_current_page(self, page_name: str):
        """Définir la page actuelle"""
        self.set('current_page', page_name)
    
    def add_notification(self, message: str, type: str = 'info'):
        """Ajouter une notification"""
        notifications = self.get('notifications', [])
        notifications.append({
            'message': message,
            'type': type,
            'timestamp': datetime.now()
        })
        self.set('notifications', notifications)
    
    def clear_notifications(self):
        """Effacer les notifications"""
        self.set('notifications', [])
    
    def set_filter(self, module: str, filter_data: Dict):
        """Définir un filtre pour un module"""
        filters = self.get('filters', {})
        filters[module] = filter_data
        self.set('filters', filters)
    
    def get_filter(self, module: str) -> Dict:
        """Obtenir le filtre d'un module"""
        filters = self.get('filters', {})
        return filters.get(module, {})
    
    def mark_refreshed(self, module: str):
        """Marquer qu'un module a été rafraîchi"""
        last_refresh = self.get('last_refresh', {})
        last_refresh[module] = datetime.now()
        self.set('last_refresh', last_refresh, notify=False)
    
    def needs_refresh(self, module: str, max_age_seconds: int = 300) -> bool:
        """Vérifier si un module nécessite un rafraîchissement"""
        last_refresh = self.get('last_refresh', {})
        if module not in last_refresh:
            return True
        
        age = (datetime.now() - last_refresh[module]).total_seconds()
        return age > max_age_seconds


# Instance globale singleton
state = StateManager()
