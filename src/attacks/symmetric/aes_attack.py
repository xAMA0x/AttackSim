"""
AES Attack Module - Attaque par Force Brute
Implémente une attaque par force brute sur AES avec clés réduites pour simulation
"""
import secrets
from typing import Optional, Tuple, Dict, List
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.prompt import Prompt, IntPrompt
from rich import box
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# Import PyCryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Import des utilitaires
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from core.utils import Timer, save_plot, format_time, format_number

console = Console()


# ═══════════════════════════════════════════════════════════════
#  UTILITAIRES DE CHIFFREMENT
# ═══════════════════════════════════════════════════════════════

def generate_aes_key(key_bits: int) -> bytes:
    """
    Génère une clé AES de taille réduite (pour simulation)
    
    Args:
        key_bits: Nombre de bits de la clé (16-40 bits)
    
    Returns:
        Clé AES formatée (16, 24 ou 32 octets selon la taille)
    """
    # AES supporte 128, 192, 256 bits (16, 24, 32 octets)
    # Pour simuler des clés plus petites, on utilise 16 octets et on fixe les bits non utilisés
    key_bytes = secrets.randbits(key_bits).to_bytes((key_bits + 7) // 8, 'big')
    
    # Pad à 16 octets (taille minimale pour AES)
    if len(key_bytes) < 16:
        key_bytes = key_bytes.ljust(16, b'\x00')
    
    # Tronque à 16 octets pour cette simulation
    key_bytes = key_bytes[:16]
    
    return key_bytes


def encrypt_aes(plaintext: bytes, key: bytes) -> bytes:
    """
    Chiffre un message avec AES
    
    Args:
        plaintext: Message en clair
        key: Clé AES (16, 24 ou 32 octets)
    
    Returns:
        Message chiffré
    """
    try:
        # Utilise AES-128 (16 octets) pour cette simulation
        key_16 = key[:16].ljust(16, b'\x00')[:16]
        cipher = AES.new(key_16, AES.MODE_ECB)
        padded_text = pad(plaintext, AES.block_size)
        ciphertext = cipher.encrypt(padded_text)
        return ciphertext
    except Exception:
        return b''


def decrypt_aes(ciphertext: bytes, key: bytes) -> Optional[bytes]:
    """
    Déchiffre un message avec AES
    
    Args:
        ciphertext: Message chiffré
        key: Clé AES (16, 24 ou 32 octets)
    
    Returns:
        Message déchiffré ou None si échec
    """
    try:
        key_16 = key[:16].ljust(16, b'\x00')[:16]
        cipher = AES.new(key_16, AES.MODE_ECB)
        decrypted = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted, AES.block_size)
        return plaintext
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════
#  ATTAQUE PAR FORCE BRUTE
# ═══════════════════════════════════════════════════════════════

def brute_force_aes(ciphertext: bytes, plaintext: bytes, key_bits: int,
                    max_keys: Optional[int] = None) -> Tuple[Optional[bytes], float, int]:
    """
    Attaque par force brute sur AES
    
    Args:
        ciphertext: Message chiffré connu
        plaintext: Message en clair connu (pour validation)
        key_bits: Nombre de bits de la clé à tester
        max_keys: Nombre maximum de clés à tester (None = toutes)
    
    Returns:
        Tuple (clé trouvée, temps écoulé, nombre de clés testées)
    """
    timer = Timer()
    timer.start()
    
    max_keys_to_test = 2 ** key_bits
    if max_keys is not None:
        max_keys_to_test = min(max_keys, max_keys_to_test)
    
    keys_tested = 0
    
    # Génère toutes les clés possibles
    for key_int in range(max_keys_to_test):
        # Convertit l'entier en octets (clé 16 octets avec zéros au début)
        key_bytes = key_int.to_bytes(16, byteorder='big')
        
        # Tente de déchiffrer
        decrypted = decrypt_aes(ciphertext, key_bytes)
        
        keys_tested += 1
        
        if decrypted is not None and decrypted == plaintext:
            timer.stop()
            return key_bytes, timer.elapsed(), keys_tested
    
    timer.stop()
    return None, timer.elapsed(), keys_tested


