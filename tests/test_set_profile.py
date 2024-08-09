import unittest
import requests
from config import Config

class TestSetProfile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = Config()
        cls.miners = cls.config.miners
        cls.profiles = ["overclock", "normal", "underclock"]

    def test_set_profile(self):
        for miner in self.miners:
            for profile in self.profiles:
                with self.subTest(miner=miner, profile=profile):
                    url = f"http://localhost:8000/set_profile/{miner}/{profile}"
                    response = requests.post(url)
                    self.assertEqual(response.status_code, 200, f"Failed to set profile for {miner} to {profile}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    unittest.main()
