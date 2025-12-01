"""
Gestionnaire de retry et timeout pour opérations réseau/DB
"""

import time
import sqlite3
from functools import wraps
from typing import Callable, Any, Tuple, Type


class RetryManager:
    """Gestionnaire de retry avec backoff exponentiel"""
    
    @staticmethod
    def retry(
        max_attempts: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
        exceptions: Tuple[Type[Exception], ...] = (sqlite3.OperationalError,),
        on_retry: Callable = None
    ):
        """
        Décorateur pour retry automatique
        
        Args:
            max_attempts: Nombre max de tentatives
            delay: Délai initial entre tentatives (secondes)
            backoff: Facteur multiplicatif du délai (2.0 = double à chaque fois)
            exceptions: Tuple des exceptions à capturer
            on_retry: Callback appelé après chaque échec
        
        Usage:
            @RetryManager.retry(max_attempts=5, delay=2.0)
            def ma_fonction_db():
                # Code qui peut échouer
                pass
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                attempt = 0
                current_delay = delay
                
                while attempt < max_attempts:
                    try:
                        return func(*args, **kwargs)
                    
                    except exceptions as e:
                        attempt += 1
                        
                        if attempt >= max_attempts:
                            # Dernière tentative échouée
                            print(f"❌ Échec après {max_attempts} tentatives: {func.__name__}")
                            raise
                        
                        # Log retry
                        print(f"⚠️  Tentative {attempt}/{max_attempts} échouée: {func.__name__} - {str(e)}")
                        print(f"⏳ Nouvelle tentative dans {current_delay}s...")
                        
                        # Callback custom
                        if on_retry:
                            try:
                                on_retry(attempt, current_delay, e)
                            except Exception as callback_error:
                                print(f"❌ Erreur callback on_retry: {callback_error}")
                        
                        # Attendre avant retry
                        time.sleep(current_delay)
                        
                        # Augmenter le délai (backoff exponentiel)
                        current_delay *= backoff
            
            return wrapper
        return decorator
    
    @staticmethod
    def with_timeout(timeout_seconds: float):
        """
        Décorateur pour timeout (nécessite threading)
        
        Args:
            timeout_seconds: Durée max d'exécution
        
        Usage:
            @RetryManager.with_timeout(10.0)
            def ma_fonction():
                # Code qui ne doit pas dépasser 10s
                pass
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                import threading
                
                result = [None]
                exception = [None]
                
                def target():
                    try:
                        result[0] = func(*args, **kwargs)
                    except Exception as e:
                        exception[0] = e
                
                thread = threading.Thread(target=target)
                thread.daemon = True
                thread.start()
                thread.join(timeout_seconds)
                
                if thread.is_alive():
                    print(f"⏱️  Timeout après {timeout_seconds}s: {func.__name__}")
                    raise TimeoutError(f"Fonction {func.__name__} timeout après {timeout_seconds}s")
                
                if exception[0]:
                    raise exception[0]
                
                return result[0]
            
            return wrapper
        return decorator


# ═══════════════════════════════════════════════════════════
# EXEMPLES D'UTILISATION
# ═══════════════════════════════════════════════════════════

def retry_callback(attempt: int, delay: float, error: Exception):
    """Callback appelé après chaque échec"""
    print(f"🔄 Retry #{attempt} après {delay:.1f}s (erreur: {str(error)})")


@RetryManager.retry(max_attempts=5, delay=1.0, backoff=2.0)
def example_db_operation():
    """Exemple d'opération DB avec retry"""
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ELEVE LIMIT 1")
    data = cursor.fetchone()
    conn.close()
    return data


@RetryManager.with_timeout(5.0)
def example_long_operation():
    """Exemple d'opération avec timeout"""
    time.sleep(3)  # Simule une opération longue
    return "Terminé"


@RetryManager.retry(max_attempts=3, on_retry=retry_callback)
@RetryManager.with_timeout(10.0)
def example_combined():
    """Exemple combinant retry ET timeout"""
    # Code critique ici
    pass


# ═══════════════════════════════════════════════════════════
# HELPERS POUR DB
# ═══════════════════════════════════════════════════════════

class SafeDBConnection:
    """Context manager pour connexion DB avec retry"""
    
    def __init__(self, db_path: str, max_attempts: int = 3):
        self.db_path = db_path
        self.max_attempts = max_attempts
        self.conn = None
    
    def __enter__(self):
        @RetryManager.retry(
            max_attempts=self.max_attempts,
            delay=0.5,
            exceptions=(sqlite3.OperationalError, sqlite3.DatabaseError)
        )
        def connect():
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        
        self.conn = connect()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            try:
                if exc_type is None:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            finally:
                self.conn.close()
        return False


# Usage du context manager:
# with SafeDBConnection("database/app.db") as conn:
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM ELEVE")
#     data = cursor.fetchall()
