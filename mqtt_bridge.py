from kafka import KafkaProducer
import paho.mqtt.client as mqtt
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    producer.send('mqtt_data', value=data)
    print(f"Published to Kafka: {data}")

client = mqtt.Client()
client.connect("localhost", 1883)
client.subscribe("factory/machines")
client.on_message = on_message
client.loop_forever()
