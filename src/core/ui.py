"""
Interface utilisateur CLI
"""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import box
from typing import Callable, Dict

console = Console()


def display_banner():
    """Affiche le banner de l'application"""
    banner = """
    ╔═══════════════════════════════════════════════════╗
    ║                                                   ║
    ║           🔐 CRYPTO ATTACK SIMULATOR 🔐          ║
    ║                                                   ║
    ║              Simulateur d'Attaques                ║
    ║              Cryptographiques - ESGI              ║
    ║                                                   ║
    ╚═══════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan", border_style="bright_blue"))


def display_menu(options: Dict[str, str]) -> str:
    """
    Affiche le menu principal et retourne le choix de l'utilisateur
    
    Args:
        options: Dictionnaire {clé: description}
    
    Returns:
        Choix de l'utilisateur
    """
    table = Table(title="🎯 Menu Principal", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", justify="center", width=10)
    table.add_column("Description", style="white")
    
    for key, desc in options.items():
        table.add_row(key, desc)
    
    console.print()
    console.print(table)
    console.print()
    
    choice = Prompt.ask(
        "[bold yellow]Choisissez une option[/bold yellow]",
        choices=list(options.keys()),
        default="0"
    )
    return choice


def display_submenu(title: str, options: Dict[str, str]) -> str:
    """
    Affiche un sous-menu et retourne le choix
    
    Args:
        title: Titre du sous-menu
        options: Dictionnaire {clé: description}
    
    Returns:
        Choix de l'utilisateur
    """
    table = Table(title=f"📋 {title}", box=box.ROUNDED, show_header=True, header_style="bold green")
    table.add_column("Option", style="cyan", justify="center", width=10)
    table.add_column("Attaque", style="white")
    
    for key, desc in options.items():
        table.add_row(key, desc)
    
    console.print()
    console.print(table)
    console.print()
    
    choice = Prompt.ask(
        "[bold yellow]Choisissez une attaque[/bold yellow]",
        choices=list(options.keys()),
        default="0"
    )
    return choice


def display_success(message: str):
    """Affiche un message de succès"""
    console.print(f"\n[bold green]✓ {message}[/bold green]\n")


def display_error(message: str):
    """Affiche un message d'erreur"""
    console.print(f"\n[bold red]✗ {message}[/bold red]\n")


def display_info(message: str):
    """Affiche un message d'information"""
    console.print(f"\n[bold blue]ℹ {message}[/bold blue]\n")


def display_warning(message: str):
    """Affiche un avertissement"""
    console.print(f"\n[bold yellow]⚠ {message}[/bold yellow]\n")


def display_result_panel(title: str, content: str, style: str = "green"):
    """Affiche les résultats dans un panel"""
    console.print()
    console.print(Panel(content, title=title, style=style, border_style="bright_" + style))
    console.print()


def confirm_action(message: str) -> bool:
    """Demande confirmation à l'utilisateur"""
    response = Prompt.ask(f"[bold yellow]{message} (o/n)[/bold yellow]", choices=["o", "n"], default="n")
    return response.lower() == "o"


def wait_for_key():
    """Attend que l'utilisateur appuie sur Entrée"""
    Prompt.ask("\n[dim]Appuyez sur Entrée pour continuer...[/dim]", default="")


def clear_screen():
    """Efface l'écran (via Rich)"""
    console.clear()
