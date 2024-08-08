from flask import Flask, jsonify
from miner_controller import MinerController
from config import Config
from scheduler import Scheduler
import threading

app = Flask(__name__)
config = Config()
miner_controller = MinerController(config.api_url)
current_state = {}

# Endpoint to get the current state of miners
@app.route('/state', methods=['GET'])
def get_state():
    return jsonify(current_state)

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(miner_controller.logs)

def start_scheduler():   
    # Log in miners and set initial state
    for miner_ip in config.miners:
        try:
            miner_controller.login(miner_ip)
            current_state[miner_ip] = {
                "token": miner_controller.tokens[miner_ip],
                "profile": None,  # Initial profile state is None
                "state": None     # Initial state is None
            }
        except Exception as e:
            print(f"Failed to login miner {miner_ip}: {e}")
    
    scheduler = Scheduler(miner_controller, config.miners, current_state)
    scheduler.start()

if __name__ == '__main__':
    # Run the scheduler in a separate daemon thread
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Run the Flask app
    app.run(port=8000)
    
