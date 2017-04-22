from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging
import settings
from models.base import Base
from models.models import *

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class Db(object):
    def __init__(self):
        self.session = None
        self.engine = None
        pass

    def init_db(self):
        db_type = settings.DB_TYPE
        db_login = settings.DB_LOGIN
        db_password = settings.DB_PASSWORD
        db_address = settings.DB_ADDRESS
        db_name = settings.DB_NAME
        db_connection_str = '%s://%s:%s@%s/%s' % (db_type, db_login, db_password, db_address, db_name)

        self.engine = create_engine(db_connection_str, echo=True)
        Base.metadata.create_all(self.engine)

    def get_session(self):
        if not self.engine:
            raise Exception('Engine not defined. You need to init db connection with init_db() method first.')
        if not self.session:
            self.session = sessionmaker(bind=self.engine)
        return self.session


    def test(self):
        session = self.get_session();
        first_user = User(name='slava', chat_id='333551684', age=25, weight=65.5)
        session.add(first_user)
        session.commit()
