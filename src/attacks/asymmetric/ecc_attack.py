"""
ECC Attack Module - Analyse de Résistance des Courbes Elliptiques
Implémente l'analyse de sécurité des courbes elliptiques et démontre diverses attaques
"""
import time
import random
import math
import hashlib
from typing import Tuple, List, Dict, Optional, NamedTuple
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich import box
from pathlib import Path
import sys

# Import des utilitaires
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from core.utils import Timer, save_plot, format_time, format_number

console = Console()

# ═══════════════════════════════════════════════════════════════
#  IMPLÉMENTATION DES COURBES ELLIPTIQUES
# ═══════════════════════════════════════════════════════════════

@dataclass
class EllipticCurve:
    """Représentation d'une courbe elliptique y² = x³ + ax + b (mod p)"""
    a: int
    b: int
    p: int  # Modulo premier
    name: str = "Custom"
    
    def __post_init__(self):
        """Vérifie que la courbe est non-singulière"""
        discriminant = (4 * self.a**3 + 27 * self.b**2) % self.p
        if discriminant == 0:
            raise ValueError("Courbe singulière : discriminant = 0")

@dataclass
class ECPoint:
    """Point sur une courbe elliptique"""
    x: Optional[int]
    y: Optional[int]
    curve: EllipticCurve
    
    def __post_init__(self):
        """Vérifie que le point appartient à la courbe"""
        if self.is_infinity():
            return
        
        if not self.is_on_curve():
            raise ValueError(f"Point ({self.x}, {self.y}) n'est pas sur la courbe")
    
    def is_infinity(self) -> bool:
        """Vérifie si c'est le point à l'infini"""
        return self.x is None or self.y is None
    
    def is_on_curve(self) -> bool:
        """Vérifie si le point appartient à la courbe"""
        if self.is_infinity():
            return True
        
        lhs = (self.y**2) % self.curve.p
        rhs = (self.x**3 + self.curve.a * self.x + self.curve.b) % self.curve.p
        return lhs == rhs
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ECPoint):
            return False
        return (self.x, self.y, self.curve) == (other.x, other.y, other.curve)
    
    def __str__(self) -> str:
        if self.is_infinity():
            return "O (point à l'infini)"
        return f"({self.x}, {self.y})"


