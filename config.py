"""
Configuration pour AttackSim
"""

import os
import platform
from pathlib import Path

# Configuration globale
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Configuration matplotlib selon l'OS
def configure_matplotlib():
    """Configure matplotlib selon l'environnement"""
    import matplotlib
    
    # Détection de l'environnement
    if os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS'):
        # Environnement CI/CD
        matplotlib.use('Agg')
        return 'Agg'
    elif platform.system() == 'Darwin':  # macOS
        try:
            matplotlib.use('TkAgg')
            return 'TkAgg'
        except:
            matplotlib.use('Agg')
            return 'Agg'
    elif platform.system() == 'Windows':
        try:
            matplotlib.use('TkAgg')
            return 'TkAgg'
        except:
            matplotlib.use('Agg')
            return 'Agg'
    else:  # Linux
        # Teste si on a un display
        if os.environ.get('DISPLAY'):
            try:
                matplotlib.use('TkAgg')
                return 'TkAgg'
            except:
                matplotlib.use('Agg')
                return 'Agg'
        else:
            matplotlib.use('Agg')
            return 'Agg'

# Configuration des chemins
def ensure_directories():
    """S'assure que tous les dossiers existent"""
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

# Configuration des permissions
def check_permissions():
    """Vérifie les permissions d'écriture"""
    test_files = [
        REPORTS_DIR / ".test_write",
        DATA_DIR / ".test_write"
    ]
    
    permissions_ok = True
    for test_file in test_files:
        try:
            test_file.touch()
            test_file.unlink()
        except PermissionError:
            permissions_ok = False
            break
    
    return permissions_ok

# Configuration du logging
TIMING_ITERATIONS = {
    'quick': 100,
    'normal': 1000,
    'precise': 5000
}

# Messages multilingues
MESSAGES = {
    'fr': {
        'setup_complete': '✅ Configuration terminée avec succès!',
        'permission_error': '❌ Erreur de permissions d\'écriture',
        'matplotlib_backend': 'Backend matplotlib: {}',
    },
    'en': {
        'setup_complete': '✅ Setup completed successfully!',
        'permission_error': '❌ Write permission error',
        'matplotlib_backend': 'Matplotlib backend: {}',
    }
}

def get_message(key, lang='fr'):
    """Récupère un message dans la langue demandée"""
    return MESSAGES.get(lang, MESSAGES['fr']).get(key, key)
