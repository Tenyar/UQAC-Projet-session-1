# UQAC-Projet-session-1
Gestionnaire de mots de passe

## Tables de la base de données
User(#username(UNIQUE), #master_password)
MasterPassword(#master_password(hashed), timecost, memorycost, parallelism, salt)
Passwords(#username, site/app (name), password(hashed), {Url du site?, description du site?})

## Packages requirements
Pour ce gestionnaire de mot de passe, il faut avoir ces packages d'installés :
pip install cryptography
pip install argon2-cffi
