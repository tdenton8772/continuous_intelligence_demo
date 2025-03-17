from kafka import KafkaProducer
import paho.mqtt.client as mqtt
import json
import time

KAFKA_BROKER = "kafka:9092"
MQTT_BROKER = "mqtt_broker"
MQTT_TOPIC = "factory/machines"
KAFKA_TOPIC = "mqtt_data"

# Retry logic for Kafka connection
def create_kafka_producer():
    while True:
        try:
            print("Attempting to connect to Kafka...")
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print("Connected to Kafka successfully!")
            return producer
        except Exception as e:
            print(f"Kafka connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# Initialize Kafka producer with retries
producer = create_kafka_producer()

# MQTT message handler
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        producer.send(KAFKA_TOPIC, value=data)
        print(f"Published to Kafka: {data}")
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

# MQTT Client Setup
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883)
client.subscribe(MQTT_TOPIC)
client.on_message = on_message

print("MQTT to Kafka bridge is running...")
client.loop_forever()
