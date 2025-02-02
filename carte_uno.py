# Importation des modules nécessaires
from typing import Self
import random

# Importation des constantes
import constantes as c

class Carte_Uno:
    """Représente une carte de UNO."""
    index: int
    valeur: str
    couleur: str

    def __init__(self, valeur: str = "", couleur: str = "") -> Self:
        self.valeur: str = valeur
        self.couleur: str = couleur

    @staticmethod
    def generer_une_carte() -> Self:
        """Génère une carte Uno.
        
        Retourne : une carte Uno.
        """
        
        if random.random() < 0.10:  # 10% de chance d'avoir une carte spéciale
            carte = Carte_Uno(valeur=random.choice(c.CARTES_SPECIALES))
        else:  # 90% de chance d'avoir une carte normale
            carte = Carte_Uno(couleur=random.choice(c.CARTES_COULEURS), valeur=random.choice(c.CARTES_VALEURS))
        return carte
        