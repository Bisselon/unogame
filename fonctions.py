# Importation des modules nécessaires
from typing import Callable
from pyfiglet import Figlet

def afficher_logo(func: Callable) -> Callable:
    """Affiche le logo du jeu"""
    async def wrapper(*args, **kwargs):
        print("\033c\n", end="")
        print("-" * 38, "\n" + Figlet(font='small').renderText('FAST UNO\n') + "-" * 38 + "\n")
        return await func(*args, **kwargs)
    return wrapper
