"""
Gestionnaire de brouillons pour auto-save des formulaires
Sauvegarde automatiquement les données des formulaires en cours
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional


class DraftManager:
    """
    Gestionnaire de brouillons pour sauvegarder automatiquement
    les données des formulaires
    """
    
    DRAFT_DIR = "database/drafts"
    
    def __init__(self):
        self._ensure_draft_dir()
    
    def _ensure_draft_dir(self):
        """Crée le répertoire des brouillons s'il n'existe pas"""
        if not os.path.exists(self.DRAFT_DIR):
            os.makedirs(self.DRAFT_DIR, exist_ok=True)
    
    def _get_draft_path(self, form_type: str, form_id: str = "new") -> str:
        """
        Retourne le chemin du fichier de brouillon
        
        Args:
            form_type: Type de formulaire (ex: "student", "teacher", "payment")
            form_id: ID de l'entité ou "new" pour nouveau
        
        Returns:
            Chemin complet du fichier
        """
        filename = f"{form_type}_{form_id}.json"
        return os.path.join(self.DRAFT_DIR, filename)
    
    def save_draft(self, form_type: str, data: Dict, form_id: str = "new"):
        """
        Sauvegarde un brouillon
        
        Args:
            form_type: Type de formulaire
            data: Données du formulaire
            form_id: ID de l'entité ou "new"
        """
        try:
            draft_path = self._get_draft_path(form_type, form_id)
            
            draft_data = {
                'form_type': form_type,
                'form_id': form_id,
                'data': data,
                'saved_at': datetime.now().isoformat(),
            }
            
            with open(draft_path, 'w', encoding='utf-8') as f:
                json.dump(draft_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde du brouillon: {e}")
            return False
    
    def load_draft(self, form_type: str, form_id: str = "new") -> Optional[Dict]:
        """
        Charge un brouillon
        
        Args:
            form_type: Type de formulaire
            form_id: ID de l'entité ou "new"
        
        Returns:
            Dictionnaire avec les données ou None si pas de brouillon
        """
        try:
            draft_path = self._get_draft_path(form_type, form_id)
            
            if not os.path.exists(draft_path):
                return None
            
            with open(draft_path, 'r', encoding='utf-8') as f:
                draft_data = json.load(f)
            
            return draft_data.get('data')
        except Exception as e:
            print(f"❌ Erreur lors du chargement du brouillon: {e}")
            return None
    
    def delete_draft(self, form_type: str, form_id: str = "new"):
        """
        Supprime un brouillon
        
        Args:
            form_type: Type de formulaire
            form_id: ID de l'entité ou "new"
        """
        try:
            draft_path = self._get_draft_path(form_type, form_id)
            
            if os.path.exists(draft_path):
                os.remove(draft_path)
                return True
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la suppression du brouillon: {e}")
            return False
    
    def has_draft(self, form_type: str, form_id: str = "new") -> bool:
        """
        Vérifie si un brouillon existe
        
        Args:
            form_type: Type de formulaire
            form_id: ID de l'entité ou "new"
        
        Returns:
            True si un brouillon existe
        """
        draft_path = self._get_draft_path(form_type, form_id)
        return os.path.exists(draft_path)
    
    def get_draft_age(self, form_type: str, form_id: str = "new") -> Optional[str]:
        """
        Retourne l'âge du brouillon
        
        Args:
            form_type: Type de formulaire
            form_id: ID de l'entité ou "new"
        
        Returns:
            Chaîne formatée avec l'âge du brouillon ou None
        """
        try:
            draft_path = self._get_draft_path(form_type, form_id)
            
            if not os.path.exists(draft_path):
                return None
            
            with open(draft_path, 'r', encoding='utf-8') as f:
                draft_data = json.load(f)
            
            saved_at = datetime.fromisoformat(draft_data['saved_at'])
            age = datetime.now() - saved_at
            
            if age.days > 0:
                return f"Il y a {age.days} jour(s)"
            elif age.seconds > 3600:
                hours = age.seconds // 3600
                return f"Il y a {hours} heure(s)"
            else:
                minutes = age.seconds // 60
                return f"Il y a {minutes} minute(s)"
        except Exception:
            return None
    
    def clean_old_drafts(self, days: int = 7):
        """
        Supprime les brouillons plus vieux que X jours
        
        Args:
            days: Nombre de jours à conserver
        """
        try:
            if not os.path.exists(self.DRAFT_DIR):
                return
            
            now = datetime.now()
            deleted_count = 0
            
            for filename in os.listdir(self.DRAFT_DIR):
                if not filename.endswith('.json'):
                    continue
                
                filepath = os.path.join(self.DRAFT_DIR, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        draft_data = json.load(f)
                    
                    saved_at = datetime.fromisoformat(draft_data['saved_at'])
                    age = now - saved_at
                    
                    if age.days > days:
                        os.remove(filepath)
                        deleted_count += 1
                except Exception:
                    continue
            
            if deleted_count > 0:
                print(f"✅ {deleted_count} brouillon(s) ancien(s) supprimé(s)")
        except Exception as e:
            print(f"❌ Erreur lors du nettoyage des brouillons: {e}")


# Instance globale
_draft_manager = None

def get_draft_manager() -> DraftManager:
    """Retourne l'instance du gestionnaire de brouillons"""
    global _draft_manager
    if _draft_manager is None:
        _draft_manager = DraftManager()
    return _draft_manager
