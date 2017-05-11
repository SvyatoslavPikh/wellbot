import cgi
import urllib
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram.ext import Job
from lib.chatscript import ChatScript


def start(context):
    t = threading.Thread(target=_run_server, args=[context])
    t.start()


def _run_server(context):
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
        self.routes_GET = {
            '/push': self.push_message
        }
        self.routes_POST = {
            '/push': self.push_message
        }

        super(RestApiHandler, self).__init__(request, client_address, server)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()

    def do_GET(self):
        path = self._get_clear_path()

        if path in self.routes_GET:
            i = self.path.find('?')
            if i >= 0:
                args = urllib.parse.parse_qs(self.path[i + 1:])

            self.routes_GET[path](args or {})
        else:
            self.send_response(404)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes("404 Not found.", "utf-8"))

    def do_POST(self):
        path = self._get_clear_path()

        if path in self.routes_POST:
            args = {}
            i = self.path.find('?')
            if i >= 0:
                args = urllib.parse.parse_qs(self.path[i + 1:])
                print('line_args:' + repr(args))

            post_args = {}
            if self.headers['content-type']:
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                if ctype == 'multipart/form-data':
                    post_args = cgi.parse_multipart(self.rfile, pdict)
                elif ctype == 'application/x-www-form-urlencoded':
                    length = int(self.headers['content-length'])
                    post_args = urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=1)
                else:
                    post_args = {}
            for key in post_args:
                args[key.decode("utf-8")] = list(map(lambda x: x.decode("utf-8"), post_args[key]))

            self.routes_POST[path](args)
        else:
            self.send_response(404)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes("404 Not found.", "utf-8"))

    # r = requests.post('http://localhost:1300/push', data={'chat_id': '333551684', 'message':'Hey!','delay':'10'})
    def push_message(self, args):
        if 'chat_id' not in args:
            self.send_response(400)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes("'chat_id' not provided in arguments.", 'utf-8'))
            return

        if 'message' not in args:
            self.send_response(400)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes("'message' not provided in arguments.", 'utf-8'))
            return

        try:
            chat_id = self._get_arg(args['chat_id'])  # 333551684
            message = self._get_arg(args['message'])
            delay = 0
            if 'delay' in args:
                delay = int(self._get_arg(args['delay']))

            job = Job(self._alarm, delay, repeat=False, context=(chat_id, message))
            self.job_queue.put(job)
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes("OK.", 'utf-8'))
        except Exception as e:
            self.logger.error('[%s] %s' % (chat_id, repr(e)))
            self.send_response(500)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes("500 Internal server error.", 'utf-8'))

    def _alarm(self, bot, job):
        chat_id = job.context[0]
        message = job.context[1]

        chat_script = ChatScript()
        answer = chat_script.send_message(chat_id, 'HARRY', message)
        bot.sendMessage(chat_id, answer)

    def _get_clear_path(self):
        path = self.path.split('?')[0]
        return path if path[-1] != '/' else path[:-1]

    def _get_arg(self, list):
        return list[0] if len(list) == 1 else ', '.join(list)
