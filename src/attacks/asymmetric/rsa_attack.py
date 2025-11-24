"""
RSA Attack Module - Attaque par Factorisation
Implémente plusieurs méthodes de factorisation pour casser RSA avec petites clés
"""
import time
import math
import random
from typing import Tuple, Optional, Dict, List
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.prompt import Prompt, IntPrompt
from rich import box
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# Import des utilitaires
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from core.utils import Timer, save_plot, format_time, format_number

console = Console()


# ═══════════════════════════════════════════════════════════════
#  GÉNÉRATION DE CLÉS RSA
# ═══════════════════════════════════════════════════════════════

def is_prime(n: int, k: int = 5) -> bool:
    """Test de primalité de Miller-Rabin"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Écrire n-1 comme 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Test de Miller-Rabin k fois
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True


def generate_prime(bits: int) -> int:
    """Génère un nombre premier de 'bits' bits"""
    while True:
        # Génère un nombre impair aléatoire
        candidate = random.getrandbits(bits)
        candidate |= (1 << bits - 1) | 1  # S'assure qu'il fait bien 'bits' bits et qu'il est impair
        
        if is_prime(candidate):
            return candidate


def gcd(a: int, b: int) -> int:
    """Plus grand commun diviseur (algorithme d'Euclide)"""
    while b:
        a, b = b, a % b
    return a


def mod_inverse(e: int, phi: int) -> int:
    """Calcule l'inverse modulaire de e modulo phi (algorithme d'Euclide étendu)"""
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    
    _, x, _ = extended_gcd(e, phi)
    return (x % phi + phi) % phi


def generate_rsa_keypair(bits: int = 16) -> Dict:
    """
    Génère une paire de clés RSA
    
    Args:
        bits: Nombre de bits pour chaque nombre premier (total = 2*bits)
    
    Returns:
        Dictionnaire avec p, q, n, e, d, phi
    """
    console.print(f"[dim]Génération de deux nombres premiers de {bits} bits...[/dim]")
    
    p = generate_prime(bits)
    q = generate_prime(bits)
    
    # S'assure que p != q
    while p == q:
        q = generate_prime(bits)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choisit e (souvent 65537, mais on prend un plus petit pour petites clés)
    e = 65537 if phi > 65537 else 3
    while gcd(e, phi) != 1:
        e += 2
    
    d = mod_inverse(e, phi)
    
    return {
        'p': p,
        'q': q,
        'n': n,
        'e': e,
        'd': d,
        'phi': phi,
        'bits': bits * 2
    }


# ═══════════════════════════════════════════════════════════════
#  MÉTHODES DE FACTORISATION
# ═══════════════════════════════════════════════════════════════

def trial_division(n: int) -> Optional[Tuple[int, int]]:
    """
    Factorisation par division d'essai (force brute)
    Teste tous les diviseurs jusqu'à sqrt(n)
    """
    timer = Timer()
    timer.start()
    
    limit = int(math.sqrt(n)) + 1
    
    for i in range(2, min(limit, 10**6)):  # Limite pour éviter trop de temps
        if n % i == 0:
            timer.stop()
            return i, n // i, timer.elapsed()
    
    timer.stop()
    return None, None, timer.elapsed()


def fermat_factorization(n: int, max_iterations: int = 10**6) -> Optional[Tuple[int, int]]:
    """
    Méthode de Fermat
    Efficace quand p et q sont proches
    """
    timer = Timer()
    timer.start()
    
    a = int(math.ceil(math.sqrt(n)))
    b2 = a * a - n
    
    for _ in range(max_iterations):
        if b2 >= 0:
            b = int(math.sqrt(b2))
            if b * b == b2:
                timer.stop()
                p = a - b
                q = a + b
                return p, q, timer.elapsed()
        
        a += 1
        b2 = a * a - n
    
    timer.stop()
    return None, None, timer.elapsed()


def pollard_rho(n: int, max_iterations: int = 10**6) -> Optional[Tuple[int, int]]:
    """
    Algorithme rho de Pollard
    Méthode probabiliste efficace
    """
    timer = Timer()
    timer.start()
    
    if n % 2 == 0:
        timer.stop()
        return 2, n // 2, timer.elapsed()
    
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    
    for _ in range(max_iterations):
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = gcd(abs(x - y), n)
        
        if d != 1 and d != n:
            timer.stop()
            return d, n // d, timer.elapsed()
    
    timer.stop()
    return None, None, timer.elapsed()


# ═══════════════════════════════════════════════════════════════
#  BENCHMARK ET VISUALISATION
# ═══════════════════════════════════════════════════════════════

def benchmark_methods(key_sizes: List[int], num_tests: int = 5) -> Dict:
    """
    Benchmark des différentes méthodes sur plusieurs tailles de clés
    
    Returns:
        Dictionnaire avec les résultats par méthode
    """
    results = {
        'trial_division': {'times': [], 'success': []},
        'fermat': {'times': [], 'success': []},
        'pollard': {'times': [], 'success': []}
    }
    
    console.print(f"\n[bold cyan]📊 Benchmark sur {num_tests} tests par taille de clé[/bold cyan]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        for bits in key_sizes:
            task = progress.add_task(f"[yellow]Test {bits} bits...", total=num_tests * 3)
            
            times_td, times_fermat, times_pollard = [], [], []
            success_td, success_fermat, success_pollard = 0, 0, 0
            
            for _ in range(num_tests):
                # Génère une clé RSA
                rsa_key = generate_rsa_keypair(bits // 2)
                n = rsa_key['n']
                
                # Test Trial Division
                p, q, t = trial_division(n)
                times_td.append(t)
                if p is not None:
                    success_td += 1
                progress.advance(task)
                
                # Test Fermat
                p, q, t = fermat_factorization(n)
                times_fermat.append(t)
                if p is not None:
                    success_fermat += 1
                progress.advance(task)
                
                # Test Pollard
                p, q, t = pollard_rho(n)
                times_pollard.append(t)
                if p is not None:
                    success_pollard += 1
                progress.advance(task)
            
            # Moyenne des temps
            results['trial_division']['times'].append(np.mean(times_td))
            results['trial_division']['success'].append(success_td / num_tests * 100)
            
            results['fermat']['times'].append(np.mean(times_fermat))
            results['fermat']['success'].append(success_fermat / num_tests * 100)
            
            results['pollard']['times'].append(np.mean(times_pollard))
            results['pollard']['success'].append(success_pollard / num_tests * 100)
    
    return results


def create_benchmark_graphs(key_sizes: List[int], results: Dict) -> str:
    """Crée les graphiques de benchmark"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Graphique 1: Temps d'exécution
    ax1.plot(key_sizes, results['trial_division']['times'], 'o-', label='Division d\'essai', linewidth=2)
    ax1.plot(key_sizes, results['fermat']['times'], 's-', label='Fermat', linewidth=2)
    ax1.plot(key_sizes, results['pollard']['times'], '^-', label='Pollard Rho', linewidth=2)
    ax1.set_xlabel('Taille de clé (bits)', fontsize=12)
    ax1.set_ylabel('Temps moyen (secondes)', fontsize=12)
    ax1.set_title('Performance des Méthodes de Factorisation', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Graphique 2: Taux de succès
    width = 2
    x = np.array(key_sizes)
    ax2.bar(x - width, results['trial_division']['success'], width, label='Division d\'essai', alpha=0.8)
    ax2.bar(x, results['fermat']['success'], width, label='Fermat', alpha=0.8)
    ax2.bar(x + width, results['pollard']['success'], width, label='Pollard Rho', alpha=0.8)
    ax2.set_xlabel('Taille de clé (bits)', fontsize=12)
    ax2.set_ylabel('Taux de succès (%)', fontsize=12)
    ax2.set_title('Taux de Succès par Méthode', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_ylim([0, 105])
    
    plt.tight_layout()
    
    # Sauvegarde
    filepath = save_plot(fig, "rsa_factorization_benchmark")
    return filepath


# ═══════════════════════════════════════════════════════════════
#  INTERFACE PRINCIPALE
# ═══════════════════════════════════════════════════════════════

def run():
    """Exécute une simulation d'attaque sur RSA"""
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]         ATTAQUE RSA PAR FACTORISATION                [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]\n")
    
    console.print("[yellow]🔐 Simulation d'attaque par factorisation sur RSA[/yellow]")
    console.print("[dim]Méthodes: Division d'essai, Fermat, Pollard Rho[/dim]\n")
    
    # Menu
    menu = {
        "1": "Attaque sur une clé générée aléatoirement",
        "2": "Benchmark comparatif des méthodes",
        "3": "Mode personnalisé (vos propres p et q)",
        "0": "← Retour"
    }
    
    table = Table(title="Options", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", justify="center", width=10)
    table.add_column("Description", style="white")
    
    for key, desc in menu.items():
        table.add_row(key, desc)
    
    console.print(table)
    console.print()
    
    choice = Prompt.ask("[bold yellow]Choisissez une option[/bold yellow]", choices=list(menu.keys()), default="0")
    
    if choice == "0":
        return
    
    elif choice == "1":
        run_single_attack()
    
    elif choice == "2":
        run_benchmark()
    
    elif choice == "3":
        run_custom_attack()


def run_single_attack():
    """Attaque sur une clé générée aléatoirement"""
    console.print("\n[bold green]═══ Attaque Simple ═══[/bold green]\n")
    
    bits = IntPrompt.ask("[yellow]Taille de chaque premier (bits)[/yellow]", default=8)
    
    if bits > 32:
        console.print("[bold red]⚠️  Attention: Au-delà de 32 bits, l'attaque peut être très longue ![/bold red]")
        if not Prompt.ask("[yellow]Continuer ? (o/n)[/yellow]", choices=["o", "n"], default="n") == "o":
            return
    
    # Génération de la clé
    console.print(f"\n[cyan]🔑 Génération d'une clé RSA ({bits*2} bits)...[/cyan]")
    rsa_key = generate_rsa_keypair(bits)
    
    # Affichage de la clé
    table = Table(title="Clé RSA Générée", box=box.DOUBLE, show_header=True, header_style="bold cyan")
    table.add_column("Paramètre", style="yellow", width=12)
    table.add_column("Valeur", style="white")
    
    table.add_row("p", str(rsa_key['p']))
    table.add_row("q", str(rsa_key['q']))
    table.add_row("n (p×q)", str(rsa_key['n']))
    table.add_row("φ(n)", str(rsa_key['phi']))
    table.add_row("e (public)", str(rsa_key['e']))
    table.add_row("d (private)", str(rsa_key['d']))
    
    console.print()
    console.print(table)
    console.print()
    
    n = rsa_key['n']
    true_p, true_q = rsa_key['p'], rsa_key['q']
    
    # Test des méthodes
    console.print("[bold cyan]🔓 Tentative de factorisation...[/bold cyan]\n")
    
    methods = [
        ("Division d'essai", trial_division),
        ("Fermat", fermat_factorization),
        ("Pollard Rho", pollard_rho)
    ]
    
    results_table = Table(title="Résultats des Attaques", box=box.ROUNDED, show_header=True, header_style="bold green")
    results_table.add_column("Méthode", style="cyan", width=20)
    results_table.add_column("Succès", justify="center", width=10)
    results_table.add_column("Temps", style="yellow", width=15)
    results_table.add_column("p trouvé", style="white", width=20)
    results_table.add_column("q trouvé", style="white", width=20)
    
    for method_name, method_func in methods:
        p, q, elapsed = method_func(n)
        
        if p is not None and q is not None:
            success = "✓" if (p == true_p or p == true_q) else "✗"
            results_table.add_row(
                method_name,
                f"[green]{success}[/green]" if success == "✓" else f"[red]{success}[/red]",
                format_time(elapsed),
                str(p),
                str(q)
            )
        else:
            results_table.add_row(
                method_name,
                "[red]✗[/red]",
                format_time(elapsed),
                "[dim]Échec[/dim]",
                "[dim]Échec[/dim]"
            )
    
    console.print()
    console.print(results_table)
    console.print()
    
    console.print("[bold green]✅ Attaque terminée ![/bold green]\n")


def run_benchmark():
    """Benchmark comparatif des méthodes"""
    console.print("\n[bold green]═══ Benchmark Comparatif ═══[/bold green]\n")
    
    key_sizes = [16, 20, 24, 28, 32]
    console.print(f"[cyan]Tailles de clés testées: {key_sizes} bits[/cyan]")
    console.print(f"[dim]Cela peut prendre quelques minutes...[/dim]\n")
    
    # Exécute le benchmark
    results = benchmark_methods(key_sizes, num_tests=3)
    
    # Affiche les résultats
    console.print("\n[bold cyan]📊 Résultats du Benchmark[/bold cyan]\n")
    
    for method_name in ['trial_division', 'fermat', 'pollard']:
        method_display = {
            'trial_division': 'Division d\'essai',
            'fermat': 'Fermat',
            'pollard': 'Pollard Rho'
        }[method_name]
        
        console.print(f"[yellow]• {method_display}[/yellow]")
        for i, size in enumerate(key_sizes):
            console.print(f"  {size} bits: {format_time(results[method_name]['times'][i])} "
                         f"(succès: {results[method_name]['success'][i]:.0f}%)")
        console.print()
    
    # Génère les graphiques
    console.print("[cyan]📈 Génération des graphiques...[/cyan]")
    filepath = create_benchmark_graphs(key_sizes, results)
    console.print(f"[bold green]✅ Graphiques sauvegardés: {filepath}[/bold green]\n")


def run_custom_attack():
    """Mode personnalisé avec p et q fournis par l'utilisateur"""
    console.print("\n[bold green]═══ Mode Personnalisé ═══[/bold green]\n")
    
    p = IntPrompt.ask("[yellow]Entrez le premier nombre premier p[/yellow]")
    q = IntPrompt.ask("[yellow]Entrez le second nombre premier q[/yellow]")
    
    if not is_prime(p):
        console.print(f"[bold red]✗ Erreur: {p} n'est pas premier ![/bold red]\n")
        return
    
    if not is_prime(q):
        console.print(f"[bold red]✗ Erreur: {q} n'est pas premier ![/bold red]\n")
        return
    
    n = p * q
    console.print(f"\n[cyan]n = p × q = {format_number(n)}[/cyan]")
    console.print(f"[dim]Taille: {n.bit_length()} bits[/dim]\n")
    
    console.print("[bold cyan]🔓 Tentative de factorisation de n...[/bold cyan]\n")
    
    # Test des méthodes
    methods = [
        ("Division d'essai", trial_division),
        ("Fermat", fermat_factorization),
        ("Pollard Rho", pollard_rho)
    ]
    
    for method_name, method_func in methods:
        console.print(f"[yellow]→ {method_name}...[/yellow]")
        found_p, found_q, elapsed = method_func(n)
        
        if found_p is not None:
            console.print(f"  [green]✓ Succès en {format_time(elapsed)}[/green]")
            console.print(f"  Facteurs trouvés: {found_p} × {found_q}")
        else:
            console.print(f"  [red]✗ Échec après {format_time(elapsed)}[/red]")
        console.print()
    
    console.print("[bold green]✅ Test terminé ![/bold green]\n")
