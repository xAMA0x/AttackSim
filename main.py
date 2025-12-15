"""
Crypto Simulator - Point d'entrée principal
Simulateur d'Attaques Cryptographiques - ESGI
"""
import sys
from pathlib import Path

# Ajout du chemin src/ au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core import ui
from attacks.symmetric import des_attack, aes_attack
from attacks.asymmetric import rsa_attack, ecc_attack
from attacks.special import timing_attack


def main():
    """Fonction principale - Boucle du menu"""
    
    while True:
        ui.clear_screen()
        ui.display_banner()
        
        # Menu principal
        main_menu = {
            "1": "🔐 Attaques Symétrique (DES, AES)",
            "2": "🔑 Attaques Asymétrique (RSA, ECC)",
            "3": "⏱️ Attaques Spéciales (Timing)",
            "0": "❌ Quitter"
        }
        
        choice = ui.display_menu(main_menu)
        
        if choice == "0":
            ui.display_info("Merci d'avoir utilisé Crypto Simulator ! 👋")
            break
        
        elif choice == "1":
            handle_symmetric_attacks()
        
        elif choice == "2":
            handle_asymmetric_attacks()
        
        elif choice == "3":
            handle_special_attacks()
        
        ui.wait_for_key()


def handle_symmetric_attacks():
    """Gère les attaques sur chiffrement symétrique"""
    ui.clear_screen()
    ui.display_banner()
    
    submenu = {
        "1": "DES - Data Encryption Standard",
        "2": "AES - Advanced Encryption Standard",
        "0": "← Retour"
    }
    
    choice = ui.display_submenu("Attaques Symétrique", submenu)
    
    if choice == "1":
        des_attack.run()
    elif choice == "2":
        aes_attack.run()


def handle_asymmetric_attacks():
    """Gère les attaques sur chiffrement asymétrique"""
    ui.clear_screen()
    ui.display_banner()
    
    submenu = {
        "1": "RSA - Rivest-Shamir-Adleman",
        "2": "ECC - Elliptic Curve Cryptography",
        "0": "← Retour"
    }
    
    choice = ui.display_submenu("Attaques Asymétrique", submenu)
    
    if choice == "1":
        rsa_attack.run()
    elif choice == "2":
        ecc_attack.run()


def handle_special_attacks():
    """Gère les attaques spéciales"""
    ui.clear_screen()
    ui.display_banner()
    
    submenu = {
        "1": "Timing Attack - Analyse des temps d'exécution",
        "0": "← Retour"
    }
    
    choice = ui.display_submenu("Attaques Spéciales", submenu)
    
    if choice == "1":
        timing_attack.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ui.display_warning("\n\nInterruption par l'utilisateur (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        ui.display_error(f"Erreur fatale: {e}")
        sys.exit(1)
