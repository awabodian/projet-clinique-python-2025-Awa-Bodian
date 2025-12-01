from database.config import get_connection, close_connection
from datetime import datetime

class Patient:
    """
    Classe pour gérer les opérations CRUD des patients.
    """
    
    @staticmethod
    def ajouter_patient(nom, prenom, date_naissance, sexe, telephone, adresse=None, email=None, numero_ss=None):
        """
        Ajoute un nouveau patient dans la base de données.
        """
        connection = get_connection()
        if not connection:
            return False, "Erreur de connexion à la base de données"
        
        try:
            cursor = connection.cursor()
            
            # Validation du téléphone
            if not telephone or len(telephone) < 9:
                return False, "Numéro de téléphone invalide"
            
            # Validation de la date de naissance
            try:
                date_obj = datetime.strptime(date_naissance, '%Y-%m-%d')
                if date_obj > datetime.now():
                    return False, "La date de naissance ne peut pas être dans le futur"
            except ValueError:
                return False, "Format de date invalide (utilisez YYYY-MM-DD)"
            
            cursor.execute('''
                INSERT INTO patients (nom, prenom, date_naissance, sexe, telephone, adresse, email, numero_securite_sociale)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (nom.strip(), prenom.strip(), date_naissance, sexe, telephone, adresse, email, numero_ss))
            
            patient_id = cursor.fetchone()[0]
            connection.commit()
            
            return True, f"Patient ajouté avec succès (ID: {patient_id})"
            
        except Exception as e:
            connection.rollback()
            return False, f"Erreur lors de l'ajout du patient : {str(e)}"
        finally:
            cursor.close()
            close_connection(connection)
    
    @staticmethod
    def lister_patients():
        """
        Récupère tous les patients.
        """
        connection = get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT id, nom, prenom, date_naissance, sexe, telephone, email
                FROM patients
                ORDER BY nom, prenom
            ''')
            
            patients = cursor.fetchall()
            return patients
            
        except Exception as e:
            print(f"Erreur lors de la récupération des patients : {e}")
            return []
        finally:
            cursor.close()
            close_connection(connection)
    
    @staticmethod
    def rechercher_patient(terme_recherche):
        """
        Recherche un patient par nom, prénom ou téléphone.
        """
        connection = get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            pattern = f"%{terme_recherche}%"
            cursor.execute('''
                SELECT id, nom, prenom, date_naissance, sexe, telephone, email
                FROM patients
                WHERE nom ILIKE %s OR prenom ILIKE %s OR telephone LIKE %s
                ORDER BY nom, prenom
            ''', (pattern, pattern, pattern))
            
            patients = cursor.fetchall()
            return patients
            
        except Exception as e:
            print(f"Erreur lors de la recherche : {e}")
            return []
        finally:
            cursor.close()
            close_connection(connection)
    
    @staticmethod
    def obtenir_patient(patient_id):
        """
        Récupère les informations détaillées d'un patient.
        """
        connection = get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT id, nom, prenom, date_naissance, sexe, telephone, 
                       adresse, email, numero_securite_sociale, date_inscription
                FROM patients
                WHERE id = %s
            ''', (patient_id,))
            
            patient = cursor.fetchone()
            return patient
            
        except Exception as e:
            print(f"Erreur lors de la récupération du patient : {e}")
            return None
        finally:
            cursor.close()
            close_connection(connection)
    
    @staticmethod
    def modifier_patient(patient_id, **kwargs):
        """
        Modifie les informations d'un patient.
        kwargs peut contenir : nom, prenom, telephone, adresse, email, etc.
        """
        connection = get_connection()
        if not connection:
            return False, "Erreur de connexion"
        
        try:
            cursor = connection.cursor()
            
            # Construire la requête dynamiquement
            champs_autorises = ['nom', 'prenom', 'telephone', 'adresse', 'email', 'sexe']
            champs_a_modifier = []
            valeurs = []
            
            for champ, valeur in kwargs.items():
                if champ in champs_autorises and valeur is not None:
                    champs_a_modifier.append(f"{champ} = %s")
                    valeurs.append(valeur)
            
            if not champs_a_modifier:
                return False, "Aucun champ à modifier"
            
            valeurs.append(patient_id)
            query = f"UPDATE patients SET {', '.join(champs_a_modifier)} WHERE id = %s"
            
            cursor.execute(query, valeurs)
            connection.commit()
            
            if cursor.rowcount > 0:
                return True, "Patient modifié avec succès"
            else:
                return False, "Patient non trouvé"
            
        except Exception as e:
            connection.rollback()
            return False, f"Erreur : {str(e)}"
        finally:
            cursor.close()
            close_connection(connection)
    
    @staticmethod
    def supprimer_patient(patient_id):
        """
        Supprime un patient (et ses rendez-vous associés).
        """
        connection = get_connection()
        if not connection:
            return False, "Erreur de connexion"
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
            connection.commit()
            
            if cursor.rowcount > 0:
                return True, "Patient supprimé avec succès"
            else:
                return False, "Patient non trouvé"
            
        except Exception as e:
            connection.rollback()
            return False, f"Erreur : {str(e)}"
        finally:
            cursor.close()
            close_connection(connection)