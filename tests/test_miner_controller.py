import unittest
from unittest.mock import patch
from miner_controller import MinerController

class TestMinerController(unittest.TestCase):

    def setUp(self):
        self.api_url = "http://localhost:5000/api"
        self.miner_controller = MinerController(self.api_url)

    @patch('requests.post')
    def test_login(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'token': 'test_token'}
        token = self.miner_controller.login("192.168.1.1")
        self.assertEqual(token, 'test_token')

    @patch('requests.post')
    def test_set_profile(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'message': 'Profile set successfully'}
        self.miner_controller.tokens["192.168.1.1"] = 'test_token'
        response = self.miner_controller.set_profile("192.168.1.1", "overclock")
        self.assertEqual(response['message'], 'Profile set successfully')

    @patch('requests.post')
    def test_curtail(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'message': 'Curtail state set successfully'}
        self.miner_controller.tokens["192.168.1.1"] = 'test_token'
        response = self.miner_controller.curtail("192.168.1.1", "sleep")
        self.assertEqual(response['message'], 'Curtail state set successfully')

if __name__ == '__main__':
    unittest.main()
