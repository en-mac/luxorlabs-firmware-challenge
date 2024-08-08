import requests
from collections import defaultdict
from datetime import datetime
from utils import get_current_time_period

class MinerController:
    def __init__(self, api_url):
        self.api_url = api_url
        self.tokens = {}
        self.miner_profiles = {}
        self.miner_states = {}
        self.logs = defaultdict(list)

    def login(self, miner_ip):
        response = requests.post(f"{self.api_url}/login", json={"miner_ip": miner_ip})
        response.raise_for_status()
        token = response.json().get("token")
        if token:
            self.tokens[miner_ip] = token
            print(f"Login successful for {miner_ip}, token: {token}")
            return token
        else:
            raise ValueError("Failed to obtain token")

    def logout(self, miner_ip):
        response = requests.post(f"{self.api_url}/logout", json={"miner_ip": miner_ip})
        response.raise_for_status()
        return response.json()

    def set_profile(self, miner_ip, profile):
        if self.miner_profiles.get(miner_ip) == profile:
            print(f"Miner {miner_ip} is already in the desired profile: {profile}")
            return
        token = self.tokens.get(miner_ip)
        if not token:
            token = self.login(miner_ip)
        payload = {"token": token, "profile": profile}
        print(f"Sending profileset payload for {miner_ip}: {payload}")
        response = requests.post(f"{self.api_url}/profileset", json=payload)
        response.raise_for_status()
        self.miner_profiles[miner_ip] = profile
        return response.json()

    def curtail(self, miner_ip, mode):
        if self.miner_states.get(miner_ip) == mode:
            print(f"Miner {miner_ip} is already in the desired mode: {mode}")
            return
        token = self.tokens.get(miner_ip)
        if not token:
            token = self.login(miner_ip)
        payload = {"token": token, "mode": mode}
        print(f"Sending curtail payload for {miner_ip}: {payload}")
        response = requests.post(f"{self.api_url}/curtail", json=payload)
        if response.status_code == 401:
            print(f"Token expired for {miner_ip}, re-authenticating...")
            self.login(miner_ip)  # Re-authenticate
            payload["token"] = self.tokens[miner_ip]
            response = requests.post(f"{self.api_url}/curtail", json=payload)
        response.raise_for_status()
        self.miner_states[miner_ip] = mode
        return response.json()


    def update_miner_mode(self, miner_ip):
        period = get_current_time_period()
        if period == 'overclock':
            profile = 'overclock'
            self.set_profile(miner_ip, profile)
            state = 'active'
        elif period == 'normal':
            profile = 'normal'
            self.set_profile(miner_ip, profile)
            state = 'active'
        elif period == 'underclock':
            profile = 'underclock'
            self.set_profile(miner_ip, profile)
            state = 'active'
        elif period == 'curtail':
            profile = 'sleep'
            self.curtail(miner_ip, profile)
            state = 'asleep'
        
        timestamp = datetime.now().isoformat()  # Get the current timestamp
        print(f"Miner {miner_ip} updated to {profile} with state {state} at {timestamp}")
        self.logs[miner_ip].append((timestamp, profile, state))
        return profile, state
        return profile, state

    def get_logs(self, miner_ip):
        return self.logs[miner_ip]
