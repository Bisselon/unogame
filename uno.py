# Importation des modules
from typing import Self
from InquirerPy import inquirer
import pandas as pd
import random
import asyncio

# Importation des classes
from joueur import Joueur
from carte_uno import Carte_Uno
from database import Database

# Importation des modules
import fonctions as f

# Importation des constantes
import constantes as c

class Uno():
    _joueurs: list[Joueur]
    _cartes: list[Carte_Uno]
    _pile: list[Carte_Uno]

    def __init__(self) -> None:
        self._joueurs: list[Joueur] = []
        self._cartes: list[Carte_Uno] = []
        self._pile: list[Carte_Uno] = []

    @property
    def joueurs(self) -> list[Joueur]:
        """Liste des joueurs."""
        return self._joueurs
    
    def ajouter_joueur(self, joueur: Joueur) -> None:
        """Ajouter un joueur à la liste des joueurs."""
        self._joueurs.append(joueur)

    def retirer_joueur(self, joueur: Joueur) -> None:
        """Retirer un joueur de la liste des joueurs."""
        self._joueurs.remove(joueur)

    @property
    def cartes(self) -> list[Carte_Uno]:
        """Liste des cartes."""
        return self._cartes

    @cartes.setter
    def cartes(self, cartes: list[Carte_Uno]) -> None:
        """Définir la liste des cartes."""
        self._cartes = cartes

    def ajouter_carte(self, carte: Carte_Uno) -> None:
        """Ajouter une carte à la liste des cartes."""
        self._cartes.append(carte)

    @property
    def pile(self) -> list[Carte_Uno]:
        """Liste des cartes de la pile."""
        return self._pile
    
    @pile.setter
    def pile(self, pile: list[Carte_Uno]) -> None:
        """Définir la liste des cartes de la pile."""
        self._pile = pile

    def ajouter_carte_a_la_pile(self, carte: Carte_Uno) -> None:
        """Ajouter une carte à la pile."""
        self._pile.append(carte)

    @f.afficher_logo
    async def choisir_les_joueurs(self) -> list[Joueur]:
        """Choisit les joueurs pour la partie.

        Retourne : la liste des joueurs.
        """

        nombre_de_joueurs: int = int(await inquirer.number(message="Nombre de joueurs (min 2, max 8)", min_allowed=2, max_allowed=8).execute_async())
        
        for i in range(nombre_de_joueurs):
            print(f"\n> Joueur n°{i+1}")

            # Vérifier si le nom du joueur est déjà utilisé
            while True:
                nom_du_joueur = await inquirer.text(message=f"Nom du joueur {i+1} :", validate=lambda x: len(x) > 0, invalid_message="Le nom du joueur ne peut pas être vide").execute_async()
                if nom_du_joueur in [joueur.nom for joueur in self.joueurs]:
                    print(f"{c.RED}! Ce nom est déjà utilisé{c.RESET}")
                else:
                    break

            type_joueur: str = await inquirer.select(message="Type du joueur", choices=["Humain", "Robot"]).execute_async()

            self.ajouter_joueur(Joueur(nom=nom_du_joueur, type=type_joueur))

        return self.joueurs

    def generer_les_cartes(self) -> list[Carte_Uno]:
        """Génère un jeu de cartes Uno.

        Retourne : la liste des cartes générées.
        """
        for i in range(7 * len(self.joueurs)):
            carte = Carte_Uno.generer_une_carte()
            self.ajouter_carte(carte)
        return self.cartes

    def distribuer_les_cartes(self) -> list[Joueur]:
        """Distribue les cartes aux joueurs.

        Retourne : la liste des joueurs avec leurs cartes.
        """
        for joueur in self.joueurs:
            for i in range(7):
                carte = self.cartes.pop()
                carte.index = i
                joueur._cartes.append(carte)
        return self.joueurs

    @f.afficher_logo
    async def lancer_une_partie(self) -> dict:
        """Lance une partie de UNO.
        
        Retourne : {"joueurs": list[str], "gagnant": str}.
        """

        # Génération et distribution des cartes
        self.cartes = self.generer_les_cartes()
        self.distribuer_les_cartes()

        # Lancement de la partie
        while True:
            for joueur in self.joueurs: # Pour chaque joueur

                print(f"\n{c.YELLOW}C'est au tour de {joueur.nom} ({joueur.nombre_de_cartes} cartes restantes){c.RESET}")
                carte_jouee = await joueur.jouer_une_carte(self.pile)

                if carte_jouee and carte_jouee.valeur not in c.CARTES_SPECIALES:
                    self.ajouter_carte_a_la_pile(carte_jouee)

                # Gérer les cartes spéciales (ajout de cartes, inversion de la direction, passer le tour, échanger les cartes, changer de couleur la pile)
                if carte_jouee:
                    match carte_jouee.valeur: 
                        case "Inverse": # Inverser la direction du jeu
                            self.joueurs.reverse()
                            print(f"{c.CYAN}> {joueur.nom} a inversé la direction du jeu{c.RESET}")

                        case "Plus2": # Ajouter 2 cartes à la main du joueur suivant
                            index_prochain_joueur = self.joueurs.index(joueur) + 1
                            if index_prochain_joueur >= len(self.joueurs):
                                index_prochain_joueur = 0
                            for i in range(2):
                                nouvelle_carte = Carte_Uno.generer_une_carte()
                                nouvelle_carte.index = len(self.joueurs[index_prochain_joueur].cartes) - 1
                                self.joueurs[index_prochain_joueur].cartes.append(nouvelle_carte)

                            print(f"{c.CYAN}> {joueur.nom} a ajouté 2 cartes à {self.joueurs[index_prochain_joueur].nom}{c.RESET}")

                        case "Passer": # Passer le tour
                            print(f"{c.CYAN}> {joueur.nom} a passé son tour{c.RESET}")

                        case "ChangerCouleur": # Changer la couleur de la pile
                            nouvelle_couleur = ""
                            if joueur.type == "Humain":
                                nouvelle_couleur = await inquirer.select(message="Choisir une couleur", choices=c.CARTES_COULEURS).execute_async()
                            elif joueur.type == "Robot":
                                await asyncio.sleep(1) # Simulation de la recherche de la carte par le robot
                                nouvelle_couleur = random.choice(c.CARTES_COULEURS)

                            if self.pile:
                                self.pile[-1].couleur = nouvelle_couleur
                            else:
                                self.pile.append(Carte_Uno(couleur=nouvelle_couleur))

                            print(f"{c.CYAN}> {joueur.nom} a changé la couleur de la pile en {nouvelle_couleur}{c.RESET}")

                        case "EchangerCartes": # Echanger les cartes avec le joueur suivant
                            index_prochain_joueur = self.joueurs.index(joueur) + 1
                            if index_prochain_joueur >= len(self.joueurs):
                                index_prochain_joueur = 0
                            self.joueurs[index_prochain_joueur].cartes, joueur.cartes = joueur.cartes, self.joueurs[index_prochain_joueur].cartes

                            print(f"{c.CYAN}> {joueur.nom} a échangé les cartes avec {self.joueurs[index_prochain_joueur].nom}{c.RESET}")

                        case _:
                            print(f"{c.CYAN}> {joueur.nom} a joué la carte : {c.CYAN}{carte_jouee.couleur} {carte_jouee.valeur}{c.RESET}")

                # Vérifier si le joueur a gagné la partie (aucune carte)
                if not joueur._cartes:
                    print(f"\n{c.GREEN}{joueur.nom} a gagné la partie !!!{c.RESET}")

                    return {
                        "joueurs": [joueur.nom for joueur in self.joueurs],
                        "gagnant": joueur.nom
                    }
