from flask import Blueprint, request, jsonify
import threading
import time
import random
from application.mqtt.simulator import publish_machine_data, publish_anomaly

mod = Blueprint('api', __name__, url_prefix='/api')

# Machine states
machines = {
    "RTU_1": False,
    "RTU_2": False,
    "MAU_1": False
}

def simulate_machine(machine_id):
    """Simulates machine activity and publishes MQTT data."""
    while machines[machine_id]:
        publish_machine_data(machine_id)
        time.sleep(0.1)

@mod.route('/start/<machine_id>', methods=['POST'])
def start_machine(machine_id):
    if machine_id in machines and not machines[machine_id]:
        machines[machine_id] = True
        threading.Thread(target=simulate_machine, args=(machine_id,), daemon=True).start()
        return jsonify({"message": f"{machine_id} started"})
    return jsonify({"error": "Machine already running or invalid machine"}), 400

@mod.route('/stop/<machine_id>', methods=['POST'])
def stop_machine(machine_id):
    if machine_id in machines and machines[machine_id]:
        machines[machine_id] = False
        return jsonify({"message": f"{machine_id} stopped"})
    return jsonify({"error": "Machine not running or invalid machine"}), 400

@mod.route('/anomaly/<machine_id>', methods=['POST'])
def insert_anomaly(machine_id):
    if machine_id in machines:
        publish_anomaly(machine_id)
        return jsonify({"message": f"Anomaly inserted for {machine_id}"})
    return jsonify({"error": "Invalid machine"}), 400
