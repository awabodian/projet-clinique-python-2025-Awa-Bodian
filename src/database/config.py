import psycopg2
from psycopg2 import Error

# Configuration de la connexion à PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'database': 'clinique_db',
    'user': 'postgres',  # Changez si nécessaire
    'password': 'root',  # CHANGEZ CE MOT DE PASSE
    'port': '5432'
}

def get_connection():
    """
    Crée et retourne une connexion à la base de données PostgreSQL.
    """
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Erreur lors de la connexion à PostgreSQL : {e}")
        return None

def close_connection(connection):
    """
    Ferme la connexion à la base de données.
    """
    if connection:
        connection.close()
        print("Connexion PostgreSQL fermée")