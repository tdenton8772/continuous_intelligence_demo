from flask import Blueprint, request, jsonify
import threading
import time
import random
from application.mqtt.simulator import publish_machine_data, publish_anomaly
from os import getenv
import requests

mod = Blueprint('api', __name__, url_prefix='/api')

# Machine states
machines = {
    "RTU_1": False,
    "RTU_2": False,
    "RTU_3": False
}

PINOT_BROKER = getenv("PINOT_BROKER")
PINOT_API_KEY = getenv("PINOT_API_KEY")
PINOT_QUERY_URL = f"{PINOT_BROKER}/query/sql"

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

@mod.route('/rtu_measurements/<machine_id>', methods=['GET'])
def get_rtu_measurements(machine_id):
    """Fetches the latest measurements for each RTU from Pinot"""
    query = f"""
    select LASTWITHTIME(compressor_current, event_time, 'DOUBLE') compressor_current,
            LASTWITHTIME(fan_speed, event_time, 'DOUBLE') fan_speed,
            LASTWITHTIME(pressure, event_time, 'DOUBLE') pressure,
            LASTWITHTIME(temperature, event_time, 'DOUBLE') temperature
    from aws_demo
    where machine_id = '{machine_id}'
    """
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {PINOT_API_KEY}"
    }
    response = requests.post(PINOT_QUERY_URL, json={"sql": query}, headers=headers)

    if response.status_code == 200:
        raw_data = response.json()
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
    
    resultsTable = raw_data['resultTable']
    column_names = resultsTable.get("dataSchema", {}).get("columnNames", [])
    rows = resultsTable.get("rows", [])

    if not rows:
        return jsonify({"error": "No data found"})

    structured_data = {column_names[i]: rows[0][i] for i in range(len(column_names))}

    return jsonify(structured_data)

@mod.route('/machine_status/<machine_id>', methods=['GET'])
def get_machine_status(machine_id):
    """Returns whether a machine is running or not."""
    if machine_id not in machines:
        return jsonify({"error": "Machine not found"}), 404
    return jsonify({"machine_id": machine_id, "status": "Running" if machines[machine_id] else "Idle"})
