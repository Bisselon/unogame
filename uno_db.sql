CREATE DATABASE fast_uno;

CREATE TABLE parties (
    id SERIAL PRIMARY KEY, -- Identifiant de la partie
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date de la partie
    joueurs TEXT[] NOT NULL,  -- Tableau de joueurs
    gagnant VARCHAR(200)  -- Nom du gagnant
);