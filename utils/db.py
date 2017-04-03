from sqlalchemy import create_engine
import settings
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class DbManager(object):

    def __init__(self, *args, **kwargs):
        self.engine = create_engine('postgresql://wellbot:wellbot@127.0.0.1:5432/wellbot', echo=True)

    # connection = engine.connect()
