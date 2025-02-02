# Importation des modules
import asyncio
from InquirerPy import inquirer
import pandas as pd
from tabulate import tabulate

# Importation des classes
from joueur import Joueur
from uno import Uno
from carte_uno import Carte_Uno
from database import Database

# Importation des fonctions
import fonctions as f

# Importation des constantes
import constantes as c

class Jeu(Database):
    def __init__(self) -> None:
        # Initialisation de la base de données
        super().__init__()

    @f.afficher_logo
    async def menu_principal(self) -> None:
        print("Créé par : Bisselon\n")

        if self.connection:
            print(f"{c.GREEN}Base de données connectée, sauvegarde des parties activée{c.RESET}\n")
        else:
            print(f"{c.RED}Connexion à la base de données échouée, aucune sauvegarde des parties{c.RESET}\n")

        menu_principal: str = await inquirer.select(message="MENU PRINCIPAL", choices=[
            "Lancer une partie",
            "Historique des parties",
            "Quitter"
        ]).execute_async()

        match menu_principal:
            case "Lancer une partie":
                jeu: Uno = Uno()
                joueurs: list[Joueur] = await jeu.choisir_les_joueurs()
                partie = await jeu.lancer_une_partie()

                if self.connection:
                    self.ajouter_une_partie(joueurs=partie["joueurs"], gagnant=partie["gagnant"]) # Ajouter la partie à la base de données

                input("\nAppuyer sur Entrée pour retourner au menu principal...")
                return await self.menu_principal()

            case "Historique des parties":
                if self.connection:
                    parties: list[tuple] = self.recuperer_les_parties()
                    dataframe = pd.DataFrame(parties, columns=['ID', 'DATE', 'JOUEURS', 'GAGNANT'])
                    print(tabulate(dataframe, headers=dataframe.columns, tablefmt="fancy_grid", showindex="never", numalign="center"))
                    input("\nAppuyez sur Entrée pour retourner au menu principal...")
                return await self.menu_principal()

            case "Quitter":
                print("Merci d'avoir joué à FAST UNO !")
                await asyncio.sleep(1)
                exit()

if __name__ == "__main__":
    asyncio.run(Jeu().menu_principal())