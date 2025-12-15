# Crypto Simulator

Simulateur d'attaques cryptographiques - Projet ESGI

## 🚀 Installation et Configuration

### 1. Prérequis
- Python 3.8+ 
- Git

### 2. Installation rapide
```bash
# Cloner le dépôt
git clone <URL_DU_REPO>
cd AttackSim

# Configuration automatique (recommandé)
python setup.py

# OU installation manuelle :
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Lancement
```bash
python main.py
```

### 4. Structure des dossiers
- `data/` - Fichiers d'entrée utilisateur (mots, paramètres RSA, etc.)
- `reports/` - Rapports et graphiques générés automatiquement
- `src/` - Code source du simulateur

## 🎯 Description

Application CLI interactive permettant de simuler différentes attaques cryptographiques sur des algorithmes de chiffrement symétrique et asymétrique.

## ✨ Fonctionnalités

### 🔐 Attaques Symétrique (🚧 ÉQUIPE A)

**Attaque par Force Brute sur DES et AES**

**À implémenter dans :**
- `src/attacks/symmetric/des_attack.py`
- `src/attacks/symmetric/aes_attack.py`

**Spécifications attendues :**
- Attaque par force brute sur différentes longueurs de clés
- DES : 56 bits (clés réduites pour simulation : 8-24 bits)
- AES : 128, 192, 256 bits (clés réduites pour simulation : 16-40 bits)
- Mesure du temps de cassage selon la taille de clé
- Estimation du nombre de clés testées par seconde
- Graphiques comparatifs (temps vs taille de clé)
- Simulation de chiffrement/déchiffrement
- Mode avec clé connue pour validation
- Export des résultats en PNG

**Inspiration :** Voir `rsa_attack.py` pour la structure (benchmark, graphiques, modes)

### 🔑 Attaques Asymétrique - RSA (✅ IMPLÉMENTÉ)

**Attaque par Factorisation sur RSA avec petites clés**

- **3 Méthodes de factorisation :**
  - Division d'essai (Force brute)
  - Algorithme de Fermat
  - Algorithme rho de Pollard

- **3 Modes d'utilisation :**
  - Attaque simple sur clé générée aléatoirement
  - Benchmark comparatif des méthodes
  - Mode personnalisé (vos propres p et q)

- **Fonctionnalités :**
  - Génération de clés RSA (16-64 bits)
  - Tests de primalité (Miller-Rabin)
  - Mesure de performance
  - Graphiques comparatifs (PNG)
  - Interface CLI élégante avec Rich

### ⏱️ Attaques Spéciales & ECC (🚧 ÉQUIPE C)

**1. Timing Attack - Attaque par Canal Auxiliaire**

**À implémenter dans :**
- `src/attacks/special/timing_attack.py`

**Spécifications attendues :**
- Simulation d'une implémentation vulnérable (RSA, AES, comparaison de mots de passe)
- Mesure précise des temps d'exécution (microseconde)
- Détection de corrélations entre temps et bits secrets
- Visualisation des différences de timing
- Démonstration de récupération d'information
- Comparaison : implémentation vulnérable vs sécurisée (constant-time)
- Graphiques montrant les fuites temporelles
- Export des résultats

**2. Analyse de Résistance des Courbes Elliptiques**

**À implémenter dans :**
- `src/attacks/asymmetric/ecc_attack.py`

**Spécifications attendues :**
- Implémentation de courbes elliptiques (secp256k1, P-256, etc.)
- Attaque sur courbes faibles (petits ordres, points singuliers)
- Analyse de résistance : attaque de Pollard Rho pour ECDLP
- Comparaison de la sécurité selon les paramètres de courbe
- Estimation de la complexité d'attaque
- Visualisation des courbes elliptiques
- Benchmark de génération de clés et signatures
- Export des résultats et graphiques

## 📦 Installation

### Prérequis
- Python 3.10+
- pip

### 1. Cloner le dépôt
```bash
git clone git@github-esgi:xAMA0x/AttackSim.git
cd AttackSim
```

### 2. Créer l'environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## 🚀 Exécution

```bash
source venv/bin/activate  # Si pas déjà activé
python main.py
```

## 📊 Exemple d'utilisation - Attaque RSA

```
Menu Principal > 2. Attaques Asymétrique > 1. RSA

Options:
  1. Attaque simple (clé aléatoire)
  2. Benchmark comparatif
  3. Mode personnalisé

Exemple de résultat:
╔══════════════╦════════╗
║ Paramètre    ║ Valeur ║
╠══════════════╬════════╣
║ p            ║ 211    ║
║ q            ║ 241    ║
║ n (p×q)      ║ 50851  ║
╚══════════════╩════════╝

Résultats des Attaques:
├─ Division d'essai : ✓ (0.03ms)
├─ Fermat           : ✓ (0.01ms)
└─ Pollard Rho      : ✓ (0.06ms)
```

## 📝 Workflow Git

### Pour commencer à travailler
```bash
# 1. Cloner le dépôt
git clone git@github-esgi:xAMA0x/AttackSim.git
cd AttackSim

# 2. Créer une branche pour votre équipe
git checkout -b feature/equipe-A-symmetric  # Équipe A
git checkout -b feature/equipe-C-special    # Équipe C

# 3. Installer l'environnement
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Pendant le développement
```bash
# Commits réguliers
git add src/attacks/symmetric/des_attack.py
git commit -m "WIP: DES brute force - génération clés"
git push origin feature/equipe-A-symmetric

# Tester votre code
python main.py
```

### Quand votre module est terminé
```bash
# Commit final
git add .
git commit -m "Feat: Complete DES/AES brute force attack

- DES: 8-24 bit keys with timing benchmark
- AES: 16-40 bit keys with parallel modes
- Graphical comparison charts
- Full CLI integration

Module ready for demonstration"

git push origin feature/equipe-A-symmetric

# Ensuite : créer une Pull Request sur GitHub
```

