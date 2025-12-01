"""
Utilitaires communs pour l'application
"""

def center_window(window):
    """
    Centre une fenêtre Tkinter sur l'écran
    
    Args:
        window: Instance de CTkToplevel ou CTk
    """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def validate_phone_number(phone: str) -> bool:
    """
    Valide un numéro de téléphone marocain
    
    Args:
        phone: Numéro de téléphone à valider
        
    Returns:
        True si valide, False sinon
    """
    if not phone:
        return True  # Optionnel
    
    import re
    # Format: 0612345678 ou +212612345678
    pattern = r'^(\+212|0)[5-7]\d{8}$'
    return bool(re.match(pattern, phone.replace(" ", "")))


def validate_amount(amount) -> bool:
    """
    Valide qu'un montant est un nombre positif
    
    Args:
        amount: Montant à valider
        
    Returns:
        True si valide, False sinon
    """
    try:
        return float(amount) >= 0
    except (ValueError, TypeError):
        return False