def brute_force_aes_with_progress(ciphertext: bytes, plaintext: bytes, key_bits: int,
                                  max_keys: Optional[int] = None) -> Tuple[Optional[bytes], float, int]:
    """
    Attaque par force brute avec barre de progression
    
    Args:
        ciphertext: Message chiffré connu
        plaintext: Message en clair connu
        key_bits: Nombre de bits de la clé
        max_keys: Nombre maximum de clés à tester
    
    Returns:
        Tuple (clé trouvée, temps écoulé, nombre de clés testées)
    """
    timer = Timer()
    timer.start()
    
    max_keys_to_test = 2 ** key_bits
    if max_keys is not None:
        max_keys_to_test = min(max_keys, max_keys_to_test)
    
    keys_tested = 0
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task(f"[yellow]Test de {format_number(max_keys_to_test)} clés...", total=max_keys_to_test)
        
        for key_int in range(max_keys_to_test):
            key_bytes = key_int.to_bytes(16, byteorder='big')
            
            decrypted = decrypt_aes(ciphertext, key_bytes)
            keys_tested += 1
            
            progress.update(task, advance=1)
            
            if decrypted is not None and decrypted == plaintext:
                timer.stop()
                return key_bytes, timer.elapsed(), keys_tested
    
    timer.stop()
    return None, timer.elapsed(), keys_tested


# ═══════════════════════════════════════════════════════════════
#  BENCHMARK ET VISUALISATION
# ═══════════════════════════════════════════════════════════════

def benchmark_aes_brute_force(key_sizes: List[int], num_tests: int = 3) -> Dict:
    """
    Benchmark de l'attaque par force brute sur différentes tailles de clés
    
    Args:
        key_sizes: Liste des tailles de clés à tester (en bits)
        num_tests: Nombre de tests par taille
    
    Returns:
        Dictionnaire avec les résultats
    """
    results = {
        'key_sizes': key_sizes,
        'times': [],
        'keys_per_sec': [],
        'total_keys_tested': []
    }
    
    console.print(f"\n[bold cyan]📊 Benchmark sur {num_tests} tests par taille de clé[/bold cyan]\n")
    
    # Message de test fixe
    test_plaintext = b"Hello AES!"
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        total_tasks = len(key_sizes) * num_tests
        main_task = progress.add_task("[yellow]Benchmark en cours...", total=total_tasks)
        
        for key_bits in key_sizes:
            times = []
            keys_per_sec_list = []
            total_keys = []
            
            for test_num in range(num_tests):
                # Génère une clé aléatoire
                true_key = generate_aes_key(key_bits)
                
                # Chiffre le message
                ciphertext = encrypt_aes(test_plaintext, true_key)
                
                # Lance l'attaque
                found_key, elapsed, keys_tested = brute_force_aes(
                    ciphertext, test_plaintext, key_bits
                )
                
                times.append(elapsed)
                if elapsed > 0:
                    keys_per_sec = keys_tested / elapsed
                else:
                    keys_per_sec = keys_tested
                keys_per_sec_list.append(keys_per_sec)
                total_keys.append(keys_tested)
                
                progress.advance(main_task)
            
            # Moyennes
            results['times'].append(np.mean(times))
            results['keys_per_sec'].append(np.mean(keys_per_sec_list))
            results['total_keys_tested'].append(int(np.mean(total_keys)))
    
    return results


