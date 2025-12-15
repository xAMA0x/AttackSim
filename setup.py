#!/usr/bin/env python3
"""
Script de configuration pour AttackSim
Assure que l'environnement est correctement configuré après un git clone/pull
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Vérifie la version de Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        print(f"Version actuelle: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    return True


def create_directories():
    """Crée les dossiers nécessaires"""
    project_root = Path(__file__).parent
    directories = [
        "reports",
        "data",  # Pour les fichiers d'entrée utilisateur
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(exist_ok=True)
        print(f"✅ Dossier {directory}/ créé/vérifié")
        
        # Crée un .gitkeep si le dossier est vide
        if not any(dir_path.iterdir()):
            gitkeep_path = dir_path / ".gitkeep"
            gitkeep_path.touch()
            print(f"  📁 Fichier .gitkeep créé dans {directory}/")


def check_virtual_environment():
    """Vérifie si un environnement virtuel est actif"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Environnement virtuel actif")
        return True
    else:
        print("⚠️  Aucun environnement virtuel détecté")
        print("Recommandation: python -m venv venv && source venv/bin/activate")
        return False


def install_requirements():
    """Installe les dépendances"""
    requirements_path = Path(__file__).parent / "requirements.txt"
    
    if not requirements_path.exists():
        print("❌ Fichier requirements.txt introuvable")
        return False
    
    try:
        print("📦 Installation des dépendances...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_path)
        ], check=True, capture_output=True)
        print("✅ Dépendances installées")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False


def check_imports():
    """Vérifie que tous les modules requis sont importables"""
    required_modules = [
        "matplotlib",
        "numpy",
        "scipy",
        "seaborn",
        "rich",
        "tinyec",
        "sympy"
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Modules manquants: {', '.join(failed_imports)}")
        print("Exécutez: pip install -r requirements.txt")
        return False
    
    return True


def test_project_structure():
    """Teste la structure du projet"""
    project_root = Path(__file__).parent
    required_paths = [
        "src/__init__.py",
        "src/core/utils.py",
        "src/attacks/special/timing_attack.py",
        "src/attacks/asymmetric/ecc_attack.py",
        "main.py",
        "requirements.txt"
    ]
    
    missing_files = []
    
    for path_str in required_paths:
        path = project_root / path_str
        if path.exists():
            print(f"✅ {path_str}")
        else:
            print(f"❌ {path_str}")
            missing_files.append(path_str)
    
    if missing_files:
        print(f"\n❌ Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    return True


def test_matplotlib_backend():
    """Teste le backend matplotlib"""
    try:
        from config import configure_matplotlib
        backend = configure_matplotlib()
        print(f"✅ Matplotlib configuré avec le backend: {backend}")
        
        import matplotlib.pyplot as plt
        
        # Test de création d'un graphique simple
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.plot([1, 2, 3], [1, 4, 2])
        ax.set_title("Test")
        
        # Test de sauvegarde
        from src.core.utils import save_plot
        filepath = save_plot(fig, "test_setup")
        
        # Vérifie que le fichier a été créé
        if Path(filepath).exists():
            print("✅ Matplotlib et sauvegarde fonctionnent")
            # Supprime le fichier de test
            Path(filepath).unlink()
            return True
        else:
            print("❌ Problème avec la sauvegarde matplotlib")
            return False
            
    except Exception as e:
        print(f"❌ Erreur matplotlib: {e}")
        return False


def main():
    """Fonction principale de configuration"""
    print("🚀 Configuration d'AttackSim\n" + "=" * 50)
    
    success = True
    
    # Tests de base
    print("\n1. Vérification Python")
    success &= check_python_version()
    
    print("\n2. Structure du projet")
    success &= test_project_structure()
    
    print("\n3. Création des dossiers")
    create_directories()
    
    print("\n4. Environnement virtuel")
    check_virtual_environment()  # Warning seulement
    
    print("\n5. Installation des dépendances")
    if not check_imports():
        print("Installation automatique...")
        success &= install_requirements()
        
        # Nouvelle vérification
        print("Vérification post-installation:")
        success &= check_imports()
    
    print("\n6. Test matplotlib")
    success &= test_matplotlib_backend()
    
    print("\n" + "=" * 50)
    
    if success:
        print("✅ Configuration terminée avec succès!")
        print("\nPour démarrer le simulateur:")
        print("  python main.py")
    else:
        print("❌ Configuration incomplète")
        print("Veuillez corriger les erreurs ci-dessus")
        sys.exit(1)


if __name__ == "__main__":
    main()
