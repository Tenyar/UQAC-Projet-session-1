# UQAC-Projet-session-1
Gestionnaire de mots de passe sécurisé avec interface GUI et CLI — Hachage Argon2id + Chiffrement des données

## Technologies utilisées
Python 3.x
CustomTKinter (GUI)
Argon2id (hachage master password)
Cryptography (chiffrement des données)
SQLite/MySQL (persistance)

## Fonctionnalités principales
- Génération de mots de passe aléatoires avec analyse d'entropie
- Hachage sécurisé du master password (Argon2id)
- Chiffrement des mots de passe stockés
- Interface GUI avec CustomTKinter
- Interface CLI alternative
- Persistance en fichier

## Tables de la base de données
- User(#username(UNIQUE), #master_password)
- MasterPassword(#master_password(hashed), timecost, memorycost, parallelism, salt)
- Passwords(#username, site/app (name), password(hashed), {Url du site?, description du site?})

## Installation & Lancement

Pour ce gestionnaire de mot de passe, il faut avoir ces packages d'installés :

```bash
pip install cryptography
pip install argon2-cffi
```

Ensuite il faut lancé l'application depuis la racine du projet :

```bash
cd \UQAC-Projet-session-1
python controller/MainController.py
```