def create_benchmark_graphs(key_sizes: List[int], results: Dict) -> str:
    """Crée les graphiques de benchmark"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Graphique 1: Temps d'exécution
    ax1.plot(key_sizes, results['times'], 'o-', color='#95E1D3', linewidth=2, markersize=8)
    ax1.set_xlabel('Taille de clé (bits)', fontsize=12)
    ax1.set_ylabel('Temps moyen (secondes)', fontsize=12)
    ax1.set_title('Temps de Cassage AES par Force Brute', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Graphique 2: Nombre de clés testées
    keys_in_millions = [k / 1_000_000 for k in results['total_keys_tested']]
    ax2.plot(key_sizes, keys_in_millions, 's-', color='#F38181', linewidth=2, markersize=8)
    ax2.set_xlabel('Taille de clé (bits)', fontsize=12)
    ax2.set_ylabel('Nombre de clés testées (millions)', fontsize=12)
    ax2.set_title('Nombre de Clés Testées selon la Taille', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Sauvegarde
    filepath = save_plot(fig, "aes_brute_force_benchmark")
    return filepath


def create_comparison_graph(des_results: Dict, aes_results: Dict) -> str:
    """Crée un graphique comparatif AES vs DES"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # Trouve les tailles communes
    common_sizes = sorted(set(des_results['key_sizes']) & set(aes_results['key_sizes']))
    
    des_times = []
    aes_times = []
    
    for size in common_sizes:
        des_idx = des_results['key_sizes'].index(size)
        aes_idx = aes_results['key_sizes'].index(size)
        des_times.append(des_results['times'][des_idx])
        aes_times.append(aes_results['times'][aes_idx])
    
    ax.plot(common_sizes, des_times, 'o-', label='DES', color='#FF6B6B', linewidth=2, markersize=8)
    ax.plot(common_sizes, aes_times, 's-', label='AES', color='#95E1D3', linewidth=2, markersize=8)
    ax.set_xlabel('Taille de clé (bits)', fontsize=12)
    ax.set_ylabel('Temps moyen (secondes)', fontsize=12)
    ax.set_title('Comparaison DES vs AES - Temps de Cassage', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    # Utilise une échelle linéaire en secondes et formate les labels en notation "plain"
    try:
        from matplotlib.ticker import ScalarFormatter
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.ticklabel_format(style='plain', axis='y')
    except Exception:
        # Fallback: ne rien faire si le formateur n'est pas disponible
        pass
    
    plt.tight_layout()
    
    # Sauvegarde
    filepath = save_plot(fig, "des_vs_aes_comparison")
    return filepath


# ═══════════════════════════════════════════════════════════════
#  INTERFACE PRINCIPALE
# ═══════════════════════════════════════════════════════════════

def run():
    """Exécute une simulation d'attaque sur AES"""
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]         ATTAQUE AES PAR FORCE BRUTE                [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]\n")
    
    console.print("[yellow]🔐 Simulation d'attaque par force brute sur AES[/yellow]")
    console.print("[dim]Tailles de clés réduites pour simulation : 16-22 bits[/dim]")
    console.print("[dim]AES réel utilise 128, 192 ou 256 bits (trop long à craquer)[/dim]\n")
    
    # Menu
    menu = {
        "1": "Attaque sur une clé générée aléatoirement",
        "2": "Benchmark comparatif (temps vs taille de clé)",
        "3": "Mode validation (clé connue)",
        "4": "Comparaison AES vs DES",
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
        run_validation_mode()
    
    elif choice == "4":
        run_comparison()


def run_single_attack():
    """Attaque sur une clé générée aléatoirement"""
    console.print("\n[bold green]═══ Attaque Simple ═══[/bold green]\n")
    
    key_bits = IntPrompt.ask("[yellow]Taille de la clé (bits)[/yellow]", default=20)
    
    if key_bits < 16 or key_bits > 40:
        console.print("[bold red]⚠️  Taille de clé doit être entre 16 et 40 bits pour la simulation ![/bold red]")
        key_bits = max(16, min(40, key_bits))
        console.print(f"[dim]Ajusté à {key_bits} bits[/dim]\n")
    
    if key_bits > 32:
        console.print("[bold red]⚠️  Attention: Au-delà de 22 bits, l'attaque peut être très longue ![/bold red]")
        if not Prompt.ask("[yellow]Continuer ? (o/n)[/yellow]", choices=["o", "n"], default="n") == "o":
            return
    
    # Génération de la clé et du message
    console.print(f"\n[cyan]🔑 Génération d'une clé AES ({key_bits} bits)...[/cyan]")
    true_key = generate_aes_key(key_bits)
    
    test_plaintext = b"Hello AES!"
    console.print(f"[cyan]📝 Message en clair: {test_plaintext.decode()}[/cyan]")
    
    # Chiffrement
    ciphertext = encrypt_aes(test_plaintext, true_key)
    console.print(f"[cyan]🔒 Message chiffré (hex): {ciphertext.hex()}[/cyan]\n")
    
    # Affichage de la clé (pour vérification)
    table = Table(title="Paramètres de l'Attaque", box=box.DOUBLE, show_header=True, header_style="bold cyan")
    table.add_column("Paramètre", style="yellow", width=20)
    table.add_column("Valeur", style="white")
    
    table.add_row("Taille de clé", f"{key_bits} bits")
    table.add_row("Clé (hex)", true_key.hex())
    table.add_row("Clés possibles", format_number(2 ** key_bits))
    
    console.print()
    console.print(table)
    console.print()
    
    # Lance l'attaque
    console.print("[bold cyan]🔓 Lancement de l'attaque par force brute...[/bold cyan]\n")
    
    found_key, elapsed, keys_tested = brute_force_aes_with_progress(
        ciphertext, test_plaintext, key_bits
    )
    
    # Résultats
    console.print()
    results_table = Table(title="Résultats de l'Attaque", box=box.ROUNDED, show_header=True, header_style="bold green")
    results_table.add_column("Métrique", style="cyan", width=25)
    results_table.add_column("Valeur", style="white")
    
    if found_key is not None:
        results_table.add_row("Succès", "[green]✓ Clé trouvée ![/green]")
        results_table.add_row("Clé trouvée (hex)", found_key.hex())
        results_table.add_row("Clé correcte", "[green]✓[/green]" if found_key == true_key else "[red]✗[/red]")
    else:
        results_table.add_row("Succès", "[red]✗ Clé non trouvée[/red]")
    
    results_table.add_row("Temps écoulé", format_time(elapsed))
    results_table.add_row("Clés testées", format_number(keys_tested))
    
    if elapsed > 0:
        keys_per_sec = keys_tested / elapsed
        results_table.add_row("Clés/seconde", f"{format_number(int(keys_per_sec))}")
    else:
        results_table.add_row("Clés/seconde", "N/A")
    
    console.print()
    console.print(results_table)
    console.print()
    
    # Vérification
    if found_key is not None:
        decrypted = decrypt_aes(ciphertext, found_key)
        if decrypted == test_plaintext:
            console.print("[bold green]✅ Vérification: Message déchiffré correctement ![/bold green]\n")
    
    console.print("[bold green]✅ Attaque terminée ![/bold green]\n")


def run_benchmark():
    """Benchmark comparatif"""
    console.print("\n[bold green]═══ Benchmark Comparatif ═══[/bold green]\n")
    
    key_sizes = [16, 18, 20, 22]
    console.print(f"[cyan]Tailles de clés testées: {key_sizes} bits[/cyan]")
    console.print(f"[dim]3 tests par taille[/dim]\n")
    
    # Exécute le benchmark
    results = benchmark_aes_brute_force(key_sizes, num_tests=3)
    
    # Affiche les résultats
    console.print("\n[bold cyan]📊 Résultats du Benchmark[/bold cyan]\n")
    
    results_table = Table(title="Résultats par Taille de Clé", box=box.ROUNDED, show_header=True, header_style="bold green")
    results_table.add_column("Taille (bits)", style="cyan", justify="center", width=15)
    results_table.add_column("Temps moyen", style="yellow", width=20)
    results_table.add_column("Clés/seconde", style="green", width=20)
    results_table.add_column("Clés testées", style="white", width=20)
    
    for i, size in enumerate(key_sizes):
        results_table.add_row(
            str(size),
            format_time(results['times'][i]),
            format_number(int(results['keys_per_sec'][i])),
            format_number(results['total_keys_tested'][i])
        )
    
    console.print()
    console.print(results_table)
    console.print()
    
    # Génère les graphiques
    console.print("[cyan]📈 Génération des graphiques...[/cyan]")
    filepath = create_benchmark_graphs(key_sizes, results)
    console.print(f"[bold green]✅ Graphiques sauvegardés: {filepath}[/bold green]\n")


def get_validated_secret_key() -> bytes:
    """
    Récupère un secret de l'utilisateur avec validation
    
    Le secret doit être inférieur à 2^22 (4194304) et est converti en clé AES 16 octets.
    
    Returns:
        Clé AES de 16 octets dérivée du secret validé
    """
    MAX_VALUE = 2 ** 22  # 4194304
    
    console.print("[cyan]Entrez un secret (nombre entier ou chaîne hexadécimale):[/cyan]")
    console.print(f"[dim]Le secret doit être < {MAX_VALUE:,} (2^22)[/dim]")
    
    while True:
        secret_input = Prompt.ask("[yellow]Secret[/yellow]").strip()
        
        if not secret_input:
            console.print("[bold red]✗ Entrée vide, veuillez réessayer[/bold red]")
            continue
        
        try:
            # Essaie de parser comme hexadécimal d'abord (si commence par 0x ou contient lettres)
            if secret_input.lower().startswith('0x') or any(c in secret_input.lower() for c in 'abcdef'):
                secret_value = int(secret_input, 16)
                input_type = "hexadécimal"
            else:
                # Sinon, le traite comme entier décimal
                secret_value = int(secret_input, 10)
                input_type = "décimal"
            
            # Valide la limite
            if secret_value < 0:
                console.print("[bold red]✗ Le secret doit être positif[/bold red]")
                continue
            
            if secret_value >= MAX_VALUE:
                console.print(f"[bold red]✗ Le secret ({secret_value:,}) dépasse la limite (< {MAX_VALUE:,})[/bold red]")
                console.print(f"[dim]En binaire, cela ferait {secret_value.bit_length()} bits, dépassant les 22 bits autorisés[/dim]")
                continue
            
            # ✅ Secret valide - Convertit en clé AES
            console.print(f"[green]✓ Secret validé ({input_type}): {secret_value:,}[/green]")
            
            # Convertit l'entier en clé AES de 16 octets
            # Place le secret à la FIN avec padding de zéros au DÉBUT
            # Cela garantit que la clé reste dans l'intervalle [0, 2^22]
            key_bytes = secret_value.to_bytes(16, byteorder='big')
            
            console.print(f"[cyan]Clé AES (hex): {key_bytes.hex()}[/cyan]")
            console.print(f"[cyan]Clé (16 octets): {key_bytes}[/cyan]\n")
            
            return key_bytes
        
        except ValueError:
            console.print("[bold red]✗ Format invalide. Entrez un nombre entier ou hexadécimal (ex: 123 ou 0xABC)[/bold red]")
            continue


def run_validation_mode():
    """Mode validation avec clé connue"""
    console.print("\n[bold green]═══ Mode Validation ═══[/bold green]\n")
    
    console.print("[yellow]Ce mode permet de valider que l'attaque fonctionne avec une clé connue[/yellow]\n")
    
    # Récupère et valide le secret
    true_key = get_validated_secret_key()
    
    # Calcule le nombre de bits effectifs de la clé
    key_int = int.from_bytes(true_key, 'big')
    effective_bits = key_int.bit_length() if key_int > 0 else 1
    
    console.print(f"[cyan]Clé acceptée: {true_key.hex()}[/cyan]")
    console.print(f"[cyan]Nombre de bits effectifs: {effective_bits}[/cyan]\n")
    
    # Message de test
    test_plaintext = b"Test AES!"
    console.print(f"[cyan]📝 Message en clair: {test_plaintext.decode()}[/cyan]")
    
    # Chiffrement
    ciphertext = encrypt_aes(test_plaintext, true_key)
    console.print(f"[cyan]🔒 Message chiffré (hex): {ciphertext.hex()}[/cyan]\n")
    
    # Teste d'abord la clé exacte pour validation rapide
    console.print("[bold cyan]🔓 Test de la clé exacte en premier...[/bold cyan]")
    decrypted = decrypt_aes(ciphertext, true_key)
    if decrypted == test_plaintext:
        console.print("[bold green]✅ La clé fournie fonctionne correctement ![/bold green]\n")
    else:
        console.print("[bold red]✗ La clé fournie ne déchiffre pas correctement le message ![/bold red]\n")
        return
    
    # Lance l'attaque par force brute
    console.print("[bold cyan]🔓 Lancement de l'attaque par force brute...[/bold cyan]\n")
    
    # Limite à 22 bits max pour éviter des temps trop longs
    key_bits_to_test = min(22, max(effective_bits, 16))
    
    if effective_bits > 22:
        console.print(f"[yellow]⚠️  La clé fait {effective_bits} bits, mais on teste seulement jusqu'à 22 bits pour la simulation[/yellow]")
        console.print(f"[yellow]Pour tester la clé exacte, utilisez une clé de 22 bits ou moins[/yellow]\n")
    
    found_key, elapsed, keys_tested = brute_force_aes_with_progress(
        ciphertext, test_plaintext, key_bits_to_test
    )
    
    # Vérifie aussi si la clé exacte serait dans la plage testée
    key_in_range = key_int < (2 ** key_bits_to_test)
    
    # Résultats
    console.print()
    if found_key is not None:
        if found_key == true_key:
            console.print("[bold green]✅ Succès: Clé trouvée et validée ![/bold green]")
            console.print(f"[green]Clé trouvée: {found_key.hex()}[/green]")
            console.print(f"[green]Temps: {format_time(elapsed)}[/green]")
            console.print(f"[green]Clés testées: {format_number(keys_tested)}[/green]\n")
        else:
            console.print("[yellow]⚠️  Une clé a été trouvée, mais ce n'est pas la clé fournie[/yellow]")
            console.print(f"[yellow]Clé trouvée: {found_key.hex()}[/yellow]")
            console.print(f"[yellow]Clé attendue: {true_key.hex()}[/yellow]\n")
    else:
        if not key_in_range:
            console.print(f"[yellow]ℹ️  La clé fournie ({effective_bits} bits) dépasse la plage testée (22 bits)[/yellow]")
            console.print("[yellow]C'est normal que la clé ne soit pas trouvée dans cette simulation[/yellow]\n")
        else:
            console.print("[bold red]✗ Échec: Clé non trouvée dans la plage testée[/bold red]\n")
    
    console.print("[bold green]✅ Test de validation terminé ![/bold green]\n")


def run_comparison():
    """Comparaison AES vs DES"""
    console.print("\n[bold green]═══ Comparaison AES vs DES ═══[/bold green]\n")
    
    console.print("[yellow]Cette fonction compare les performances de cassage entre AES et DES[/yellow]")
    console.print("[dim]Note: Les tailles de clés sont réduites pour la simulation[/dim]\n")
    
    if not Prompt.ask("[yellow]Lancer la comparaison ? (o/n)[/yellow]", choices=["o", "n"], default="o") == "o":
        return
    
    # Tailles communes pour la comparaison
    common_sizes = [16, 18, 20, 22]
    console.print(f"[cyan]Tailles testées: {common_sizes} bits[/cyan]")
    console.print(f"[dim]Cela peut prendre plusieurs minutes...[/dim]\n")
    
    # Import DES pour le benchmark (import local pour éviter dépendance circulaire)
    try:
        from . import des_attack
        benchmark_des_brute_force = des_attack.benchmark_des_brute_force
    except ImportError:
        # Fallback si import relatif échoue
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        import des_attack
        benchmark_des_brute_force = des_attack.benchmark_des_brute_force
    
    # Benchmark DES
    console.print("[cyan]📊 Benchmark DES...[/cyan]")
    des_results = benchmark_des_brute_force(common_sizes, num_tests=2)
    
    # Benchmark AES
    console.print("[cyan]📊 Benchmark AES...[/cyan]")
    aes_results = benchmark_aes_brute_force(common_sizes, num_tests=2)
    
    # Affiche les résultats
    console.print("\n[bold cyan]📊 Résultats Comparatifs[/bold cyan]\n")
    
    comparison_table = Table(title="Comparaison DES vs AES", box=box.ROUNDED, show_header=True, header_style="bold green")
    comparison_table.add_column("Taille (bits)", style="cyan", justify="center", width=15)
    comparison_table.add_column("DES (temps)", style="yellow", width=20)
    comparison_table.add_column("AES (temps)", style="yellow", width=20)
    comparison_table.add_column("Ratio", style="green", width=15)
    
    for size in common_sizes:
        des_idx = des_results['key_sizes'].index(size)
        aes_idx = aes_results['key_sizes'].index(size)
        
        des_time = des_results['times'][des_idx]
        aes_time = aes_results['times'][aes_idx]
        
        ratio = aes_time / des_time if des_time > 0 else 0
        
        comparison_table.add_row(
            str(size),
            format_time(des_time),
            format_time(aes_time),
            f"{ratio:.2f}x"
        )
    
    console.print()
    console.print(comparison_table)
    console.print()
    
    # Génère le graphique comparatif
    console.print("[cyan]📈 Génération du graphique comparatif...[/cyan]")
    filepath = create_comparison_graph(des_results, aes_results)
    console.print(f"[bold green]✅ Graphique sauvegardé: {filepath}[/bold green]\n")
