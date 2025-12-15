# Guide de Déploiement - AttackSim

## 🚀 Installation sur un nouveau poste

### 1. Prérequis système
- **Python 3.8+** (recommandé: 3.9+)
- **Git** 
- **Terminal/Console** 

### 2. Commandes d'installation

```bash
# 1. Cloner le dépôt
git clone <URL_DU_DEPOT>
cd AttackSim

# 2. Configuration automatique (RECOMMANDÉ)
python setup.py

# 3. Lancement
python main.py
```

### 3. Installation manuelle (si setup.py échoue)

```bash
# Créer environnement virtuel
python -m venv venv

# Activer l'environnement
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Créer les dossiers nécessaires
mkdir -p data reports

# Lancer le simulateur
python main.py
```

## 📁 Structure des dossiers

### Avant le premier lancement
```
AttackSim/
├── src/               # Code source
├── main.py            # Point d'entrée
├── requirements.txt   # Dépendances
├── setup.py          # Script de configuration
└── README.md         # Documentation
```

### Après configuration
```
AttackSim/
├── data/              # Fichiers d'entrée utilisateur
│   ├── exemple_mots.txt
│   ├── exemple_messages_rsa.txt
│   └── rsa_params.txt
├── reports/           # Rapports et graphiques générés
├── venv/             # Environnement virtuel Python
├── src/              # Code source
├── main.py           # Point d'entrée
├── requirements.txt  # Dépendances
├── setup.py         # Script de configuration
└── config.py        # Configuration environnement
```

## 🔧 Dépannage

### Problème: "Module not found"
```bash
# Réinstaller les dépendances
pip install -r requirements.txt

# Ou utiliser le setup automatique
python setup.py
```

### Problème: Permissions d'écriture
```bash
# Vérifier les permissions
ls -la

# Corriger si nécessaire (Linux/macOS)
chmod 755 data/ reports/
```

### Problème: Matplotlib
```bash
# Installation manuelle des dépendances graphiques (Ubuntu/Debian)
sudo apt-get install python3-tk

# macOS avec Homebrew
brew install python-tk

# Windows: Généralement inclus avec Python
```

### Problème: Import errors
```bash
# S'assurer d'être dans le bon dossier
cd AttackSim
pwd

# Vérifier la structure
ls -la src/
```

## 🧹 Nettoyage

```bash
# Nettoyer les fichiers temporaires
./cleanup.sh

# Ou manuellement:
rm -rf __pycache__/ 
rm -rf src/**/__pycache__/
rm -f reports/*.png reports/*.md
rm -f data/my_*
```

## 🔄 Mise à jour

```bash
# Récupérer les dernières modifications
git pull origin main

# Réinstaller si nécessaire
python setup.py
```

## 🎯 Tests de fonctionnement

Après installation, vous devriez pouvoir :

1. **Lancer le simulateur** : `python main.py`
2. **Voir le menu principal** avec 4 options
3. **Accéder aux attaques timing** (option 3)
4. **Générer des graphiques** dans `reports/`
5. **Importer des fichiers** depuis `data/`

### Test rapide
```bash
# Test configuration
python setup.py

# Test lancement (quitte immédiatement)
echo "0" | python main.py

# Si les deux fonctionnent, l'installation est réussie ✅
```

## 📞 Support

En cas de problème :
1. Vérifier que Python 3.8+ est installé : `python --version`
2. Vérifier que Git est installé : `git --version` 
3. S'assurer d'être dans le dossier AttackSim
4. Relancer `python setup.py`
5. Consulter les logs d'erreur
