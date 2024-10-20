# UQAC-Projet-session-1
Gestionnaire de mots de passe

## Tables de la base de données
User(#username(UNIQUE), #master_password)
MasterPassword(#master_password(hashed), timecost, memorycost, parallelism, salt)
Passwords(#username, site/app (name), password(hashed), {Url du site?, description du site?})
