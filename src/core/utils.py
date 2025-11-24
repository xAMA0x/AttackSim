"""
Utilitaires communs
"""
import os
import time
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from typing import List, Tuple


def ensure_reports_dir() -> Path:
    """
    Crée le dossier reports/ s'il n'existe pas
    
    Returns:
        Path vers le dossier reports/
    """
    reports_dir = Path(__file__).parent.parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    return reports_dir


def save_plot(fig, filename: str) -> str:
    """
    Sauvegarde un graphique matplotlib dans reports/
    
    Args:
        fig: Figure matplotlib
        filename: Nom du fichier (sans extension)
    
    Returns:
        Chemin complet du fichier sauvegardé
    """
    reports_dir = ensure_reports_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_filename = f"{filename}_{timestamp}.png"
    filepath = reports_dir / full_filename
    
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    return str(filepath)


def format_time(seconds: float) -> str:
    """
    Formate un temps en secondes de manière lisible
    
    Args:
        seconds: Temps en secondes
    
    Returns:
        Chaîne formatée (ex: "2.35s", "1m 23s", "1h 5m")
    """
    if seconds < 1:
        return f"{seconds*1000:.2f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def format_number(num: int) -> str:
    """
    Formate un grand nombre avec des séparateurs
    
    Args:
        num: Nombre à formater
    
    Returns:
        Chaîne formatée avec espaces (ex: "1 000 000")
    """
    return f"{num:,}".replace(",", " ")


def create_progress_bar(current: int, total: int, width: int = 50) -> str:
    """
    Crée une barre de progression ASCII
    
    Args:
        current: Valeur actuelle
        total: Valeur maximale
        width: Largeur de la barre
    
    Returns:
        Barre de progression formatée
    """
    percentage = (current / total) * 100
    filled = int((current / total) * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percentage:.1f}%"


def generate_report_header(attack_name: str, params: dict) -> str:
    """
    Génère un en-tête de rapport
    
    Args:
        attack_name: Nom de l'attaque
        params: Paramètres de l'attaque
    
    Returns:
        En-tête formaté
    """
    header = f"""
╔═══════════════════════════════════════════════════╗
  RAPPORT D'ATTAQUE : {attack_name}
  Date : {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
╚═══════════════════════════════════════════════════╝

📋 Paramètres :
"""
    for key, value in params.items():
        header += f"  • {key}: {value}\n"
    
    return header


def estimate_time(operations: int, ops_per_sec: float) -> str:
    """
    Estime le temps nécessaire pour un nombre d'opérations
    
    Args:
        operations: Nombre d'opérations à effectuer
        ops_per_sec: Opérations par seconde
    
    Returns:
        Estimation du temps formatée
    """
    if ops_per_sec == 0:
        return "∞"
    
    seconds = operations / ops_per_sec
    return format_time(seconds)


class Timer:
    """Classe utilitaire pour mesurer le temps d'exécution"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Démarre le chronomètre"""
        self.start_time = time.time()
    
    def stop(self):
        """Arrête le chronomètre"""
        self.end_time = time.time()
    
    def elapsed(self) -> float:
        """Retourne le temps écoulé en secondes"""
        if self.start_time is None:
            return 0.0
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time
    
    def elapsed_str(self) -> str:
        """Retourne le temps écoulé formaté"""
        return format_time(self.elapsed())
