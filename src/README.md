# Projet de Gestion d'une Clinique en Python

## Description du Projet

Application console de gestion d'une clinique permettant de gérer les patients, les rendez-vous et les utilisateurs (médecins et secrétaires). Le projet utilise PostgreSQL comme base de données relationnelle.

## Objectifs Pédagogiques

- Organisation modulaire du code
- Gestion des erreurs et exceptions
- Validation des saisies utilisateur
- Utilisation d'une base de données PostgreSQL
- Implémentation de rôles utilisateurs (médecins/secrétaires)
- Menu interactif

##  Structure du Projet

```
projet-clinique-python-2025-AwaBodian/
│
├── src/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration de la connexion PostgreSQL
│   │   └── init_db.py         # Création des tables et données de test
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── patient.py         # Gestion des patients (CRUD)
│   │   ├── rendez_vous.py     # Gestion des rendez-vous
│   │   └── utilisateur.py     # Authentification et utilisateurs
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── validation.py      # Fonctions de validation des saisies
│   │
│   └── main.py                # Point d'entrée de l'application
│
├── README.md                  # Ce fichier
└── requirements.txt           # Dépendances Python
```

##  Prérequis

- **Python 3.8+**
- **PostgreSQL 12+**
- **pip** (gestionnaire de paquets Python)

### 2. Installer PostgreSQL
### 3. Créer la base de données
Ouvrez pgAdmin ou psql et exécutez :
```sql
CREATE DATABASE clinique_db;
```

### 4. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

### 5. Configurer la connexion
Modifiez `src/database/config.py` :
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'clinique_db',
    'user': 'postgres',
    'password': 'VOTRE_MOT_DE_PASSE',  # Changez ici
    'port': '5432'
}
```

### 6. Initialiser la base de données
```bash
cd src
python database/init_db.py
```

Cela va créer les tables et insérer 2 utilisateurs de test :
- **Médecin** : `dr.diop@clinique.sn` / `medecin123`
- **Secrétaire** : `secretaire@clinique.sn` / `secretaire123`

## Lancement de l'Application

```bash
cd src
python main.py
```
### Pour les Secrétaires
- Ajouter un patient
- Rechercher un patient
- Modifier les informations d'un patient
- Créer des rendez-vous
- Voir tous les rendez-vous
- Annuler un rendez-vous
- Lister tous les patients

### Pour les Médecins
- Voir leurs rendez-vous
-  Consulter un patient (avec historique)
-  Marquer un rendez-vous comme terminé
-  Rechercher un patient
- Voir tous les patients

## Base de Données

### Tables

**utilisateurs**
- `id` : Identifiant unique
- `nom`, `prenom` : Nom complet
- `email` : Email unique (pour connexion)
- `mot_de_passe` : Mot de passe
- `role` : 'medecin' ou 'secretaire'
- `specialite` : Spécialité médicale (pour médecins)
- `telephone` : Numéro de téléphone

**patients**
- `id` : Identifiant unique
- `nom`, `prenom` : Nom complet
- `date_naissance` : Date de naissance
- `sexe` : M, F, ou Autre
- `telephone` : Numéro de téléphone
- `adresse`, `email` : Coordonnées
- `numero_securite_sociale` : NSS

**rendez_vous**
- `id` : Identifiant unique
- `patient_id` : Référence au patient
- `medecin_id` : Référence au médecin
- `date_rdv`, `heure_rdv` : Date et heure
- `motif` : Raison de la consultation
- `statut` : 'planifie', 'termine', ou 'annule'
- `notes` : Notes du médecin


### Module psycopg2 introuvable
```bash
pip install psycopg2-binary
```

### Les tables ne se créent pas
```bash
cd src
python database/init_db.py
```