from database.config import get_connection, close_connection
from datetime import datetime

class RendezVous:
    """
    Classe pour gérer les rendez-vous.
    """
    
    @staticmethod
    def creer_rendez_vous(patient_id, medecin_id, date_rdv, heure_rdv, motif=None):
        """
        Crée un nouveau rendez-vous.
        """
        connection = get_connection()
        if not connection:
            return False, "Erreur de connexion"
        
        try:
            cursor = connection.cursor()
            
            # Vérifier que le patient existe
            cursor.execute("SELECT id FROM patients WHERE id = %s", (patient_id,))
            if not cursor.fetchone():
                return False, "Patient non trouvé"
            
            # Vérifier que le médecin existe
            cursor.execute("SELECT id FROM utilisateurs WHERE id = %s AND role = 'medecin'", (medecin_id,))
            if not cursor.fetchone():
                return False, "Médecin non trouvé"
            
            # Vérifier la disponibilité (pas de conflit d'horaire)
            cursor.execute('''
                SELECT id FROM rendez_vous 
                WHERE medecin_id = %s AND date_rdv = %s AND heure_rdv = %s 
                AND statut != 'annule'
            ''', (medecin_id, date_rdv, heure_rdv))
            
            if cursor.fetchone():
                return False, "Ce créneau horaire n'est pas disponible"
            
            # Créer le rendez-vous
            cursor.execute('''
                INSERT INTO rendez_vous (patient_id, medecin_id, date_rdv, heure_rdv, motif)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            ''', (patient_id, medecin_id, date_rdv, heure_rdv, motif))
            
            rdv_id = cursor.fetchone()[0]
            connection.commit()
            
            return True, f"Rendez-vous créé avec succès (ID: {rdv_id})"
            
        except Exception as e:
            connection.rollback()
            return False, f"Erreur : {str(e)}"
        finally:
            cursor.close()
            close_connection(connection)
    
    @staticmethod
    def lister_rendez_vous(filtre=None, valeur=None):
        """
        Liste les rendez-vous avec filtres optionnels.
        filtre peut être : 'medecin', 'patient', 'date', 'statut'
        """
        connection = get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            
            query = '''
                SELECT r.id, r.date_rdv, r.heure_rdv, r.motif, r.statut,
                       p.nom || ' ' || p.prenom as patient,
                       u.nom || ' ' || u.prenom as medecin
                FROM rendez_vous r
                JOIN patients p ON r.patient_id = p.id
                JOIN utilisateurs u ON r.medecin_id = u.id
            '''
            
            params = []
            if filtre and valeur:
                if filtre == 'medecin':
                    query += " WHERE r.medecin_id = %s"
                    params.append(valeur)
                elif filtre == 'patient':
                    query += " WHERE r.patient_id = %s"
                    params.append(valeur)
                elif filtre == 'date':
                    query += " WHERE r.date_rdv = %s"
                    params.append(valeur)
                elif filtre == 'statut':
                    query += " WHERE r.statut = %s"
                    params.append(valeur)
            
            query += " ORDER BY r.date_rdv DESC, r.heure_rdv DESC"
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            rendez_vous = cursor.fetchall()
            return rendez_vous
            
        except Exception as e:
            print(f"Erreur lors de la récupération des rendez-vous : {e}")
            return []
        finally:
            cursor.close()
            close_connection(connection)
    
    @staticmethod
    def modifier_statut(rdv_id, nouveau_statut, notes=None):
        """
        Modifie le statut d'un rendez-vous (planifie, termine, annule).
        """
        connection = get_connection()
        if not connection:
            return False, "Erreur de connexion"
        
        try:
            cursor = connection.cursor()
            
            statuts_valides = ['planifie', 'termine', 'annule']
            if nouveau_statut not in statuts_valides:
                return False, f"Statut invalide. Utilisez : {', '.join(statuts_valides)}"
            
            if notes:
                cursor.execute('''
                    UPDATE rendez_vous 
                    SET statut = %s, notes = %s 
                    WHERE id = %s
                ''', (nouveau_statut, notes, rdv_id))
            else:
                cursor.execute('''
                    UPDATE rendez_vous 
                    SET statut = %s 
                    WHERE id = %s
                ''', (nouveau_statut, rdv_id))
            
            connection.commit()
            
            if cursor.rowcount > 0:
                return True, f"Statut modifié en '{nouveau_statut}'"
            else:
                return False, "Rendez-vous non trouvé"
            
        except Exception as e:
            connection.rollback()
            return False, f"Erreur : {str(e)}"
        finally:
            cursor.close()
            close_connection(connection)
    
    @staticmethod
    def supprimer_rendez_vous(rdv_id):
        """
        Supprime un rendez-vous.
        """
        connection = get_connection()
        if not connection:
            return False, "Erreur de connexion"
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM rendez_vous WHERE id = %s", (rdv_id,))
            connection.commit()
            
            if cursor.rowcount > 0:
                return True, "Rendez-vous supprimé"
            else:
                return False, "Rendez-vous non trouvé"
            
        except Exception as e:
            connection.rollback()
            return False, f"Erreur : {str(e)}"
        finally:
            cursor.close()
            close_connection(connection)