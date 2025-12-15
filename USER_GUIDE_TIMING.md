# 🕐 Guide d'Utilisation - Timing Attacks Interactifs

## 🎯 Vue d'ensemble

Les modules **Timing Attack** permettent maintenant d'utiliser **vos propres données** pour les démonstrations ! Plus besoin de se contenter des exemples prédéfinis. 

## 📁 Formats de Fichiers Supportés

### 1. **Secret pour Attaque de Chaînes** (`secret.txt`)
```
MonMotDePasseSecret123!
```
- **Format** : Texte simple, une ligne
- **Contenu** : Le secret que vous voulez faire découvrir par l'attaque
- **Exemple** : `secret_example.txt`

### 2. **Paramètres RSA** (`rsa_params.txt`)
```
61,53
```
- **Format** : `p,q` (deux nombres premiers séparés par une virgule)
- **Contenu** : Nombres premiers pour générer les clés RSA
- **Recommandation** : Utilisez des petits nombres premiers pour la démo (p,q < 1000)
- **Exemple** : `rsa_params_example.txt`

### 3. **Messages RSA** (`messages.txt`)
```
123
456
789
1000
2000
```
- **Format** : Un message par ligne
- **Contenu** : Messages à chiffrer/déchiffrer pour l'analyse temporelle
- **Contrainte** : Messages entre 2 et n-1 (où n = p×q)
- **Exemple** : `messages_example.txt`

### 4. **Valeurs Test Cache** (`test_values.txt`)
```
0
4
8
12
15
```
- **Format** : Une valeur par ligne
- **Contenu** : Valeurs d'entrée pour la S-box AES (0-255)
- **Usage** : Test des variations de cache timing
- **Exemple** : `test_values_example.txt`

## 🎮 Mode d'Emploi

### **Étape 1 : Préparer vos données**

#### Option A : Utiliser l'Assistant Intégré
```
Menu Timing Attack → 6 - 🛠️ Créer des Fichiers de Données
```
L'assistant vous guide pour créer vos propres fichiers.

#### Option B : Créer les Exemples
```
Menu Timing Attack → 7 - 📁 Créer Exemples de Fichiers  
```
Génère automatiquement tous les fichiers d'exemple.

#### Option C : Créer Manuellement
Créez vos fichiers avec les formats ci-dessus.

### **Étape 2 : Lancer les Attaques**

#### **🔤 Attaque sur Comparaison de Chaînes**
1. Menu → `1 - Attaque sur Comparaison de Chaînes`
2. Choisir le mode :
   - `1` - Exemple prédéfini (rapide)
   - `2` - Saisir votre secret à la volée
   - `3` - Charger depuis un fichier
3. Choisir le charset :
   - `1` - Lettres + chiffres (rapide)
   - `2` - Complet avec symboles
   - `3` - Charset personnalisé

#### **🔐 Attaque Temporelle RSA**
1. Menu → `2 - Attaque Temporelle RSA`
2. Choisir les paramètres :
   - `1` - Exemple simple (p=61, q=53)
   - `2` - Saisir vos propres p,q
   - `3` - Charger depuis fichier
3. Choisir les messages :
   - `1` - Messages aléatoires
   - `2` - Saisir vos messages
   - `3` - Charger depuis fichier

#### **💾 Attaque Cache Timing**
1. Menu → `3 - Attaque Cache Timing`
2. Choisir les valeurs :
   - `1` - Valeurs 0-15 (standard)
   - `2` - Plage personnalisée
   - `3` - Valeurs spécifiques
   - `4` - Charger depuis fichier
3. Définir le nombre d'itérations (10-5000)

## 💡 **Exemples Concrets d'Utilisation**

### **Scénario 1 : Test avec votre mot de passe**
```bash
# Créer votre fichier secret
echo "VotreMotDePasse2025!" > mon_secret.txt

# Lancer l'attaque
Menu → 1 → 3 → mon_secret.txt
```

### **Scénario 2 : RSA avec vos paramètres**
```bash
# Créer vos paramètres RSA
echo "97,101" > mes_params.txt

# Créer vos messages de test
echo -e "50\n150\n200\n250\n500" > mes_messages.txt

# Lancer l'attaque
Menu → 2 → 3 → mes_params.txt → 3 → mes_messages.txt
```

### **Scénario 3 : Cache timing ciblé**
```bash
# Tester des valeurs spécifiques
echo -e "0\n1\n4\n5\n16\n17" > mes_valeurs.txt

# Lancer l'attaque
Menu → 3 → 4 → mes_valeurs.txt → 1000 itérations
```

## 📊 **Export des Résultats**

Tous les résultats sont automatiquement exportables :
- **Rapports** : `timing_attack_report_YYYYMMDD_HHMMSS.md`
- **Graphiques** : `timing_comparison_YYYYMMDD_HHMMSS.png`
- **Données brutes** : `timing_results_YYYYMMDD_HHMMSS.txt`

## 🔧 **Conseils d'Optimisation**

### **Pour les Démonstrations Rapides :**
- Utilisez des secrets courts (< 10 caractères)
- RSA avec petits premiers (p,q < 200)
- Cache timing avec peu de valeurs (< 20)
- Réduisez les itérations pour les tests rapides

### **Pour les Analyses Approfondies :**
- Secrets plus longs pour voir l'effet scaling
- Plus d'itérations (1000+) pour la précision statistique
- Gammes de valeurs étendues pour cache timing
- Plusieurs jeux de paramètres RSA pour comparaison

### **Pour l'Enseignement :**
- Préparez des fichiers avec des "secrets" pédagogiques
- Utilisez des paramètres RSA avec patterns reconnaissables
- Créez des scénarios progressifs (facile → difficile)

## 🚨 **Limitations et Sécurité**

### **Limitations Techniques :**
- RSA limité à de petites clés (pour la démo)
- Timing artificiel (simulation des fuites)
- Cache timing simplifié (pas de vrai cache)

### **Sécurité :**
- ⚠️ **Ne jamais utiliser de vrais secrets sensibles !**
- Les fichiers sont créés en texte brut
- Destiné uniquement à l'éducation/formation

## 📚 **Cas d'Usage Pédagogiques**

### **1. Cours de Cryptographie**
- Démonstration des canaux auxiliaires
- Comparaison vulnérable vs sécurisé
- Impact des paramètres sur la sécurité

### **2. TP Sécurité**
- Analyse de code vulnérable
- Mesure quantitative des fuites
- Conception de contre-mesures

### **3. Projets Étudiants**
- Implémentation de variants d'attaque
- Analyse statistique des résultats
- Proposition d'améliorations

---

## 🎯 **Résumé des Améliorations**

✅ **Import de données personnalisées** (fichiers + saisie)  
✅ **Assistant de création** de fichiers de test  
✅ **Export automatique** des résultats  
✅ **Validation** des données d'entrée  
✅ **Interface intuitive** avec choix multiples  
✅ **Gestion d'erreurs** robuste  
✅ **Exemples prêts à l'emploi**  

**Vos timing attacks sont maintenant 100% personnalisables ! 🚀**
