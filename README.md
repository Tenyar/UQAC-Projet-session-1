# UQAC-Projet-session-1
Gestionnaire de mots de passe

## Tables de la base de données
User(#username(UNIQUE), #full_hashed_password)

PasswordData(#username, algorithm, version, memorycost, timecost, parallelism, salt, hash_len, salt_len, split_hashed_password)

UserData(#username, service_name, password)
