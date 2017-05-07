API_KEY = ''

DB_TYPE = 'postgresql'
DB_LOGIN = 'wellbot'
DB_PASSWORD = 'wellbot'
DB_ADDRESS = '127.0.0.1:5432'
DB_NAME = 'wellbot'

try:
    from local_settings import *
except ImportError:
    pass
