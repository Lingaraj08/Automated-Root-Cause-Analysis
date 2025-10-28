# Simple Flask app that consumes Kafka 'alerts' and shows a tiny dashboard
from flask import Flask, jsonify, render_template_string
from kafka import KafkaConsumer
import threading, json, os, time

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "kafka:9092")

app = Flask(__name__)

events = []

def consumer_thread():
    consumer = KafkaConsumer('alerts',
                             bootstrap_servers=[KAFKA_BOOTSTRAP],
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                             auto_offset_reset='earliest',
                             consumer_timeout_ms=1000)
    print("RCA consumer started, listening to 'alerts'...")
    while True:
        try:
            for msg in consumer:
                ev = msg.value
                ev['_received_at'] = int(time.time())
                print("Received event:", ev)
                events.insert(0, ev)
                # keep last 50 events
                if len(events) > 50:
                    events.pop()
            time.sleep(1)
        except Exception as e:
            print("Consumer error:", e)
            time.sleep(2)

@app.route('/api/events')
def api_events():
    return jsonify(events)

@app.route('/')
def index():
    html = """<!doctype html>
    <html><head><title>RCA Dashboard</title></head><body>
    <h1>Automated RCA - mock dashboard</h1>
    <p>Recent alerts (most recent first):</p>
    <div id="events"></div>
    <script>
    async function load() {
        const resp = await fetch('/api/events');
        const data = await resp.json();
        const el = document.getElementById('events');
        if (!data.length) { el.innerHTML = '<i>No events yet</i>'; return; }
        el.innerHTML = '<ul>' + data.map(d => `<li><b>${d.host}</b> / ${d.service} — ${d.state} — ${d.output} <small>(${new Date(d.timestamp*1000).toLocaleString()})</small></li>`).join('') + '</ul>';
    }
    setInterval(load, 3000);
    load();
    </script>
    </body></html>"""
    return render_template_string(html)

if __name__ == '__main__':
    t = threading.Thread(target=consumer_thread, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000)
