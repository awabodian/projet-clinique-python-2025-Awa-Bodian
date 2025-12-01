from database.config import get_connection, close_connection

class Utilisateur:
    """
    Classe pour gérer l'authentification et les utilisateurs.
    """
    
    @staticmethod
    def authentifier(email, mot_de_passe):
        """
        Authentifie un utilisateur et retourne ses informations.
        """
        connection = get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT id, nom, prenom, email, role, specialite
                FROM utilisateurs
                WHERE email = %s AND mot_de_passe = %s
            ''', (email, mot_de_passe))
            
            user = cursor.fetchone()
            
            if user:
                return {
                    'id': user[0],
                    'nom': user[1],
                    'prenom': user[2],
                    'email': user[3],
                    'role': user[4],
                    'specialite': user[5]
                }
            return None
            
        except Exception as e:
            print(f"Erreur d'authentification : {e}")
            return None
        finally:
            cursor.close()
            close_connection(connection)
    
    @staticmethod
    def lister_medecins():
        """
        Récupère la liste de tous les médecins.
        """
        connection = get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT id, nom, prenom, specialite, telephone
                FROM utilisateurs
                WHERE role = 'medecin'
                ORDER BY nom, prenom
            ''')
            
            medecins = cursor.fetchall()
            return medecins
            
        except Exception as e:
            print(f"Erreur : {e}")
            return []
        finally:
            cursor.close()
            close_connection(connection)
    
    @staticmethod
    def ajouter_utilisateur(nom, prenom, email, mot_de_passe, role, specialite=None, telephone=None):
        """
        Ajoute un nouvel utilisateur (médecin ou secrétaire).
        """
        connection = get_connection()
        if not connection:
            return False, "Erreur de connexion"
        
        try:
            cursor = connection.cursor()
            
            # Vérifier que l'email n'existe pas déjà
            cursor.execute("SELECT id FROM utilisateurs WHERE email = %s", (email,))
            if cursor.fetchone():
                return False, "Cet email est déjà utilisé"
            
            # Valider le rôle
            if role not in ['medecin', 'secretaire']:
                return False, "Rôle invalide (medecin ou secretaire)"
            
            cursor.execute('''
                INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role, specialite, telephone)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (nom, prenom, email, mot_de_passe, role, specialite, telephone))
            
            user_id = cursor.fetchone()[0]
            connection.commit()
            
            return True, f"Utilisateur créé avec succès (ID: {user_id})"
            
        except Exception as e:
            connection.rollback()
            return False, f"Erreur : {str(e)}"
        finally:
            cursor.close()
            close_connection(connection)