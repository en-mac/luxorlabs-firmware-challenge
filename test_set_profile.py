import requests
from config import Config

def test_set_profile(miner_ip, profile):
    url = f"http://localhost:8000/set_profile/{miner_ip}/{profile}"
    response = requests.post(url)
    if response.status_code == 200:
        print(f"Successfully set profile for {miner_ip} to {profile}")
    else:
        print(f"Failed to set profile for {miner_ip} to {profile}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    config = Config()
    miners = config.miners
    profiles = ["overclock", "normal", "underclock"]

    for miner in miners:
        for profile in profiles:
            test_set_profile(miner, profile)
