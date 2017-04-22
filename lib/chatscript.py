import socket


class Message(object):

    def __init__(self, user_id, bot_name, message):
        self.data = bytes('%s\0%s\0%s\0' % (user_id, bot_name, message), 'utf-8')

    def send(self, sock, buffer_size=1024):
        if not self.data:
            raise ValueError('Invalid message data.')
        sock.send(self.data)
        response = sock.recv(buffer_size)
        return response.decode("utf-8")


class ChatScript(object):

    def __init__(self, host='localhost', port=1024):
        self.host = host
        self.port = port

    def is_alive(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, self.port))
            chat_message = Message('', '1', '')
            chat_message.send()
        except ConnectionRefusedError as e:
            return False
        return True

    def send_message(self, user_id, bot_name, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        chat_message = Message(user_id, bot_name, message)
        return chat_message.send(sock)
