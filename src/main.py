import sys
import os

# Ajouter le dossier parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.utilisateur import Utilisateur
from models.patient import Patient
from models.rendez_vous import RendezVous
from utils.validation import *

print("test deusieme commit")
class ApplicationClinique:
    """
    Application principale de gestion de la clinique.
    """
    
    def __init__(self):
        self.utilisateur_connecte = None
    
    def clear_screen(self):
        """Efface l'écran du terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def afficher_header(self):
        """Affiche l'en-tête de l'application."""
        print("\n" + "="*60)
        print("          SYSTÈME DE GESTION DE CLINIQUE")
        print("="*60)
        if self.utilisateur_connecte:
            print(f"Connecté : {self.utilisateur_connecte['prenom']} {self.utilisateur_connecte['nom']}")
            print(f"Rôle : {self.utilisateur_connecte['role'].capitalize()}")
        print("="*60 + "\n")
    
    def connexion(self):
        """Gère la connexion de l'utilisateur."""
        self.clear_screen()
        print("\n=== CONNEXION ===\n")
        
        email = input("Email : ").strip()
        mot_de_passe = input("Mot de passe : ").strip()
        
        user = Utilisateur.authentifier(email, mot_de_passe)
        
        if user:
            self.utilisateur_connecte = user
            print(f"\n✓ Connexion réussie ! Bienvenue {user['prenom']} {user['nom']}")
            input("\nAppuyez sur Entrée pour continuer...")
            return True
        else:
            print("\n✗ Email ou mot de passe incorrect")
            input("\nAppuyez sur Entrée pour réessayer...")
            return False
    
    def menu_principal(self):
        """Affiche le menu principal selon le rôle."""
        while True:
            self.clear_screen()
            self.afficher_header()
            
            if self.utilisateur_connecte['role'] == 'medecin':
                self.menu_medecin()
            else:
                self.menu_secretaire()
    
    def menu_medecin(self):
        """Menu pour les médecins."""
        print("=== MENU MÉDECIN ===\n")
        print("1. Voir mes rendez-vous")
        print("2. Consulter un patient")
        print("3. Marquer un rendez-vous comme terminé")
        print("4. Rechercher un patient")
        print("5. Voir tous les patients")
        print("0. Déconnexion")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == '1':
            self.voir_rendez_vous_medecin()
        elif choix == '2':
            self.consulter_patient()
        elif choix == '3':
            self.terminer_rendez_vous()
        elif choix == '4':
            self.rechercher_patient()
        elif choix == '5':
            self.lister_tous_patients()
        elif choix == '0':
            self.deconnexion()
        else:
            print("Choix invalide")
            input("\nAppuyez sur Entrée...")
    
    def menu_secretaire(self):
        """Menu pour les secrétaires."""
        print("=== MENU SECRÉTAIRE ===\n")
        print("1. Ajouter un patient")
        print("2. Rechercher un patient")
        print("3. Modifier un patient")
        print("4. Créer un rendez-vous")
        print("5. Voir tous les rendez-vous")
        print("6. Annuler un rendez-vous")
        print("7. Lister tous les patients")
        print("0. Déconnexion")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == '1':
            self.ajouter_patient()
        elif choix == '2':
            self.rechercher_patient()
        elif choix == '3':
            self.modifier_patient()
        elif choix == '4':
            self.creer_rendez_vous()
        elif choix == '5':
            self.voir_tous_rendez_vous()
        elif choix == '6':
            self.annuler_rendez_vous()
        elif choix == '7':
            self.lister_tous_patients()
        elif choix == '0':
            self.deconnexion()
        else:
            print("Choix invalide")
            input("\nAppuyez sur Entrée...")
    
    # === FONCTIONS PATIENTS ===
    
    def ajouter_patient(self):
        """Ajoute un nouveau patient."""
        self.clear_screen()
        print("\n=== AJOUTER UN PATIENT ===\n")
        
        try:
            nom = input("Nom : ").strip()
            prenom = input("Prénom : ").strip()
            date_naissance = saisir_date("Date de naissance")
            sexe = saisir_choix("Sexe (M/F/Autre) : ", ['m', 'f', 'autre']).upper()
            telephone = input("Téléphone : ").strip()
            adresse = input("Adresse (optionnel) : ").strip() or None
            email = input("Email (optionnel) : ").strip() or None
            numero_ss = input("Numéro de sécurité sociale (optionnel) : ").strip() or None
            
            succes, message = Patient.ajouter_patient(
                nom, prenom, date_naissance, sexe, telephone, 
                adresse, email, numero_ss
            )
            
            print(f"\n{'✓' if succes else '✗'} {message}")
            
        except Exception as e:
            print(f"\n✗ Erreur : {e}")
        
        input("\nAppuyez sur Entrée...")
    
    def rechercher_patient(self):
        """Recherche un patient."""
        self.clear_screen()
        print("\n=== RECHERCHER UN PATIENT ===\n")
        
        terme = input("Nom, prénom ou téléphone : ").strip()
        
        patients = Patient.rechercher_patient(terme)
        
        if patients:
            print(f"\n{len(patients)} patient(s) trouvé(s) :\n")
            for p in patients:
                print(f"ID: {p[0]} | {p[1]} {p[2]} | Né(e) le {p[3]} | Tel: {p[5]}")
        else:
            print("\nAucun patient trouvé")
        
        input("\nAppuyez sur Entrée...")
    
    def lister_tous_patients(self):
        """Affiche tous les patients."""
        self.clear_screen()
        print("\n=== LISTE DES PATIENTS ===\n")
        
        patients = Patient.lister_patients()
        
        if patients:
            print(f"Total : {len(patients)} patients\n")
            for p in patients:
                print(f"ID: {p[0]} | {p[1]} {p[2]} | Né(e) le {p[3]} | {p[4]} | Tel: {p[5]}")
        else:
            print("Aucun patient enregistré")
        
        input("\nAppuyez sur Entrée...")
    
    def modifier_patient(self):
        """Modifie les informations d'un patient."""
        self.clear_screen()
        print("\n=== MODIFIER UN PATIENT ===\n")
        
        patient_id = saisir_entier("ID du patient : ", min_val=1)
        
        patient = Patient.obtenir_patient(patient_id)
        if not patient:
            print("\n✗ Patient non trouvé")
            input("\nAppuyez sur Entrée...")
            return
        
        print(f"\nPatient : {patient[1]} {patient[2]}")
        print("\nLaissez vide pour ne pas modifier un champ\n")
        
        nouveau_tel = input(f"Nouveau téléphone ({patient[5]}) : ").strip()
        nouvelle_adresse = input(f"Nouvelle adresse ({patient[6] or 'N/A'}) : ").strip()
        nouvel_email = input(f"Nouvel email ({patient[7] or 'N/A'}) : ").strip()
        
        modifications = {}
        if nouveau_tel:
            modifications['telephone'] = nouveau_tel
        if nouvelle_adresse:
            modifications['adresse'] = nouvelle_adresse
        if nouvel_email:
            modifications['email'] = nouvel_email
        
        if modifications:
            succes, message = Patient.modifier_patient(patient_id, **modifications)
            print(f"\n{'✓' if succes else '✗'} {message}")
        else:
            print("\nAucune modification effectuée")
        
        input("\nAppuyez sur Entrée...")
    
    def consulter_patient(self):
        """Affiche les détails d'un patient (pour médecin)."""
        self.clear_screen()
        print("\n=== CONSULTER UN PATIENT ===\n")
        
        patient_id = saisir_entier("ID du patient : ", min_val=1)
        
        patient = Patient.obtenir_patient(patient_id)
        if not patient:
            print("\n✗ Patient non trouvé")
            input("\nAppuyez sur Entrée...")
            return
        
        print(f"\n--- Informations Patient ---")
        print(f"Nom complet : {patient[1]} {patient[2]}")
        print(f"Date de naissance : {patient[3]}")
        print(f"Sexe : {patient[4]}")
        print(f"Téléphone : {patient[5]}")
        print(f"Adresse : {patient[6] or 'N/A'}")
        print(f"Email : {patient[7] or 'N/A'}")
        print(f"N° Sécurité sociale : {patient[8] or 'N/A'}")
        
        # Afficher les rendez-vous du patient
        rdvs = RendezVous.lister_rendez_vous('patient', patient_id)
        if rdvs:
            print(f"\n--- Rendez-vous ({len(rdvs)}) ---")
            for rdv in rdvs:
                print(f"{rdv[1]} à {rdv[2]} | {rdv[4]} | Médecin: {rdv[6]}")
        
        input("\nAppuyez sur Entrée...")
    
    # === FONCTIONS RENDEZ-VOUS ===
    
    def creer_rendez_vous(self):
        """Crée un nouveau rendez-vous."""
        self.clear_screen()
        print("\n=== CRÉER UN RENDEZ-VOUS ===\n")
        
        patient_id = saisir_entier("ID du patient : ", min_val=1)
        
        # Afficher les médecins disponibles
        medecins = Utilisateur.lister_medecins()
        if not medecins:
            print("\n✗ Aucun médecin disponible")
            input("\nAppuyez sur Entrée...")
            return
        
        print("\nMédecins disponibles :")
        for m in medecins:
            spec = f" ({m[3]})" if m[3] else ""
            print(f"  ID {m[0]} : Dr {m[1]} {m[2]}{spec}")
        
        medecin_id = saisir_entier("\nID du médecin : ", min_val=1)
        date_rdv = saisir_date("Date du rendez-vous")
        heure_rdv = saisir_heure("Heure du rendez-vous")
        motif = input("Motif (optionnel) : ").strip() or None
        
        succes, message = RendezVous.creer_rendez_vous(
            patient_id, medecin_id, date_rdv, heure_rdv, motif
        )
        
        print(f"\n{'✓' if succes else '✗'} {message}")
        input("\nAppuyez sur Entrée...")
    
    def voir_rendez_vous_medecin(self):
        """Affiche les rendez-vous d'un médecin."""
        self.clear_screen()
        print("\n=== MES RENDEZ-VOUS ===\n")
        
        rdvs = RendezVous.lister_rendez_vous('medecin', self.utilisateur_connecte['id'])
        
        if rdvs:
            print(f"Total : {len(rdvs)} rendez-vous\n")
            for rdv in rdvs:
                print(f"ID {rdv[0]} | {rdv[1]} à {rdv[2]} | Patient: {rdv[5]}")
                print(f"  Statut: {rdv[4]} | Motif: {rdv[3] or 'N/A'}\n")
        else:
            print("Aucun rendez-vous")
        
        input("\nAppuyez sur Entrée...")
    
    def voir_tous_rendez_vous(self):
        """Affiche tous les rendez-vous."""
        self.clear_screen()
        print("\n=== TOUS LES RENDEZ-VOUS ===\n")
        
        rdvs = RendezVous.lister_rendez_vous()
        
        if rdvs:
            print(f"Total : {len(rdvs)} rendez-vous\n")
            for rdv in rdvs:
                print(f"ID {rdv[0]} | {rdv[1]} à {rdv[2]}")
                print(f"  Patient: {rdv[5]} | Médecin: {rdv[6]}")
                print(f"  Statut: {rdv[4]} | Motif: {rdv[3] or 'N/A'}\n")
        else:
            print("Aucun rendez-vous")
        
        input("\nAppuyez sur Entrée...")
    
    def terminer_rendez_vous(self):
        """Marque un rendez-vous comme terminé."""
        self.clear_screen()
        print("\n=== TERMINER UN RENDEZ-VOUS ===\n")
        
        rdv_id = saisir_entier("ID du rendez-vous : ", min_val=1)
        notes = input("Notes (optionnel) : ").strip() or None
        
        succes, message = RendezVous.modifier_statut(rdv_id, 'termine', notes)
        print(f"\n{'✓' if succes else '✗'} {message}")
        
        input("\nAppuyez sur Entrée...")
    
    def annuler_rendez_vous(self):
        """Annule un rendez-vous."""
        self.clear_screen()
        print("\n=== ANNULER UN RENDEZ-VOUS ===\n")
        
        rdv_id = saisir_entier("ID du rendez-vous : ", min_val=1)
        
        if confirmer_action("Confirmer l'annulation ?"):
            succes, message = RendezVous.modifier_statut(rdv_id, 'annule')
            print(f"\n{'✓' if succes else '✗'} {message}")
        else:
            print("\nAnnulation abandonnée")
        
        input("\nAppuyez sur Entrée...")
    
    def deconnexion(self):
        """Déconnexion de l'utilisateur."""
        if confirmer_action("\nVoulez-vous vraiment vous déconnecter ?"):
            self.utilisateur_connecte = None
            print("\n✓ Déconnexion réussie")
            return True
        return False
    
    def demarrer(self):
        """Démarre l'application."""
        print("\n" + "="*60)
        print("   Bienvenue dans le Système de Gestion de Clinique")
        print("="*60)
        
        while True:
            if not self.utilisateur_connecte:
                if not self.connexion():
                    if not confirmer_action("\nVoulez-vous réessayer ?"):
                        print("\nAu revoir !")
                        break
                else:
                    self.menu_principal()
                    if not self.utilisateur_connecte:
                        continue

if __name__ == "__main__":
    app = ApplicationClinique()
    app.demarrer()