# Crypto Simulator

Simulateur d'attaques cryptographiques - Projet ESGI

## 🎯 Description

Application CLI interactive permettant de simuler différentes attaques cryptographiques sur des algorithmes de chiffrement symétrique et asymétrique.

## ✨ Fonctionnalités

### 🔐 Attaques Asymétrique - RSA (✅ IMPLÉMENTÉ)

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

### 🔐 Attaques Symétrique (🚧 EN ATTENTE)
- DES - Data Encryption Standard
- AES - Advanced Encryption Standard

### ⏱️ Attaques Spéciales (🚧 EN ATTENTE)
- Timing Attack - Analyse des temps d'exécution

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

## 📁 Structure

```
AttackSim/
├── main.py                      # Point d'entrée
├── requirements.txt             # Dépendances
├── README.md                    # Documentation
├── reports/                     # Exports graphiques
└── src/
    ├── core/
    │   ├── ui.py               # Interface CLI (Rich)
    │   └── utils.py            # Utilitaires communs
    └── attacks/
        ├── symmetric/          # DES, AES (🚧)
        ├── asymmetric/
        │   ├── rsa_attack.py  # ✅ COMPLET
        │   └── ecc_attack.py  # 🚧
        └── special/            # Timing (🚧)
```

## 🛠️ Développement

### Architecture modulaire
- Chaque module d'attaque expose une fonction `run()`
- Le `main.py` orchestre les menus et appelle les modules
- `core/ui.py` gère l'affichage avec Rich
- `core/utils.py` fournit les utilitaires (Timer, graphiques, etc.)

### Ajouter une nouvelle attaque
1. Créer un fichier dans `src/attacks/[categorie]/`
2. Implémenter la fonction `run()`
3. Importer et référencer dans `main.py`

## 👥 Équipe

- **Équipe A** : Chiffrement Symétrique (DES, AES)
- **Équipe B** : Chiffrement Asymétrique (RSA ✅, ECC)
- **Équipe C** : Attaques Spéciales (Timing)

## 📜 Licence

Projet académique - ESGI 2025
