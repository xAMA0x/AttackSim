# 🔐 Guide d'Implémentation - Attaques Timing et ECC

## 📋 Vue d'ensemble

Ce document explique l'implémentation des modules d'**attaque par canal auxiliaire (timing attack)** et d'**analyse de résistance des courbes elliptiques** dans le simulateur d'attaques cryptographiques.

## 🕐 Module Timing Attack

### 🎯 Objectifs Pédagogiques

- Comprendre les **canaux auxiliaires** en cryptographie
- Démontrer comment des **différences de temps** révèlent des informations secrètes
- Comparer implémentations **vulnérables vs sécurisées**
- Mesurer et visualiser les **fuites temporelles**

### 🔧 Implémentations Vulnérables

#### 1. Comparaison de Chaînes Non Constant-Time
```python
def vulnerable_string_compare(secret: str, guess: str) -> bool:
    for i in range(len(secret)):
        if secret[i] != guess[i]:
            return False  # ❌ Arrêt précoce = fuite temporelle
        time.sleep(0.0001)  # Simulation opération coûteuse
    return True
```

**Pourquoi c'est vulnérable :**
- L'algorithme s'arrête au premier caractère différent
- Plus le préfixe est correct, plus l'exécution est longue
- Un attaquant peut déduire le secret caractère par caractère

#### 2. Exponentiation RSA Naïve
```python
def vulnerable_rsa_decrypt(ciphertext: int, d: int, n: int) -> int:
    result = 1
    while exponent > 0:
        if exponent & 1:  # ❌ Branchement dépendant de la clé
            result = (result * base) % n
            time.sleep(0.00001)  # Multiplication "plus lente"
        base = (base * base) % n
        exponent >>= 1
    return result
```

**Pourquoi c'est vulnérable :**
- Le nombre d'opérations dépend du nombre de bits à 1 dans l'exposant
- Un attaquant peut déduire des informations sur la clé privée `d`

#### 3. Lookup Table AES Dépendant de la Clé
```python
def vulnerable_aes_sbox_lookup(byte_val: int) -> int:
    sbox = [0x63, 0x7c, 0x77, ...]  # S-box AES
    if byte_val % 4 == 0:  # ❌ Cache miss simulé
        time.sleep(0.00005)
    return sbox[byte_val % len(sbox)]
```

**Pourquoi c'est vulnérable :**
- Les accès mémoire ont des temps variables (cache hits/misses)
- Le pattern d'accès révèle des informations sur les données traitées

### 🛡️ Contre-mesures Implémentées

#### 1. Comparaison Constant-Time
```python
def secure_string_compare(secret: str, guess: str) -> bool:
    result = 0
    for i in range(len(secret)):
        result |= ord(secret[i]) ^ ord(guess[i])
        time.sleep(0.0001)  # ✅ TOUJOURS exécuté
    return result == 0
```

#### 2. Exponentiation avec Blinding
```python
def secure_rsa_decrypt(ciphertext: int, d: int, n: int) -> int:
    # ✅ Masquage aléatoire pour cacher les patterns
    r = random.randint(2, n-1)
    r_inv = pow(r, -1, n)
    blinded_c = (ciphertext * pow(r, 65537, n)) % n
    result = pow(blinded_c, d, n)
    return (result * r_inv) % n
```

### 📊 Mesures et Analyses

- **Mesure précise** : `time.perf_counter()` avec haute résolution
- **Analyse statistique** : moyenne, écart-type, percentiles
- **Détection d'outliers** : identification des valeurs suspectes (>2σ)
- **Visualisations** : box plots, heatmaps, comparaisons temporelles

## 🔮 Module ECC (Courbes Elliptiques)

### 🎯 Objectifs Pédagogiques

- Comprendre les **courbes elliptiques** en cryptographie
- Analyser la **résistance** selon les paramètres
- Démontrer des **attaques sur courbes faibles**
- Implémenter l'algorithme **Pollard Rho** pour ECDLP

### 📐 Implémentation Mathématique

#### Structure des Courbes
```python
@dataclass
class EllipticCurve:
    a: int          # Coefficient a dans y² = x³ + ax + b
    b: int          # Coefficient b
    p: int          # Module premier
    name: str       # Nom de la courbe
```

#### Arithmétique des Points
```python
class EllipticCurveArithmetic:
    @staticmethod
    def point_add(P: ECPoint, Q: ECPoint) -> ECPoint:
        # Addition de points : P + Q = R
        # Gestion des cas spéciaux (infini, doublement, etc.)
        
    @staticmethod  
    def scalar_mult(k: int, P: ECPoint) -> ECPoint:
        # Multiplication scalaire : k*P
        # Méthode binaire efficace
```

### 🏗️ Courbes Implémentées

#### Courbes Standards (Sécurisées)
- **secp256k1** : Utilisée par Bitcoin (256 bits)
- **P-256** : NIST recommandée (256 bits)

#### Courbes Faibles (Pour Démonstration)
- **TinyWeak1** : p=97, facilement cassable
- **SmallWeak** : p=1009, attaque Pollard Rho possible

### ⚔️ Attaque Pollard Rho pour ECDLP

#### Principe
Résout le **Problème du Logarithme Discret Elliptique** : trouver `k` tel que `Q = k*P`

```python
def pollard_rho_ecdlp(P: ECPoint, Q: ECPoint, n: int) -> Optional[int]:
    # Algorithme de Floyd (tortue et lièvre)
    # Détection de collision dans une séquence pseudoaléatoire
    # Complexité : O(√n) au lieu de O(n) pour la force brute
```