class EllipticCurveArithmetic:
    """Arithmétique sur les courbes elliptiques"""
    
    @staticmethod
    def mod_inverse(a: int, m: int) -> int:
        """Calcule l'inverse modulaire de a modulo m"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError("L'inverse modulaire n'existe pas")
        return x % m
    
    @staticmethod
    def point_add(P: ECPoint, Q: ECPoint) -> ECPoint:
        """Addition de deux points sur une courbe elliptique"""
        if P.curve != Q.curve:
            raise ValueError("Points sur des courbes différentes")
        
        curve = P.curve
        
        # Cas spéciaux
        if P.is_infinity():
            return Q
        if Q.is_infinity():
            return P
        
        # Cas P = -Q (résultat = point à l'infini)
        if P.x == Q.x and P.y == (-Q.y) % curve.p:
            return ECPoint(None, None, curve)
        
        # Calcul de la pente
        if P == Q:  # Doublement de point
            if P.y == 0:
                return ECPoint(None, None, curve)
            
            # λ = (3x₁² + a) / (2y₁)
            numerator = (3 * P.x**2 + curve.a) % curve.p
            denominator = (2 * P.y) % curve.p
            slope = (numerator * EllipticCurveArithmetic.mod_inverse(denominator, curve.p)) % curve.p
        else:  # Addition normale
            # λ = (y₂ - y₁) / (x₂ - x₁)
            numerator = (Q.y - P.y) % curve.p
            denominator = (Q.x - P.x) % curve.p
            slope = (numerator * EllipticCurveArithmetic.mod_inverse(denominator, curve.p)) % curve.p
        
        # Coordonnées du point résultat
        # x₃ = λ² - x₁ - x₂
        # y₃ = λ(x₁ - x₃) - y₁
        x3 = (slope**2 - P.x - Q.x) % curve.p
        y3 = (slope * (P.x - x3) - P.y) % curve.p
        
        return ECPoint(x3, y3, curve)
    
    @staticmethod
    def scalar_mult(k: int, P: ECPoint) -> ECPoint:
        """Multiplication scalaire k*P using binary method"""
        if k == 0:
            return ECPoint(None, None, P.curve)
        if k == 1:
            return P
        
        result = ECPoint(None, None, P.curve)  # Point à l'infini
        addend = P
        
        while k > 0:
            if k & 1:  # Si le bit est 1
                result = EllipticCurveArithmetic.point_add(result, addend)
            addend = EllipticCurveArithmetic.point_add(addend, addend)  # Doubler
            k >>= 1
        
        return result


# ═══════════════════════════════════════════════════════════════
#  COURBES STANDARDS ET FAIBLES
# ═══════════════════════════════════════════════════════════════

def get_standard_curves() -> Dict[str, Dict]:
    """Retourne les paramètres des courbes elliptiques standards"""
    curves = {
        "secp256k1": {
            "p": 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
            "a": 0,
            "b": 7,
            "gx": 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
            "gy": 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
            "n": 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
            "description": "Courbe utilisée par Bitcoin"
        },
        
        "P-256": {
            "p": 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
            "a": 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC,
            "b": 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
            "gx": 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
            "gy": 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
            "n": 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
            "description": "NIST P-256 / secp256r1"
        }
    }
    return curves


def get_weak_curves() -> List[Dict]:
    """Retourne des courbes faibles pour démonstration"""
    weak_curves = [
        {
            "name": "TinyWeak1",
            "p": 97,  # Petit premier
            "a": 2,
            "b": 3,
            "description": "Courbe très petite (p=97) - Facile à casser"
        },
        {
            "name": "TinyWeak2", 
            "p": 101,
            "a": 1,
            "b": 5,
            "description": "Courbe petite (p=101) - Ordre faible"
        },
        {
            "name": "SmallWeak",
            "p": 1009,  # Plus grand mais encore cassable
            "a": 0,
            "b": 1,
            "description": "Courbe moyenne (p=1009) - Attaque Pollard Rho possible"
        }
    ]
    return weak_curves


# ═══════════════════════════════════════════════════════════════
#  CALCUL DE L'ORDRE D'UNE COURBE
# ═══════════════════════════════════════════════════════════════

def count_curve_points(curve: EllipticCurve) -> int:
    """Compte naïvement tous les points d'une courbe (pour petites courbes)"""
    if curve.p > 2000:
        raise ValueError("Courbe trop grande pour comptage naïf")
    
    point_count = 1  # Point à l'infini
    
    for x in range(curve.p):
        y_squared = (x**3 + curve.a * x + curve.b) % curve.p
        
        # Cherche les racines carrées de y²
        for y in range(curve.p):
            if (y * y) % curve.p == y_squared:
                point_count += 1
    
    return point_count


def estimate_curve_order_hasse(curve: EllipticCurve) -> Tuple[int, int]:
    """Estime l'ordre d'une courbe avec les bornes de Hasse"""
    p = curve.p
    lower_bound = p + 1 - 2 * int(math.sqrt(p))
    upper_bound = p + 1 + 2 * int(math.sqrt(p))
    return lower_bound, upper_bound


# ═══════════════════════════════════════════════════════════════
#  ATTAQUE POLLARD RHO POUR ECDLP
# ═══════════════════════════════════════════════════════════════

