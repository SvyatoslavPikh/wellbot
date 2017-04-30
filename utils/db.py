from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

import datetime
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
        db_type = settings.DB_TYPE
        db_login = settings.DB_LOGIN
        db_password = settings.DB_PASSWORD
        db_address = settings.DB_ADDRESS
        db_name = settings.DB_NAME
        db_connection_str = '%s://%s:%s@%s/%s' % (db_type, db_login, db_password, db_address, db_name)
        print('db_connection_str %s' % db_connection_str)

        self.engine = create_engine(db_connection_str, echo=True)
        # Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        if not self.engine:
            raise Exception('Engine not defined. You need to init db connection with init_db() method first.')
        if not self.session:
            self.session = sessionmaker(bind=self.engine)()
        return self.session

    def test(self, chat_id, user_name):
        # '333551684'
        session = self.get_session();
        first_user = session.query(User).filter_by(chat_id=chat_id).scalar()
        if not first_user:
            first_user = User(name=user_name, chat_id=chat_id, age=25, weight=65.5)
            session.add(first_user)
        print('first_user %s' % first_user)

        test_menu = session.query(Menu).filter_by(name='Test').scalar()
        if not test_menu:
            test_menu = Menu(name='Test', user=first_user)
            session.add(test_menu)
        else:
            session.query(Taking).filter_by(menu=test_menu).delete()
        print('test_menu %s' % test_menu)

        taking_1 = Taking(menu=test_menu, datetime=datetime.datetime.now() + datetime.timedelta(minutes=1), message='1 minute passed')
        taking_5 = Taking(menu=test_menu, datetime=datetime.datetime.now() + datetime.timedelta(minutes=5), message='5 minute passed')
        taking_10 = Taking(menu=test_menu, datetime=datetime.datetime.now() + datetime.timedelta(minutes=10), message='10 minute passed')
        taking_60 = Taking(menu=test_menu, datetime=datetime.datetime.now() + datetime.timedelta(hours=1), message='60 minute passed')
        test_menu.takings.extend([taking_1, taking_5, taking_10, taking_60])

        session.commit()
        return test_menu