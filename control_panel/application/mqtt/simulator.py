import paho.mqtt.client as mqtt
import time
import json
import random

MQTT_BROKER = "mqtt_broker"
MQTT_PORT = 1883
MQTT_TOPIC = "factory/machines"

# Initialize MQTT client
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Initial conditions for sensors
machine_sensors = {
    "RTU_1": {"temperature": 75.0, "compressor_current": 10.0, "fan_speed": 1200, "pressure": 50.0},
    "RTU_2": {"temperature": 76.0, "compressor_current": 9.5, "fan_speed": 1250, "pressure": 48.5},
    "RTU_3": {"temperature": 72.0, "compressor_current": 10.2, "fan_speed": 1300, "pressure": 49.0}
}

def update_sensor_values(machine_id):
    """Generates sensor data following realistic patterns."""
    if machine_id not in machine_sensors:
        return None
    
    sensors = machine_sensors[machine_id]
    
    # Temperature: changes slowly over time
    sensors["temperature"] += random.uniform(-0.2, 0.2)
    sensors["temperature"] = max(65, min(85, sensors["temperature"]))  # Keep within range
    
    # Compressor Current: fluctuates slightly but stays stable
    sensors["compressor_current"] += random.uniform(-0.2, 0.2)
    sensors["compressor_current"] = max(8.0, min(12.0, sensors["compressor_current"]))
    
    # Fan Speed: small gradual changes
    sensors["fan_speed"] += random.randint(-10, 10)
    sensors["fan_speed"] = max(1000, min(1500, sensors["fan_speed"]))
    
    # Pressure: fluctuates within a set range
    sensors["pressure"] += random.uniform(-0.2, 0.2)
    sensors["pressure"] = max(45, min(55, sensors["pressure"]))
    
    return sensors

def publish_machine_data(machine_id):
    """Publishes simulated machine data to MQTT."""
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

def publish_anomaly(machine_id):
    """Publishes an anomaly event to MQTT."""
    
    measurement_type = ['temperature', 'compressor_current', 'fan_speed', 'pressure']
    measurement = random.choice(measurement_type)

    sensor_data = update_sensor_values(machine_id)
    if not sensor_data:
        print(f"Error: No sensor data available for {machine_id}")
        return

    anomaly_data = {
        "machine_id": machine_id,
        **{key: round(value, 2) if isinstance(value, float) else value for key, value in sensor_data.items()},
        "status": "Anomaly",
        "event_time": int(round(time.time() * 1000))
    }

    # Inject anomaly into the chosen measurement type
    small_anomaly_ranges = {
        "temperature": lambda: round(random.uniform(95.0, 120.0), 2),
        "compressor_current": lambda: round(random.uniform(15.0, 25.0), 2),
        "fan_speed": lambda: random.randint(500, 2000),
        "pressure": lambda: round(random.uniform(30.0, 70.0), 2)
    }

    large_anomaly_ranges = {
        "temperature": lambda: round(random.uniform(95.0, 120.0), 2),
        "compressor_current": lambda: round(random.uniform(15.0, 25.0), 2),
        "fan_speed": lambda: random.randint(500, 2000),
        "pressure": lambda: round(random.uniform(30.0, 70.0), 2)
    }

    anomaly_type = ["small", "large"]
    selected_type = random.choice(anomaly_type)

    if selected_type == "small":
        anomaly_data[measurement] = small_anomaly_ranges[measurement]()
    else:
        anomaly_data[measurement] = large_anomaly_ranges[measurement]()

    payload = json.dumps(anomaly_data)
    client.publish(MQTT_TOPIC, payload)
    print(f"[MQTT ANOMALY] {payload}")