def pollard_rho_ecdlp(P: ECPoint, Q: ECPoint, n: int, max_iterations: int = 100000) -> Optional[int]:
    """
    Attaque Pollard Rho pour résoudre le problème du logarithme discret elliptique
    Trouve k tel que Q = k*P
    """
    
    def partition_function(R: ECPoint) -> int:
        """Fonction de partitionnement pour Pollard Rho"""
        if R.is_infinity():
            return 0
        return R.x % 3
    
    def iterate_function(R: ECPoint, a: int, b: int) -> Tuple[ECPoint, int, int]:
        """Fonction d'itération f(R) avec mise à jour des coefficients"""
        try:
            partition = partition_function(R)
            
            if partition == 0:
                # R' = 2R, a' = 2a, b' = 2b
                new_R = EllipticCurveArithmetic.point_add(R, R)
                return (new_R, (2 * a) % n, (2 * b) % n)
            elif partition == 1:
                # R' = R + P, a' = a + 1, b' = b
                new_R = EllipticCurveArithmetic.point_add(R, P)
                return (new_R, (a + 1) % n, b)
            else:
                # R' = R + Q, a' = a, b' = b + 1
                new_R = EllipticCurveArithmetic.point_add(R, Q)
                return (new_R, a, (b + 1) % n)
        except:
            # En cas d'erreur, retourner le point à l'infini
            return (ECPoint(None, None, R.curve), 0, 0)
    
    # Essayer plusieurs points de départ
    for attempt in range(3):
        try:
            # Initialisation aléatoire
            x0 = random.randint(1, n-1)
            y0 = random.randint(1, n-1)
            
            # R0 = x0*P + y0*Q
            try:
                R0 = EllipticCurveArithmetic.point_add(
                    EllipticCurveArithmetic.scalar_mult(x0, P),
                    EllipticCurveArithmetic.scalar_mult(y0, Q)
                )
            except:
                continue
            
            # Algorithme de Floyd (tortue et lièvre)
            tortue_R, tortue_a, tortue_b = R0, x0, y0
            lievre_R, lievre_a, lievre_b = R0, x0, y0
            
            for i in range(max_iterations // 3):
                try:
                    # Tortue : un pas
                    tortue_R, tortue_a, tortue_b = iterate_function(tortue_R, tortue_a, tortue_b)
                    
                    # Lièvre : deux pas
                    lievre_R, lievre_a, lievre_b = iterate_function(lievre_R, lievre_a, lievre_b)
                    lievre_R, lievre_a, lievre_b = iterate_function(lievre_R, lievre_a, lievre_b)
                    
                    # Collision détectée
                    if tortue_R == lievre_R and not tortue_R.is_infinity():
                        # tortue: a1*P + b1*Q, lievre: a2*P + b2*Q
                        # a1*P + b1*Q = a2*P + b2*Q
                        # (a1-a2)*P = (b2-b1)*Q
                        
                        da = (tortue_a - lievre_a) % n
                        db = (lievre_b - tortue_b) % n
                        
                        if db == 0:
                            continue  # Pas utile, recommencer
                        
                        try:
                            # k = da * db^(-1) mod n
                            db_inv = EllipticCurveArithmetic.mod_inverse(db, n)
                            k = (da * db_inv) % n
                            
                            # Vérification
                            verification = EllipticCurveArithmetic.scalar_mult(k, P)
                            if verification == Q:
                                return k
                        except (ValueError, ZeroDivisionError):
                            # Inverse n'existe pas, continuer
                            continue
                except:
                    # Erreur dans l'itération, continuer
                    continue
        except:
            # Erreur dans l'initialisation, essayer un autre point de départ
            continue
    
    # Si toutes les tentatives échouent, essayer une approche par force brute pour petites clés
    if n <= 1000:
        for k in range(1, min(n, 100)):
            try:
                if EllipticCurveArithmetic.scalar_mult(k, P) == Q:
                    return k
            except:
                continue
    
    return None  # Échec


# ═══════════════════════════════════════════════════════════════
#  BENCHMARKS ET ANALYSES
# ═══════════════════════════════════════════════════════════════

def benchmark_scalar_multiplication(curves: List[EllipticCurve], iterations: int = 100) -> Dict:
    """Benchmark de la multiplication scalaire sur différentes courbes"""
    results = {}
    
    for curve in curves:
        # Génère un point aléatoire
        while True:
            x = random.randint(1, curve.p - 1)
            y_squared = (x**3 + curve.a * x + curve.b) % curve.p
            
            # Test si y_squared est un carré parfait
            y = int(math.sqrt(y_squared))
            if (y * y) % curve.p == y_squared:
                P = ECPoint(x, y, curve)
                break
        
        times = []
        k = random.randint(1000, 9999)  # Multiplicateur fixe
        
        for _ in range(iterations):
            start = time.perf_counter()
            EllipticCurveArithmetic.scalar_mult(k, P)
            end = time.perf_counter()
            times.append(end - start)
        
        results[curve.name] = {
            'times': times,
            'mean': np.mean(times),
            'std': np.std(times),
            'curve_size': curve.p.bit_length()
        }
    
    return results


def analyze_curve_security(curve_params: Dict) -> Dict:
    """Analyse la sécurité d'une courbe elliptique"""
    p = curve_params['p']
    
    # Taille de la clé en bits
    key_bits = p.bit_length()
    
    # Estimation de la complexité d'attaque (approximation)
    if 'n' in curve_params:  # Ordre connu
        n = curve_params['n']
        attack_complexity = math.sqrt(n)  # Complexité Pollard Rho
        security_bits = int(math.log2(attack_complexity))
    else:
        # Estimation avec Hasse
        security_bits = key_bits // 2
    
    # Classification de la sécurité
    if security_bits < 40:
        security_level = "TRÈS FAIBLE"
        color = "red"
    elif security_bits < 80:
        security_level = "FAIBLE" 
        color = "yellow"
    elif security_bits < 128:
        security_level = "ACCEPTABLE"
        color = "blue"
    else:
        security_level = "FORT"
        color = "green"
    
    return {
        'key_bits': key_bits,
        'security_bits': security_bits,
        'security_level': security_level,
        'color': color,
        'attack_complexity': 2**security_bits
    }


# ═══════════════════════════════════════════════════════════════
#  VISUALISATIONS
# ═══════════════════════════════════════════════════════════════

def plot_elliptic_curve(curve: EllipticCurve, point_limit: int = 1000) -> str:
    """Visualise une courbe elliptique (pour petites courbes)"""
    if curve.p > point_limit:
        console.print(f"[yellow]Courbe trop grande (p={curve.p}) pour visualisation[/yellow]")
        return ""
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Points de la courbe
    x_coords = []
    y_coords = []
    
    for x in range(curve.p):
        y_squared = (x**3 + curve.a * x + curve.b) % curve.p
        
        for y in range(curve.p):
            if (y * y) % curve.p == y_squared:
                x_coords.append(x)
                y_coords.append(y)
    
    # Graphique
    ax.scatter(x_coords, y_coords, c='blue', alpha=0.6, s=20)
    ax.set_title(f'Courbe Elliptique: y² ≡ x³ + {curve.a}x + {curve.b} (mod {curve.p})')
    ax.set_xlabel('x')
    ax.set_ylabel('y') 
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-1, curve.p)
    ax.set_ylim(-1, curve.p)
    
    # Annotations
    point_count = len(x_coords)
    ax.text(0.02, 0.98, f'Points: {point_count + 1}', transform=ax.transAxes, 
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    filepath = save_plot(fig, f"elliptic_curve_{curve.name}")
    
    return filepath


def plot_security_comparison(analyses: Dict) -> str:
    """Compare la sécurité de différentes courbes"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    names = list(analyses.keys())
    key_bits = [analyses[name]['key_bits'] for name in names]
    security_bits = [analyses[name]['security_bits'] for name in names]
    colors = [analyses[name]['color'] for name in names]
    
    # Graphique 1: Taille des clés vs sécurité
    bars1 = ax1.bar(names, key_bits, alpha=0.7, color='lightblue', label='Taille clé')
    bars2 = ax1.bar(names, security_bits, alpha=0.7, color=colors, label='Sécurité effective')
    
    ax1.set_title('Taille des Clés vs Sécurité Effective')
    ax1.set_ylabel('Bits')
    ax1.set_xlabel('Courbes')
    ax1.legend()
    ax1.tick_params(axis='x', rotation=45)
    
    # Annotations
    for i, (kb, sb) in enumerate(zip(key_bits, security_bits)):
        ax1.annotate(f'{kb}', (i, kb), ha='center', va='bottom')
        ax1.annotate(f'{sb}', (i, sb), ha='center', va='bottom')
    
    # Graphique 2: Complexité d'attaque (échelle log)
    complexities = [analyses[name]['attack_complexity'] for name in names]
    ax2.bar(names, [math.log10(c) for c in complexities], color=colors, alpha=0.7)
    ax2.set_title('Complexité d\'Attaque (log₁₀)')
    ax2.set_ylabel('log₁₀(Opérations)')
    ax2.set_xlabel('Courbes')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    filepath = save_plot(fig, "ecc_security_comparison")
    
    return filepath


# ═══════════════════════════════════════════════════════════════
#  INTERFACE UTILISATEUR
# ═══════════════════════════════════════════════════════════════

def demo_weak_curve_attack():
    """Démonstration d'attaque sur courbe faible"""
    console.print("\n[bold yellow]🎯 Attaque sur Courbe Faible[/bold yellow]\n")
    
    # Sélection d'une courbe faible
    weak_curves = get_weak_curves()
    curve_data = weak_curves[0]  # TinyWeak1
    
    curve = EllipticCurve(curve_data['a'], curve_data['b'], curve_data['p'], curve_data['name'])
    console.print(f"[dim]Courbe: y² ≡ x³ + {curve.a}x + {curve.b} (mod {curve.p})[/dim]")
    
    # Trouve un point générateur
    G = None
    for x in range(1, curve.p):
        y_squared = (x**3 + curve.a * x + curve.b) % curve.p
        for y in range(curve.p):
            if (y * y) % curve.p == y_squared:
                G = ECPoint(x, y, curve)
                break
        if G:
            break
    
    if not G:
        console.print("[red]Erreur: Impossible de trouver un point générateur[/red]")
        return
    
    console.print(f"[cyan]Point générateur G: {G}[/cyan]")
    
    # Génération d'une clé privée secrète
    order = count_curve_points(curve)
    console.print(f"[cyan]Ordre de la courbe: {order}[/cyan]")
    
    secret_key = random.randint(2, order - 1)
    public_key = EllipticCurveArithmetic.scalar_mult(secret_key, G)
    
    console.print(f"[green]Clé privée (secrète): {secret_key}[/green]")
    console.print(f"[blue]Clé publique: {public_key}[/blue]")
    
    # Attaque Pollard Rho
    console.print(f"\n[yellow]🚀 Lancement de l'attaque Pollard Rho...[/yellow]")
    
    start_time = time.perf_counter()
    recovered_key = pollard_rho_ecdlp(G, public_key, order)
    end_time = time.perf_counter()
    
    if recovered_key is not None:
        # Vérification que la clé récupérée est correcte
        verification = EllipticCurveArithmetic.scalar_mult(recovered_key, G)
        is_correct = verification == public_key
        
        console.print(f"[bold green]✅ Clé privée récupérée: {recovered_key}[/bold green]")
        console.print(f"[bold green]✅ Vérification Q = k*P: {is_correct}[/bold green]")
        
        if is_correct:
            console.print(f"[bold green]🎯 SUCCÈS - Clé secrète retrouvée ![/bold green]")
        else:
            # Vérifier si c'est équivalent modulo l'ordre
            for test_mod in [order, order//2, order//4]:
                if (recovered_key % test_mod) == (secret_key % test_mod):
                    console.print(f"[bold green]🎯 SUCCÈS - Clés équivalentes modulo {test_mod}[/bold green]")
                    is_correct = True
                    break
            
            if not is_correct:
                console.print(f"[yellow]⚠️ Clé trouvée mais différente de l'originale[/yellow]")
        
        console.print(f"[cyan]Temps d'attaque: {format_time(end_time - start_time)}[/cyan]")
        return True
    else:
        console.print(f"[red]❌ Échec de l'attaque[/red]")
        console.print(f"[dim]Ceci est normal - Pollard Rho est probabiliste et peut échouer[/dim]")
        console.print(f"[dim]Essayez de relancer l'attaque ou utilisez une courbe différente[/dim]")
        return False


def compare_curve_strengths():
    """Compare la force de différentes courbes"""
    console.print("\n[bold yellow]📊 Comparaison des Forces des Courbes[/bold yellow]\n")
    
    # Courbes à analyser
    weak_curves = get_weak_curves()
    standard_curves = get_standard_curves()
    
    all_analyses = {}
    
    # Analyse des courbes faibles
    for weak in weak_curves:
        analysis = analyze_curve_security(weak)
        all_analyses[weak['name']] = analysis
    
    # Analyse des courbes standards (échantillon)
    for name, params in list(standard_curves.items())[:2]:  # Limite pour la démo
        analysis = analyze_curve_security(params)
        all_analyses[name] = analysis
    
    # Tableau de comparaison
    table = Table(title="Analyse de Sécurité des Courbes", box=box.ROUNDED)
    table.add_column("Courbe", justify="left")
    table.add_column("Taille Clé (bits)", justify="center")
    table.add_column("Sécurité (bits)", justify="center")
    table.add_column("Niveau", justify="center")
    table.add_column("Complexité Attaque", justify="center")
    
    for name, analysis in all_analyses.items():
        color = analysis['color']
        table.add_row(
            name,
            str(analysis['key_bits']),
            str(analysis['security_bits']),
            f"[{color}]{analysis['security_level']}[/{color}]",
            f"{analysis['attack_complexity']:.2e}"
        )
    
    console.print(table)
    
    # Génération du graphique
    plot_path = plot_security_comparison(all_analyses)
    console.print(f"\n[green]📊 Graphique de comparaison: {plot_path}[/green]")
    
    return all_analyses


def benchmark_performance():
    """Benchmark des performances ECC"""
    console.print("\n[bold yellow]⚡ Benchmark des Performances[/bold yellow]\n")
    
    # Courbes de test (petites pour la démo)
    test_curves = []
    weak_curves = get_weak_curves()
    
    for weak in weak_curves:
        curve = EllipticCurve(weak['a'], weak['b'], weak['p'], weak['name'])
        test_curves.append(curve)
    
    # Benchmark
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
    ) as progress:
        
        task = progress.add_task("Benchmark en cours...", total=len(test_curves))
        benchmark_results = benchmark_scalar_multiplication(test_curves, iterations=50)
        progress.update(task, completed=len(test_curves))
    
    # Résultats
    table = Table(title="Performances Multiplication Scalaire", box=box.ROUNDED)
    table.add_column("Courbe", justify="left")
    table.add_column("Taille (bits)", justify="center")
    table.add_column("Temps Moyen (ms)", justify="center")
    table.add_column("Écart-type (ms)", justify="center")
    
    for name, result in benchmark_results.items():
        table.add_row(
            name,
            str(result['curve_size']),
            f"{result['mean'] * 1000:.3f}",
            f"{result['std'] * 1000:.3f}"
        )
    
    console.print(table)
    
    return benchmark_results


def run():
    """Exécute une analyse de résistance ECC"""
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   ANALYSE DE RÉSISTANCE DES COURBES ELLIPTIQUES     [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]\n")
    
    menu = {
        "1": "🎯 Attaque sur Courbe Faible (Pollard Rho)",
        "2": "📊 Comparaison Force des Courbes",
        "3": "👁️  Visualisation de Courbes",
        "4": "⚡ Benchmark Performances",
        "5": "🧮 Analyse Complète",
        "0": "← Retour"
    }
    
    while True:
        console.print("\n[bold blue]Choisissez une analyse ECC :[/bold blue]")
        for key, value in menu.items():
            console.print(f"  [cyan]{key}[/cyan] - {value}")
        
        choice = Prompt.ask("\n[bold]Votre choix", choices=list(menu.keys()))
        
        if choice == "0":
            break
        elif choice == "1":
            demo_weak_curve_attack()
        elif choice == "2":
            compare_curve_strengths()
        elif choice == "3":
            # Visualisation de courbes petites
            weak_curves = get_weak_curves()
            for curve_data in weak_curves:
                curve = EllipticCurve(curve_data['a'], curve_data['b'], curve_data['p'], curve_data['name'])
                if curve.p <= 200:  # Seulement les très petites
                    plot_path = plot_elliptic_curve(curve)
                    if plot_path:
                        console.print(f"[green]📊 Courbe {curve.name}: {plot_path}[/green]")
        elif choice == "4":
            benchmark_performance()
        elif choice == "5":
            console.print("\n[bold yellow]🚀 Analyse Complète[/bold yellow]")
            
            # Toutes les analyses
            console.print("\n[cyan]1. Attaque sur courbe faible...[/cyan]")
            attack_success = demo_weak_curve_attack()
            
            console.print("\n[cyan]2. Comparaison des courbes...[/cyan]")
            analyses = compare_curve_strengths()
            
            console.print("\n[cyan]3. Benchmark des performances...[/cyan]")
            benchmarks = benchmark_performance()
            
            # Génération de rapport
            from core.utils import ensure_reports_dir
            from datetime import datetime
            
            reports_dir = ensure_reports_dir()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = reports_dir / f"ecc_analysis_report_{timestamp}.md"
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("# 📈 Rapport d'Analyse ECC\n\n")
                f.write(f"**Date:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                
                f.write("## 🎯 Résultats des Attaques\n\n")
                f.write(f"- **Attaque Pollard Rho:** {'✅ Réussie' if attack_success else '❌ Échec'}\n\n")
                
                f.write("## 📊 Analyse de Sécurité\n\n")
                for name, analysis in analyses.items():
                    level = analysis['security_level']
                    bits = analysis['security_bits']
                    f.write(f"- **{name}:** {level} ({bits} bits de sécurité)\n")
                
                f.write("\n## 🛡️ Recommandations\n\n")
                f.write("1. **Éviter les courbes de petite taille** (< 160 bits)\n")
                f.write("2. **Utiliser des courbes standards** (P-256, secp256k1)\n")
                f.write("3. **Vérifier l'ordre de la courbe** (éviter factorisation facile)\n")
                f.write("4. **Implémenter des contre-mesures** contre les attaques par canaux auxiliaires\n")
            
            console.print(f"\n[green]📄 Rapport ECC généré: {report_path}[/green]")
        
        if choice != "0":
            console.print(f"\n[dim]Appuyez sur Entrée pour continuer...[/dim]")
            input()