#### Fonction d'Itération
```python
def iterate_function(R, a, b):
    partition = R.x % 3
    if partition == 0:
        return (2*R, 2*a, 2*b)      # Doublement
    elif partition == 1:  
        return (R+P, a+1, b)        # Addition P
    else:
        return (R+Q, a, b+1)        # Addition Q
```

### 📈 Analyses de Sécurité

#### Estimation de la Force
```python
def analyze_curve_security(curve_params):
    key_bits = p.bit_length()
    security_bits = key_bits // 2  # Approximation Pollard Rho
    
    if security_bits < 40:
        return "TRÈS FAIBLE"
    elif security_bits < 80:
        return "FAIBLE"
    # ... etc
```

#### Classification des Niveaux
- **TRÈS FAIBLE** (<40 bits) : Cassable en minutes
- **FAIBLE** (40-80 bits) : Cassable en heures/jours
- **ACCEPTABLE** (80-128 bits) : Résistant aux attaques classiques
- **FORT** (>128 bits) : Sécurité quantique considérée

## 🔬 Fonctionnalités Avancées

### Timing Attack
- ✅ **Attaque de récupération de mot de passe** caractère par caractère
- ✅ **Analyse RSA** avec détection des patterns d'exponentiation
- ✅ **Cache timing sur AES** avec détection d'outliers
- ✅ **Comparaisons vulnérable/sécurisé** avec métriques
- ✅ **Visualisations** (box plots, heatmaps, distributions)
- ✅ **Rapports automatiques** en Markdown

### ECC Analysis
- ✅ **Implémentation complète** d'arithmétique elliptique
- ✅ **Courbes standards** (secp256k1, P-256) et faibles
- ✅ **Attaque Pollard Rho** fonctionnelle
- ✅ **Calcul d'ordre** de courbe (méthode naïve)
- ✅ **Benchmarks de performance** 
- ✅ **Visualisations** des courbes (petites tailles)
- ✅ **Analyse comparative** de sécurité
- ✅ **Rapports détaillés** avec recommandations

## 🎮 Utilisation

### Lancement
```bash
cd AttackSim
source venv/bin/activate
python main.py
```

### Navigation
1. **Menu Principal** → `3` (Attaques Spéciales)
2. **Menu Principal** → `2` (Attaques Asymétriques) → `2` (ECC)

### Exemples de Sortie

#### Timing Attack
```
🎯 Attaque sur Comparaison de Chaînes
Secret à découvrir : 21 caractères
Position  1: 'S'
Position  5: 'Super' 
Position 10: 'SuperSecre'
✅ Mot de passe découvert : 'SuperSecretPassword123!'
```

#### ECC Analysis  
```
🎯 Attaque sur Courbe Faible
Courbe: TinyWeak1 - y² ≡ x³ + 2x + 3 (mod 97)
Ordre de la courbe: 100
Clé privée (secrète): 42
🚀 Lancement de l'attaque Pollard Rho...
✅ Clé privée récupérée: 42
✅ Correct: True
Temps d'attaque: 0.023s
```

## 📚 Concepts Pédagogiques Couverts

### Timing Attacks
- **Canaux auxiliaires** en cryptographie
- **Corrélation temps/information secrète**
- **Implémentations constant-time**
- **Contre-mesures** (blinding, masquage)
- **Mesures statistiques** et détection d'anomalies

### Courbes Elliptiques
- **Géométrie** des courbes elliptiques
- **Arithmétique modulaire** et groupes
- **Problème du logarithme discret**
- **Algorithmes d'attaque** (Pollard Rho)
- **Analyse de complexité** et sécurité pratique
- **Standards cryptographiques** industriels

## 🛠️ Architecture Technique

### Dépendances Ajoutées
```python
scipy>=1.10.0      # Statistiques avancées
seaborn>=0.12.0    # Visualisations
tinyec>=0.4.0      # Courbes elliptiques
sympy>=1.11.0      # Mathématiques symboliques
```

### Structure des Modules
```
src/attacks/special/timing_attack.py      # 600+ lignes
src/attacks/asymmetric/ecc_attack.py      # 800+ lignes
```

### Intégration
- **Interface unified** avec le simulateur existant
- **Style cohérent** avec les modules RSA/AES
- **Gestion d'erreurs** robuste
- **Rapports automatiques** dans `/reports/`

## 🎓 Valeur Pédagogique

### Pour les Étudiants
- **Compréhension pratique** des attaques par canaux auxiliaires
- **Implémentation concrète** d'algorithmes cryptographiques
- **Analyse comparative** vulnérable vs sécurisé
- **Visualisation** des concepts abstraits
- **Mesures quantitatives** de sécurité

### Pour les Enseignants
- **Démonstrations interactives** en cours
- **Exercices pratiques** d'implémentation
- **Analyse de cas réels** (Bitcoin, TLS)
- **Recommandations** pour développeurs
- **Rapports automatiques** pour évaluation

---

## 🔗 Références

- [NIST SP 800-186](https://csrc.nist.gov/publications/detail/sp/800-186/final) - Recommandations ECC
- [Kocher et al. (1996)](https://link.springer.com/chapter/10.1007/3-540-68697-5_9) - Timing Attacks on RSA
- [Pollard (1978)](https://www.ams.org/journals/mcom/1978-32-143/S0025-5718-1978-0491431-9/) - Méthode Rho
- [Bitcoin secp256k1](https://en.bitcoin.it/wiki/Secp256k1) - Standards Bitcoin

**Implémentation terminée avec succès ! 🎉**
