#   For better modularity these constants can be imported in various scripts inside the app
#   Constant for defaut name of the two databases :
DEFAULT_DB_USER_NAME = 'user.db'
DEFAULT_DB_PASSWORD_NAME = 'password.db'

#   -----------------   UserModel Constants     -----------------

# defaults constant of minimum limits (reasonable ones) for at least security with the hash
# Also default and minimum/maximum limits for security
DEFAULT_TIME_COST = 3
MIN_TIME_COST = 1
MAX_TIME_COST = 10  # Maximum time cost

DEFAULT_MEMORY_COST = 65536  # 64 MB
MIN_MEMORY_COST = 8192  # 8 MB
MAX_MEMORY_COST = 1048576  # 1 GB (in KiB)

DEFAULT_PARALLELISM = 4
MIN_PARALLELISM = 1
MAX_PARALLELISM = 8  # Max parallelism, use reasonable limits based on CPU cores

DEFAULT_HASH_LEN = 32
MIN_HASH_LEN = 16
MAX_HASH_LEN = 64  # Max length of the hash

DEFAULT_SALT_LEN = 16
MIN_SALT_LEN = 8
MAX_SALT_LEN = 32  # Max length of the salt

#   -----------------   GeneratorModel Constants     -----------------

DEFAULT_PASSWORD_LENGTH = 16
MAX_PASSWORD_LENGTH = 128
MIN_PASSWORD_LENGTH = 8
MAX_ENTROPY = 91 #  Sum of all character pools