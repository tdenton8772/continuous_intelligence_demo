import paho.mqtt.client as mqtt
import time
import random
import json

MQTT_BROKER = "localhost"  # Update with actual broker if needed
MQTT_PORT = 1883
MQTT_TOPIC = "factory/machines"

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

def publish_machine_data(machine_id):
    """Publishes simulated machine data to MQTT."""
    data = {
        "machine_id": machine_id,
        "temperature": round(random.uniform(20.0, 100.0), 2),
        "status": "running"
    }
    payload = json.dumps(data)
    client.publish(MQTT_TOPIC, payload)
    print(f"[MQTT PUBLISHED] {payload}")

def publish_anomaly(machine_id):
    """Publishes an anomaly event to MQTT."""
    anomaly_data = {
        "machine_id": machine_id,
        "temperature": round(random.uniform(150.0, 300.0), 2),  # Extreme temp
        "status": "anomaly_detected"
    }
    payload = json.dumps(anomaly_data)
    client.publish(MQTT_TOPIC, payload)
    print(f"[MQTT ANOMALY] {payload}")
