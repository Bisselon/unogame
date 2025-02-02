# Importation des bibliothèques nécessaires
import psycopg2
import json
import os
from dotenv import load_dotenv

# Importation des constantes
import constantes as c

# Chargement des variables d'environnement
load_dotenv()

class Database:
    connection: psycopg2.extensions.connection = None
    cursor: psycopg2.extensions.cursor = None

    def __init__(self) -> None:
        try: # Connexion à la base de données
            self.connection: psycopg2.extensions.connection = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST")
            )
            self.cursor: psycopg2.extensions.cursor = self.connection.cursor()
            self.creer_la_table()
        except psycopg2.Error as e: # Si la connexion à la base de données échoue
            print(f"{c.RED}Erreur de connexion à la base de données : {e}{c.RESET}")
    
    def creer_la_table(self) -> bool:
        """Crée la table parties si elle n'existe pas.
        
        Retourne : True si la table a été créée, False sinon.
        """
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS parties (
                    id SERIAL PRIMARY KEY,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                joueurs TEXT[] NOT NULL,
                gagnant VARCHAR(200)
            );
            """)
            self.connection.commit()
            return True
        except psycopg2.Error as e:
            input(f"Erreur lors de la création de la table : {e}")
            return False

    def ajouter_une_partie(self, joueurs: list[str], gagnant: str) -> bool:
        """Ajoute une partie à la base de données.
        
        Retourne : True si la partie a été ajoutée, False sinon.
        """
        try:
            sql = "INSERT INTO parties (joueurs, gagnant) VALUES (%s, %s)"
            self.cursor.execute(sql, (joueurs, gagnant))
            self.connection.commit()
            return True
        except psycopg2.Error as e:
            print(f"Erreur lors de l'ajout de la partie : {e}")
            return False

    def recuperer_les_parties(self) -> list[tuple]:
        """Récupère toutes les parties de la base de données.
        
        Retourne : la liste des parties.
        """
        sql = "SELECT * FROM parties"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
