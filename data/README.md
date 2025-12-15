# Dossier pour les fichiers de données utilisateur

Ce dossier contient les fichiers de données que les utilisateurs peuvent importer dans le simulateur.

## Exemples de fichiers supportés

### Pour les attaques timing:

1. **Fichiers de mots/phrases** (`.txt`):
   - Un mot ou une phrase par ligne
   - Utilisé pour les attaques de comparaison de chaînes

2. **Fichiers de messages RSA** (`.txt`):
   - Un message par ligne (texte ou nombres)
   - Utilisé pour les attaques timing RSA

3. **Fichiers de données cache** (`.txt`):
   - Données pour simuler les attaques par canal auxiliaire

## Instructions

1. Placez vos fichiers dans ce dossier
2. Lancez le simulateur avec `python main.py`
3. Sélectionnez l'attaque timing appropriée
4. Choisissez l'option d'import de fichier
5. Entrez le nom du fichier (par exemple: `mes_mots.txt`)

Le simulateur cherchera automatiquement le fichier dans ce dossier.
