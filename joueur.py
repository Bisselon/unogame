# Importation des modules
from typing import Self
import random
from InquirerPy import inquirer
import asyncio

# Importation des classes
from carte_uno import Carte_Uno

# Importation des constantes
import constantes as c

class Joueur:
    """
    Représente un joueur de UNO.

    Attributs:
        :nom (str): Nom du joueur
        :type (str): Type du joueur
        :place (int): Position du joueur dans la partie
        :cartes (list[Carte_Uno]): Liste des cartes en main du joueur

    Retourne:
        Joueur: Un joueur de UNO.
    """
    _nom: str
    _type: str
    _cartes: list[Carte_Uno]
    
    def __init__(self, nom: str, type: str) -> None:
        self._nom: str = nom
        self._type: str = type
        self._cartes: list[Carte_Uno] = []

    @property
    def nom(self) -> str:
        """Nom du joueur."""
        return self._nom
    
    @nom.setter
    def nom(self, value: str) -> str:
        """Définir le nom du joueur."""
        self._nom = value

    @property
    def type(self) -> str:
        """Type du joueur."""
        return self._type
    
    @type.setter
    def type(self, value: str) -> str:
        """Définir le type du joueur."""
        self._type = value

    @property
    def nombre_de_cartes(self) -> int:
        """Nombre de cartes en main du joueur."""
        return len(self.cartes)

    @property
    def cartes(self) -> list[Carte_Uno]:
        """Liste des cartes en main du joueur."""
        return self._cartes

    @cartes.setter
    def cartes(self, value: list[Carte_Uno]) -> None:
        """Définir la liste des cartes en main du joueur."""
        self._cartes = value


    def ajouter_carte(self) -> None:
        """Ajoute une carte à la main du joueur."""
        nouvelle_carte = Carte_Uno.generer_une_carte()
        nouvelle_carte.index = self.nombre_de_cartes - 1 # Mettre à jour l'index de la carte
        self.cartes.append(nouvelle_carte)
        return

    def retirer_carte(self, index: int) -> None:
        """Retire une carte de la main du joueur."""
        # Retirer la carte avec l'index spécifié
        for carte in self.cartes:
            if carte.index == index:
                self.cartes.remove(carte)
                break
        
        # Mettre à jour les index des cartes restantes et la liste
        cartes_mises_a_jour = []
        for i, carte in enumerate(self.cartes):
            carte.index = i
            cartes_mises_a_jour.append(carte)
        
        self.cartes = cartes_mises_a_jour # Mettre à jour la liste des cartes
        return

    def verifier_cartes_jouables(self, pile: list[Carte_Uno]) -> list[Carte_Uno]:
        """Vérifie si les cartes sont jouables.
        
        Retourne : la liste des cartes jouables.
        """
        cartes_jouables = []
        
        # Si la pile n'est pas vide, on vérifie si les cartes sont jouables
        if pile:
            
            carte_en_haut_de_la_pile = ""
            if (pile[-1].couleur):
                carte_en_haut_de_la_pile += pile[-1].couleur
            if (pile[-1].valeur):
                carte_en_haut_de_la_pile += " " + pile[-1].valeur

            print(f"{c.PURPLE}Carte en haut de la pile : {carte_en_haut_de_la_pile}{c.RESET}")

    
            for carte in self.cartes:
                # Vérifie si la carte correspond en couleur ou en valeur
                if carte.couleur == pile[-1].couleur or carte.valeur == pile[-1].valeur:
                    cartes_jouables.append(carte)
                # Vérifie si c'est une carte spéciale (qui change la couleur)
                elif carte.valeur in c.CARTES_SPECIALES and carte.couleur is None:
                    cartes_jouables.append(carte)
                

        else: # Si la pile est vide, le joueur peut jouer n'importe quelle carte (début de la partie)
            cartes_jouables = self.cartes

        return cartes_jouables

    async def jouer_une_carte(self, pile: list[Carte_Uno]) -> Carte_Uno | bool:
        """Jouer une carte.
        
        Retourne : la carte jouée ou False si le joueur n'a pas de carte jouable.
        """
        # Vérification si le joueur a une carte qui correspond à la carte en haut de la pile
        cartes_jouables = self.verifier_cartes_jouables(pile)

        # Vérification si le joueur a une carte qui correspond à la carte en haut de la pile
        if cartes_jouables:
            # Demander au joueur de choisir une carte
            if self.type == "Humain":
                carte_jouee = await inquirer.select(message=f"Choisir une carte", choices=[f"n°{carte.index} - {carte.couleur} {carte.valeur}" for carte in cartes_jouables]).execute_async()
                index = int(carte_jouee.split("n°")[1].split(" ")[0]) # Index de la carte choisie
            elif self.type == "Robot":
                await asyncio.sleep(1) # Simulation de la recherche de la carte par le robot
                carte_jouee = random.choice(cartes_jouables)
                index = carte_jouee.index
            
            # Récupérer la carte choisie
            carte_jouee = self.cartes[index]

            # Retirer la carte choisie du joueur de sa liste de cartes
            self.retirer_carte(index) 
            return carte_jouee

        else: # Si le joueur n'a pas de carte jouable
            self.ajouter_carte()
            print(f"{c.CYAN}> {self.nom} a dû piocher une carte{c.RESET}")
            await asyncio.sleep(1)
            return
