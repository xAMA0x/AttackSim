# Crypto Simulator

Simulateur d'attaques cryptographiques - Projet ESGI

## 🎯 Description

Application CLI interactive permettant de simuler différentes attaques cryptographiques sur des algorithmes de chiffrement symétrique et asymétrique. Ce projet a pour but pédagogique d'illustrer les vulnérabilités de certains algorithmes et l'importance de l'utilisation de paramètres sécurisés.

## ✨ Fonctionnalités

### 🔐 Attaques Symétrique

**Attaque par Force Brute sur DES et AES**
- Attaque par force brute sur différentes longueurs de clés.
- DES : Clés réduites pour simulation (8-24 bits).
- AES : Clés réduites pour simulation (16-40 bits).
- Mesure du temps de cassage et estimation du nombre de clés testées par seconde.
- Graphiques comparatifs (temps vs taille de clé).

### 🔑 Attaques Asymétrique - RSA

**Attaque par Factorisation sur RSA avec petites clés**
- **3 Méthodes de factorisation :**
  - Division d'essai (Force brute)
  - Algorithme de Fermat
  - Algorithme rho de Pollard
- **Fonctionnalités :**
  - Génération de clés RSA (16-64 bits).
  - Tests de primalité (Miller-Rabin).
  - Graphiques comparatifs.

### ⏱️ Attaques Spéciales & ECC

**1. Timing Attack - Attaque par Canal Auxiliaire**
- Simulation d'une implémentation vulnérable.
- Mesure précise des temps d'exécution.
- Démonstration de récupération d'information via analyse temporelle.

**2. Analyse de Résistance des Courbes Elliptiques**
- Implémentation de courbes elliptiques.
- Attaque sur courbes faibles (petits ordres, points singuliers).
- Analyse de résistance : attaque de Pollard Rho pour ECDLP.

## 🚀 Installation et Utilisation

### Prérequis
- Python 3.8+

### Installation

```bash
# Cloner le dépôt
git clone <URL_DU_REPO>
cd AttackSim

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement

```bash
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

## 📁 Structure du projet

- `data/` - Fichiers d'entrée utilisateur (mots, paramètres RSA, etc.)
- `reports/` - Rapports et graphiques générés automatiquement
- `src/` - Code source du simulateur
    - `core/` - Composants centraux (UI, Utils)
    - `attacks/` - Modules d'attaques (Symétrique, Asymétrique, Spécial)

## 📜 Licence

Projet académique - ESGI 2025

