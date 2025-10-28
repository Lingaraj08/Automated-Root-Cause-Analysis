# Simple Nagios simulator that sends mock alerts to Kafka topic 'alerts'
import json
import time
import socket
from kafka import KafkaProducer
import os

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "kafka:9092")
producer = KafkaProducer(bootstrap_servers=[KAFKA_BOOTSTRAP],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

alerts = [
    {"host": "web-01", "service": "HTTP", "state": "CRITICAL", "output": "HTTP 500", "timestamp": int(time.time())},
    {"host": "db-01", "service": "MySQL", "state": "WARNING", "output": "Slow query", "timestamp": int(time.time())},
    {"host": "router-01", "service": "SNMP", "state": "CRITICAL", "output": "Interface down", "timestamp": int(time.time())},
]

def main():
    i = 0
    print("Nagios simulator started. Sending alerts to topic 'alerts' every 8 seconds.")
    while True:
        alert = alerts[i % len(alerts)].copy()
        alert['timestamp'] = int(time.time())
        alert['id'] = f"alert-{int(time.time())}"
        print("Sending alert:", alert)
        producer.send('alerts', alert)
        producer.flush()
        i += 1
        time.sleep(8)

if __name__ == '__main__':
    main()
