import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram.ext import Job
from lib.chatscript import ChatScript

class ApiServer(object):

    def __init__(self):
        pass

    def start(self, context):
        t = threading.Thread(target=self.run_server, args=[context])
        t.start()

    def run_server(self, context):
        print('API started.')

        server_address = ('', 1300)
        httpd = HTTPServer(server_address, RestApiHandler)
        httpd.server_context = context
        httpd.serve_forever()


class RestApiHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.updater = server.server_context
        self.logger = self.updater.logger
        self.job_queue = self.updater.job_queue
        super(RestApiHandler, self).__init__(request, client_address, server)


    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()

    def do_GET(self):
        try:
            job = Job(self.alarm, 30, repeat=False, context=(333551684, "Hey!"))
            self.job_queue.put(job)
        except Exception as e:
            self.logger.error('[%s] %s' % (333551684, repr(e)))
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()
        self.wfile.write(bytes("OK.\n", 'utf-8'))

        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        # self.wfile.write(bytes("You accessed path: %s" % self.path, 'utf-8'))

    def alarm(self, bot, job):
        chat_id = job.context[0]
        message = job.context[1]
        self.logger.info('[%s] Checking alarm.' % chat_id)

        chat_script = ChatScript()
        answer = chat_script.send_message(chat_id, 'HARRY', message)
        bot.sendMessage(chat_id, message)