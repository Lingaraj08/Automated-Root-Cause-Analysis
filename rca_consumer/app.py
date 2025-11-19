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
    <html>
    <head>
        <title>RCA Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                background: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 30px;
            }
            .header h1 {
                color: #2a5298;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .header p {
                color: #666;
                font-size: 1.1em;
            }
            .stats {
                display: flex;
                gap: 20px;
                margin-top: 20px;
                flex-wrap: wrap;
            }
            .stat-box {
                flex: 1;
                min-width: 200px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .stat-box.critical { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
            .stat-box.warning { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
            .stat-box.info { background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); }
            .stat-number {
                font-size: 2.5em;
                font-weight: bold;
            }
            .stat-label {
                font-size: 0.9em;
                opacity: 0.9;
                margin-top: 5px;
            }
            .events-section {
                background: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .events-section h2 {
                color: #2a5298;
                margin-bottom: 20px;
                font-size: 1.8em;
                border-bottom: 3px solid #2a5298;
                padding-bottom: 10px;
            }
            .event-list {
                display: flex;
                flex-direction: column;
                gap: 15px;
                max-height: 600px;
                overflow-y: auto;
                padding-right: 10px;
            }
            .event-card {
                background: #f8f9fa;
                border-left: 5px solid #667eea;
                padding: 20px;
                border-radius: 8px;
                transition: all 0.3s ease;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            .event-card:hover {
                transform: translateX(5px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .event-card.critical { border-left-color: #f5576c; background: #ffebee; }
            .event-card.warning { border-left-color: #ffa500; background: #fff3e0; }
            .event-card.ok { border-left-color: #4caf50; background: #e8f5e9; }
            .event-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
                flex-wrap: wrap;
                gap: 10px;
            }
            .event-host {
                font-size: 1.3em;
                font-weight: bold;
                color: #2a5298;
            }
            .event-service {
                color: #666;
                font-size: 1em;
            }
            .event-state {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 0.85em;
            }
            .event-state.critical { background: #f5576c; color: white; }
            .event-state.warning { background: #ffa500; color: white; }
            .event-state.ok { background: #4caf50; color: white; }
            .event-state.unknown { background: #9e9e9e; color: white; }
            .event-output {
                color: #555;
                margin: 10px 0;
                font-size: 0.95em;
                line-height: 1.5;
            }
            .event-time {
                font-size: 0.85em;
                color: #999;
                margin-top: 8px;
            }
            .no-events {
                text-align: center;
                padding: 40px;
                color: #999;
                font-size: 1.1em;
            }
            .refresh-indicator {
                text-align: center;
                color: #999;
                font-size: 0.85em;
                margin-top: 15px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚨 Automated RCA Dashboard</h1>
                <p>Real-time monitoring and root cause analysis system</p>
                <div class="stats">
                    <div class="stat-box critical">
                        <div class="stat-number" id="critical-count">0</div>
                        <div class="stat-label">Critical</div>
                    </div>
                    <div class="stat-box warning">
                        <div class="stat-number" id="warning-count">0</div>
                        <div class="stat-label">Warnings</div>
                    </div>
                    <div class="stat-box info">
                        <div class="stat-number" id="total-count">0</div>
                        <div class="stat-label">Total Events</div>
                    </div>
                </div>
            </div>
            <div class="events-section">
                <h2>📋 Recent Alerts</h2>
                <div id="events" class="event-list"></div>
                <div class="refresh-indicator">Auto-refreshing every 3 seconds...</div>
            </div>
        </div>
        <script>
        async function load() {
            const resp = await fetch('/api/events');
            const data = await resp.json();
            const el = document.getElementById('events');
            
            // Update stats
            document.getElementById('total-count').textContent = data.length;
            const criticalCount = data.filter(d => d.state && d.state.toLowerCase() === 'critical').length;
            const warningCount = data.filter(d => d.state && d.state.toLowerCase() === 'warning').length;
            document.getElementById('critical-count').textContent = criticalCount;
            document.getElementById('warning-count').textContent = warningCount;
            
            if (!data.length) {
                el.innerHTML = '<div class="no-events">⏳ No events yet. Waiting for alerts...</div>';
                return;
            }
            
            el.innerHTML = data.map(d => {
                const state = (d.state || 'unknown').toLowerCase();
                const time = new Date(d.timestamp * 1000).toLocaleString();
                return `
                    <div class="event-card ${state}">
                        <div class="event-header">
                            <div>
                                <div class="event-host">🖥️ ${d.host}</div>
                                <div class="event-service">${d.service}</div>
                            </div>
                            <span class="event-state ${state}">${state.toUpperCase()}</span>
                        </div>
                        <div class="event-output">📝 ${d.output}</div>
                        <div class="event-time">⏰ ${time}</div>
                    </div>
                `;
            }).join('');
        }
        
        setInterval(load, 3000);
        load();
        </script>
    </body>
    </html>"""
    return render_template_string(html)

if __name__ == '__main__':
    t = threading.Thread(target=consumer_thread, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000)
