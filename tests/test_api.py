import unittest
import requests


class PushTestCase(unittest.TestCase):
    def test_full_request(self):
        r = requests.post('http://localhost:1300/push', data={'chat_id': '111', 'message': 'Hey!', 'delay': '0'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(len(r.text) != 0)

    def test_no_args_request(self):
        r = requests.post('http://localhost:1300/push')
        self.assertEqual(r.status_code, 400)
        self.assertTrue(len(r.text) != 0)

    def test_no_chat_id_request(self):
        r = requests.post('http://localhost:1300/push', data={'message': 'Hey!', 'delay': '0'})
        self.assertEqual(r.status_code, 400)
        self.assertTrue(len(r.text) != 0)

    def test_no_message_request(self):
        r = requests.post('http://localhost:1300/push', data={'chat_id': '111', 'delay': '0'})
        self.assertEqual(r.status_code, 400)
        self.assertTrue(len(r.text) != 0)

    def test_no_delay_request(self):
        r = requests.post('http://localhost:1300/push', data={'chat_id': '111', 'message': 'Hey!'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(len(r.text) != 0)

    def test_args_in_url_request(self):
        r = requests.post('http://localhost:1300/push', params={'chat_id': '111', 'message': 'Hey!', 'delay': '0'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(len(r.text) != 0)

if __name__ == '__main__':
    unittest.main()
