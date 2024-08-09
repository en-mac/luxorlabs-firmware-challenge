import unittest
import json
from web_server import app

class TestWebServer(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_miner_configuration(self):
        response = self.app.get('/miner_configuration')
        self.assertEqual(response.status_code, 200)

    def test_get_miner_configuration_for_miner(self):
        response = self.app.get('/miner_configuration/192.168.1.1')
        if response.status_code != 404:
            self.assertEqual(response.status_code, 200)

    def test_get_logs(self):
        response = self.app.get('/logs')
        self.assertEqual(response.status_code, 200)

    def test_get_logs_for_miner(self):
        response = self.app.get('/logs/192.168.1.1')
        if response.status_code != 404:
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
