import time
import datetime
import logging
import threading


class TakingsNotifier(object):
    thread = None

    test_takings = [{
        'time': datetime.datetime.now().timestamp(),
        'user_id': '111',
        'message': 'message NOW',
        'is_notified': False
    },
    {
        'time': (datetime.datetime.now() + datetime.timedelta(seconds=3)).timestamp(),
        'user_id': '111',
        'message': 'message + 3 minute',
        'is_notified': False
    }]

    def __init__(self):
        print("__init__")
        logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s')
        self.logger = logging.getLogger('scheduler')
        self.logger.setLevel(logging.INFO)

    def start(self):
        print("start")
        self.thread = threading.Thread(target=self.run_check)
        self.thread.start()

    def run_check(self):
        print("run_check")
        while 1:
            self.check()
            time.sleep(1)

    def check(self):
        self.logger.info('Performing scheduled tasks check.')
        now = datetime.datetime.now().timestamp()
        for taking in self.test_takings:
            if taking['time'] < now and taking['is_notified'] == False:
                self.logger.info('Taking notification user_id=%s message="%s"' % (taking['user_id'], taking['message']))
                taking['is_notified'] = True


print(__name__)
if __name__ == "__main__":
    TakingsNotifier().start()