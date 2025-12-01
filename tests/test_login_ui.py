"""
Test visuel pour la page de login
Vérifie que tous les éléments sont visibles
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from ui.login import LoginWindow


def test_login_layout():
    """Test visuel de la mise en page du login"""
    
    # Créer une fenêtre de test
    root = ctk.CTk()
    root.withdraw()  # Cacher la fenêtre principale
    
    # Callback de test
    def on_success():
        print("✅ Login réussi (test)")
    
    # Créer la fenêtre de login
    login_window = LoginWindow(root, on_success)
    
    # Vérifications
    print("\n" + "="*60)
    print("🧪 TEST VISUEL - PAGE DE LOGIN")
    print("="*60 + "\n")
    
    # 1. Vérifier la géométrie
    geometry = login_window.geometry()
    width, height = geometry.split('+')[0].split('x')
    print(f"📐 Dimensions fenêtre: {width}x{height}")
    
    if int(height) >= 600:
        print("   ✅ Hauteur suffisante (>= 600px)")
    else:
        print(f"   ❌ Hauteur insuffisante ({height}px < 600px)")
    
    # 2. Vérifier les widgets
    print(f"\n🔍 Widgets détectés:")
    
    widgets_found = {
        'username_entry': False,
        'password_entry': False,
        'login_button': False
    }
    
    def check_widgets(widget, depth=0):
        """Parcourir récursivement les widgets"""
        if depth > 10:  # Limiter la profondeur
            return
        
        widget_type = widget.__class__.__name__
        
        # Vérifier si c'est un des widgets qu'on cherche
        if hasattr(widget, 'cget'):
            try:
                if widget_type == 'CTkEntry':
                    placeholder = widget.cget('placeholder_text')
                    if 'utilisateur' in placeholder.lower():
                        widgets_found['username_entry'] = True
                        print(f"   ✅ Champ username trouvé")
                    elif 'passe' in placeholder.lower():
                        widgets_found['password_entry'] = True
                        print(f"   ✅ Champ password trouvé")
                
                elif widget_type == 'CTkButton':
                    text = widget.cget('text')
                    if 'connecter' in text.lower():
                        widgets_found['login_button'] = True
                        print(f"   ✅ Bouton 'Se connecter' trouvé")
            except:
                pass
        
        # Parcourir les enfants
        if hasattr(widget, 'winfo_children'):
            for child in widget.winfo_children():
                check_widgets(child, depth + 1)
    
    check_widgets(login_window)
    
    # 3. Résumé
    print(f"\n📊 Résumé:")
    all_found = all(widgets_found.values())
    
    if all_found:
        print("   ✅ Tous les éléments critiques sont présents")
        print("\n" + "="*60)
        print("✅ TEST VISUEL RÉUSSI - Page de login OK")
        print("="*60 + "\n")
        result = True
    else:
        print("   ❌ Éléments manquants:")
        for widget_name, found in widgets_found.items():
            if not found:
                print(f"      - {widget_name}")
        print("\n" + "="*60)
        print("❌ TEST VISUEL ÉCHOUÉ - Éléments manquants")
        print("="*60 + "\n")
        result = False
    
    # Fermer
    login_window.destroy()
    root.destroy()
    
    return result


if __name__ == '__main__':
    try:
        success = test_login_layout()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
