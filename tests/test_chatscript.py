import unittest
from lib.chatscript import ChatScript


class FirstConversationCase(unittest.TestCase):
    def test_is_alive_request(self):
        chat_script = ChatScript()
        self.assertTrue(chat_script.is_alive())

    def test_is_alive_request(self):
        chat_script = ChatScript()
        answer = chat_script.send_message('111', 'HARRY', 'test')
        self.assertEqual(answer, "I don't know what to say.")


if __name__ == '__main__':
    unittest.main()
