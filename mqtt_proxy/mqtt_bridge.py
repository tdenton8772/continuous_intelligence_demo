import boto3
import paho.mqtt.client as mqtt
import json
import time
import os

MQTT_BROKER = "mqtt_broker"
MQTT_TOPIC = "factory/machines"
KINESIS_STREAM_NAME = "RTU_Machine_Data"
AWS_PROFILE = os.getenv("AWS_PROFILE", "default")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Initialize Kinesis client using AWS profile
session = boto3.Session(profile_name=AWS_PROFILE)
kinesis_client = session.client("kinesis", region_name=AWS_REGION)

def send_to_kinesis(data):
    """Sends MQTT data to Kinesis."""
    try:
        kinesis_client.put_record(
            StreamName=KINESIS_STREAM_NAME,
            Data=json.dumps(data),
            PartitionKey=data.get("machine_id", "default")
        )
        print(f"Published to Kinesis: {data}")
    except Exception as e:
        print(f"Error sending to Kinesis: {e}")

# MQTT message handler
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        send_to_kinesis(data)
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

# MQTT Client Setup
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883)
client.subscribe(MQTT_TOPIC)
client.on_message = on_message

print("MQTT to Kinesis bridge is running...")
client.loop_forever()