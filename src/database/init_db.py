from .config import get_connection, close_connection

def create_tables():
    """
    Crée toutes les tables nécessaires pour l'application.
    """
    connection = get_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Table des utilisateurs (médecins et secrétaires)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(100) NOT NULL,
                prenom VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                mot_de_passe VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL CHECK (role IN ('medecin', 'secretaire')),
                specialite VARCHAR(100),
                telephone VARCHAR(20),
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des patients
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(100) NOT NULL,
                prenom VARCHAR(100) NOT NULL,
                date_naissance DATE NOT NULL,
                sexe VARCHAR(10) CHECK (sexe IN ('M', 'F', 'Autre')),
                adresse TEXT,
                telephone VARCHAR(20) NOT NULL,
                email VARCHAR(150),
                numero_securite_sociale VARCHAR(50),
                date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des rendez-vous
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rendez_vous (
                id SERIAL PRIMARY KEY,
                patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
                medecin_id INTEGER REFERENCES utilisateurs(id) ON DELETE CASCADE,
                date_rdv DATE NOT NULL,
                heure_rdv TIME NOT NULL,
                motif TEXT,
                statut VARCHAR(20) DEFAULT 'planifie' 
                    CHECK (statut IN ('planifie', 'termine', 'annule')),
                notes TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(medecin_id, date_rdv, heure_rdv)
            )
        ''')
        
        connection.commit()
        print("✓ Tables créées avec succès!")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de la création des tables : {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_connection(connection)

def insert_default_users():
    """
    Insère des utilisateurs par défaut pour tester l'application.
    """
    connection = get_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Vérifier si des utilisateurs existent déjà
        cursor.execute("SELECT COUNT(*) FROM utilisateurs")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Médecin par défaut
            cursor.execute('''
                INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role, specialite, telephone)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', ('Diop', 'Amadou', 'dr.diop@clinique.sn', 'medecin123', 'medecin', 'Cardiologie', '771234567'))
            
            # Secrétaire par défaut
            cursor.execute('''
                INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role, telephone)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', ('Ndiaye', 'Fatou', 'secretaire@clinique.sn', 'secretaire123', 'secretaire', '776543210'))
            
            connection.commit()
            print("✓ Utilisateurs par défaut créés!")
            print("\nComptes de test :")
            print("  Médecin : dr.diop@clinique.sn / medecin123")
            print("  Secrétaire : secretaire@clinique.sn / secretaire123")
        else:
            print("Des utilisateurs existent déjà.")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de l'insertion des utilisateurs : {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_connection(connection)

if __name__ == "__main__":
    print("Initialisation de la base de données...")
    if create_tables():
        insert_default_users()