import requests
from config import Config

def test_set_state(miner_ip, state):
    url = f"http://localhost:8000/set_state/{miner_ip}/{state}"
    response = requests.post(url)
    if response.status_code == 200:
        print(f"Successfully set state for {miner_ip} to {state}")
    else:
        print(f"Failed to set state for {miner_ip} to {state}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    config = Config()
    miners = config.miners
    states = ["active", "sleep"]

    for miner in miners:
        for state in states:
            test_set_state(miner, state)
