from flask import Flask, jsonify, request
from miner_controller import MinerController
from config import Config
from scheduler import Scheduler
import threading

app = Flask(__name__)
config = Config()
miner_controller = MinerController(config.api_url)
current_state = {}

# Endpoint to get the current configuration of all miners
@app.route('/miner_configuration', methods=['GET'])
def get_miner_configuration():
    return jsonify(current_state)

# Endpoint to get the configuration of a specific miner
@app.route('/miner_configuration/<miner_ip>', methods=['GET'])
def get_miner_configuration_for_miner(miner_ip):
    if miner_ip in current_state:
        return jsonify({miner_ip: current_state[miner_ip]})
    else:
        return jsonify({"error": "No configuration found for miner IP"}), 404

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(miner_controller.logs)

# Endpoint to get the logs of a specific miner
@app.route('/logs/<miner_ip>', methods=['GET'])
def get_logs_for_miner(miner_ip):
    if miner_ip in miner_controller.logs:
        return jsonify({miner_ip: miner_controller.logs[miner_ip]})
    else:
        return jsonify({"error": "No logs found for miner IP"}), 404

@app.route('/set_profile/<miner_ip>/<profile>', methods=['POST'])
def set_profile(miner_ip, profile):
    try:
        miner_controller.login(miner_ip)
        miner_controller.set_profile(miner_ip, profile)
        current_state[miner_ip]["profile"] = profile
        return jsonify({"message": f"Profile of miner {miner_ip} set to {profile}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/set_state/<miner_ip>/<state>', methods=['POST'])
def set_state(miner_ip, state):
    try:
        miner_controller.login(miner_ip)
        miner_controller.curtail(miner_ip, state)
        current_state[miner_ip]["state"] = state
        return jsonify({"message": f"State of miner {miner_ip} set to {state}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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
