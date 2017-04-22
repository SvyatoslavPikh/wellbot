API_KEY = ''

DB_TYPE = 'postgresql'
DB_LOGIN = 'login'
DB_PASSWORD = 'password'
DB_ADDRESS = '127.0.0.1:5432'
DB_NAME = 'wellbot'

try:
    from local_settings import *
except ImportError:
    pass
