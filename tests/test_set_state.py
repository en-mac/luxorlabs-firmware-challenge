import unittest
import requests
from config import Config

class TestSetState(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = Config()
        cls.miners = cls.config.miners
        cls.states = ["active", "sleep"]

    def test_set_state(self):
        for miner in self.miners:
            for state in self.states:
                with self.subTest(miner=miner, state=state):
                    url = f"http://localhost:8000/set_state/{miner}/{state}"
                    response = requests.post(url)
                    self.assertEqual(response.status_code, 200, f"Failed to set state for {miner} to {state}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    unittest.main()
