import paho.mqtt.client as mqtt
import boto3
import time
import json
import random
from os import getenv

MQTT_BROKER = "mqtt_broker"
MQTT_PORT = 1883
MQTT_TOPIC = "factory/machines"
KINESIS_STREAM_NAME = "RTU_Machine_Data"

# Initialize MQTT client
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Initialize Kinesis client
session = boto3.Session(profile_name='default')
kinesis_client = session.client("kinesis", region_name="us-east-1")

# Initial conditions for sensors
machine_sensors = {
    "RTU_1": {"temperature": 75.0, "compressor_current": 10.0, "fan_speed": 1200, "pressure": 50.0},
    "RTU_2": {"temperature": 76.0, "compressor_current": 9.5, "fan_speed": 1250, "pressure": 48.5},
    "MAU_1": {"temperature": 72.0, "compressor_current": 10.2, "fan_speed": 1300, "pressure": 49.0}
}

def update_sensor_values(machine_id):
    """Generates sensor data following realistic patterns."""
    if machine_id not in machine_sensors:
        return None
    
    sensors = machine_sensors[machine_id]
    
    # Temperature: changes slowly over time
    sensors["temperature"] += random.uniform(-0.5, 0.5)
    sensors["temperature"] = max(65, min(85, sensors["temperature"]))  # Keep within range
    
    # Compressor Current: fluctuates slightly but stays stable
    sensors["compressor_current"] += random.uniform(-0.2, 0.2)
    sensors["compressor_current"] = max(8.0, min(12.0, sensors["compressor_current"]))
    
    # Fan Speed: small gradual changes
    sensors["fan_speed"] += random.randint(-50, 50)
    sensors["fan_speed"] = max(1000, min(1500, sensors["fan_speed"]))
    
    # Pressure: fluctuates within a set range
    sensors["pressure"] += random.uniform(-1.0, 1.0)
    sensors["pressure"] = max(45, min(55, sensors["pressure"]))
    
    return sensors

def publish_machine_data(machine_id):
    """Publishes simulated machine data to MQTT and Kinesis."""
    sensor_data = update_sensor_values(machine_id)
    if not sensor_data:
        return
    
    data = {
        "machine_id": machine_id,
        "temperature": round(sensor_data["temperature"], 2),
        "compressor_current": round(sensor_data["compressor_current"], 2),
        "fan_speed": sensor_data["fan_speed"],
        "pressure": round(sensor_data["pressure"], 2),
        "status": "running",
        "event_time": int(round(time.time() * 1000))
    }
    payload = json.dumps(data)
    client.publish(MQTT_TOPIC, payload)
    print(f"[MQTT PUBLISHED] {payload}")
    
    # Publish to Kinesis
    kinesis_client.put_record(
        StreamName=KINESIS_STREAM_NAME,
        Data=payload,
        PartitionKey=machine_id
    )
    print(f"[KINESIS PUBLISHED] {payload}")

def publish_anomaly(machine_id):
    """Publishes an anomaly event to MQTT and Kinesis."""
    anomaly_data = {
        "machine_id": machine_id,
        "temperature": round(random.uniform(95.0, 120.0), 2),  # High temp anomaly
        "compressor_current": round(random.uniform(15.0, 25.0), 2),  # Overloaded compressor
        "fan_speed": random.randint(500, 2000),  # Erratic fan speed
        "pressure": round(random.uniform(30.0, 70.0), 2),  # Out-of-range pressure
        "event_time": int(round(time.time() * 1000)),
        "status": "anomaly_detected"
    }
    payload = json.dumps(anomaly_data)
    client.publish(MQTT_TOPIC, payload)
    print(f"[MQTT ANOMALY] {payload}")
    
    # Publish to Kinesis
    kinesis_client.put_record(
        StreamName=KINESIS_STREAM_NAME,
        Data=payload,
        PartitionKey=machine_id
    )
    print(f"[KINESIS ANOMALY] {payload}")
