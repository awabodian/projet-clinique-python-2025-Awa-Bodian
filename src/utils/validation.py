import re
from datetime import datetime

def valider_email(email):
    """
    Valide le format d'un email.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def valider_telephone(telephone):
    """
    Valide un numéro de téléphone sénégalais.
    """
    # Accepte les formats : 771234567, 77 123 45 67, +221771234567
    telephone = telephone.replace(' ', '').replace('+221', '')
    return len(telephone) == 9 and telephone.isdigit()

def valider_date(date_str, format='%Y-%m-%d'):
    """
    Valide le format d'une date.
    """
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def valider_heure(heure_str, format='%H:%M'):
    """
    Valide le format d'une heure.
    """
    try:
        datetime.strptime(heure_str, format)
        return True
    except ValueError:
        return False

def saisir_entier(message, min_val=None, max_val=None):
    """
    Demande la saisie d'un entier avec validation.
    """
    while True:
        try:
            valeur = int(input(message))
            if min_val is not None and valeur < min_val:
                print(f"La valeur doit être au moins {min_val}")
                continue
            if max_val is not None and valeur > max_val:
                print(f"La valeur doit être au maximum {max_val}")
                continue
            return valeur
        except ValueError:
            print("Veuillez entrer un nombre entier valide")

def saisir_choix(message, options):
    """
    Demande un choix parmi une liste d'options.
    """
    while True:
        choix = input(message).strip().lower()
        if choix in options:
            return choix
        print(f"Choix invalide. Options disponibles : {', '.join(options)}")

def saisir_date(message):
    """
    Demande la saisie d'une date avec validation.
    """
    while True:
        date_str = input(f"{message} (YYYY-MM-DD) : ").strip()
        if valider_date(date_str):
            return date_str
        print("Format de date invalide. Utilisez YYYY-MM-DD (ex: 2024-12-25)")

def saisir_heure(message):
    """
    Demande la saisie d'une heure avec validation.
    """
    while True:
        heure_str = input(f"{message} (HH:MM) : ").strip()
        if valider_heure(heure_str):
            return heure_str
        print("Format d'heure invalide. Utilisez HH:MM (ex: 14:30)")

def confirmer_action(message):
    """
    Demande une confirmation à l'utilisateur.
    """
    reponse = input(f"{message} (o/n) : ").strip().lower()
    return reponse == 'o' or reponse == 'oui'