## 🎓 Ressources Utiles

### Pour Équipe A (Symétrique)
- [PyCryptodome Documentation](https://pycryptodome.readthedocs.io/) - Implémentation DES/AES
- [Cryptography Library](https://cryptography.io/) - Alternative moderne
- Exemple de référence : `src/attacks/asymmetric/rsa_attack.py`

### Pour Équipe C (Timing & ECC)
- [Timing Attack Tutorial](https://en.wikipedia.org/wiki/Timing_attack)
- [ECC Math](https://andrea.corbellini.name/2015/05/17/elliptic-curve-cryptography-a-gentle-introduction/)
- [tinyec Library](https://github.com/alexmgr/tinyec) - Courbes elliptiques en Python
- Python `time.perf_counter()` pour mesures précises

### Bibliothèques Recommandées
```python
# Déjà installées (requirements.txt)
import rich              # Interface CLI
import matplotlib.pyplot  # Graphiques
import numpy             # Calculs numériques

# À ajouter si besoin (mettre dans requirements.txt)
# from Crypto.Cipher import DES, AES  # PyCryptodome
# import secrets                       # Génération aléatoire sécurisée
# import hashlib                       # Fonctions de hash
```

## 🧪 Tests & Validation

### Checklist avant commit
- [ ] Le module se lance sans erreur
- [ ] L'interface est cohérente avec le reste (Rich)
- [ ] Les graphiques sont générés dans `reports/`
- [ ] Le code est commenté (docstrings)
- [ ] Les temps d'exécution sont mesurés
- [ ] Au moins 2 modes/options disponibles
- [ ] Testé avec différentes tailles de paramètres

### Commande de test rapide
```bash
# Test de votre module via le menu
source venv/bin/activate
python main.py

# Vérifier qu'il n'y a pas d'erreurs Python
python -m py_compile src/attacks/symmetric/des_attack.py
```

## 📁 Structure

```
AttackSim/
├── main.py                           # Point d'entrée
├── requirements.txt                  # Dépendances
├── README.md                         # Documentation
├── reports/                          # Exports graphiques (PNG)
└── src/
    ├── core/
    │   ├── ui.py                    # Interface CLI (Rich)
    │   └── utils.py                 # Utilitaires communs
    └── attacks/
        ├── symmetric/               # 🚧 ÉQUIPE A
        │   ├── des_attack.py       # Force brute DES
        │   └── aes_attack.py       # Force brute AES
        ├── asymmetric/
        │   ├── rsa_attack.py       # ✅ Factorisation RSA (COMPLET)
        │   └── ecc_attack.py       # 🚧 ÉQUIPE C - Résistance ECC
        └── special/                 # 🚧 ÉQUIPE C
            └── timing_attack.py    # Canal auxiliaire (timing)
```

## 🛠️ Développement

### Architecture modulaire
- Chaque module d'attaque expose une fonction `run()`
- Le `main.py` orchestre les menus et appelle les modules
- `core/ui.py` gère l'affichage avec Rich
- `core/utils.py` fournit les utilitaires (Timer, graphiques, etc.)

### Exemple de structure d'un module

```python
"""
Mon Module d'Attaque
"""
from rich.console import Console
import matplotlib.pyplot as plt
from core.utils import Timer, save_plot, format_time

console = Console()

def run():
    """Point d'entrée du module"""
    console.print("\n[bold cyan]═══ MA SUPER ATTAQUE ═══[/bold cyan]\n")
    
    # 1. Afficher le menu des options
    # 2. Récupérer les paramètres utilisateur
    # 3. Exécuter l'attaque avec Timer
    # 4. Afficher les résultats avec Rich
    # 5. Générer et sauvegarder les graphiques
```

### Utilitaires disponibles (`core/utils.py`)

```python
from core.utils import (
    Timer,              # Chronomètre précis
    save_plot,          # Sauvegarde matplotlib -> PNG
    format_time,        # Format lisible (2.5s, 1m 30s)
    format_number,      # Format avec espaces (1 000 000)
    ensure_reports_dir  # Crée le dossier reports/
)
```

### Interface utilisateur (`core/ui.py`)

```python
from core.ui import (
    display_banner,     # Banner de l'app
    display_menu,       # Menu avec Rich Table
    display_success,    # Message ✓ vert
    display_error,      # Message ✗ rouge
    display_info,       # Message ℹ bleu
    display_warning,    # Message ⚠ jaune
    confirm_action,     # Demande o/n
    wait_for_key        # "Appuyez sur Entrée..."
)
```

## 👥 Répartition des Tâches

### **ÉQUIPE A** - Chiffrement Symétrique
**Responsable :** [Nom]
- `src/attacks/symmetric/des_attack.py` - Force brute sur DES
- `src/attacks/symmetric/aes_attack.py` - Force brute sur AES
- **Livrables :** Code + Graphiques + Tests validés

### **ÉQUIPE B** - Chiffrement Asymétrique RSA
**Responsable :** Anthony (xAMA0x)
- ✅ `src/attacks/asymmetric/rsa_attack.py` - **TERMINÉ**
- Factorisation (Division, Fermat, Pollard)
- 3 modes + Benchmark + Graphiques

### **ÉQUIPE C** - Attaques Spéciales & ECC
**Responsable :** [Nom]
- `src/attacks/special/timing_attack.py` - Canal auxiliaire (timing)
- `src/attacks/asymmetric/ecc_attack.py` - Analyse résistance courbes elliptiques
- **Livrables :** Code + Graphiques + Démonstrations

## 📜 Licence

Projet académique - ESGI 2025
