API_KEY = ''

<<<<<<< HEAD
DB_TYPE = ''
DB_LOGIN = ''
DB_PASSWORD = ''
DB_ADDRESS = ''
DB_NAME = ''
=======
DB_TYPE = 'postgresql'
DB_LOGIN = 'wellbot'
DB_PASSWORD = 'wellbot'
DB_ADDRESS = '127.0.0.1:5432'
DB_NAME = 'wellbot'
>>>>>>> 86ddc368e5d06b1b2dd0b9d514ee17851cbd9d59

try:
    from local_settings import *
except ImportError:
    pass

