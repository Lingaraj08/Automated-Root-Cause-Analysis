# Automated Root Cause Analysis (RCA) Platform

A real-time automated root cause analysis system that monitors infrastructure alerts, processes them through Apache Kafka, and displays them on an interactive web dashboard.

## 📋 Overview

The **Automated Root Cause Analysis Platform** is a prototype system designed to:
- **Capture** infrastructure and application alerts from monitoring systems
- **Process** alerts in real-time using Apache Kafka message streaming
- **Visualize** critical incidents on a modern, responsive web dashboard
- **Track** alert trends and historical data for RCA investigations

### Architecture

```
┌─────────────────────┐
│ Nagios Simulator    │  → Generates mock monitoring alerts
│ (Alert Producer)    │
└──────────┬──────────┘
           │
           ↓ (Kafka Topic: 'alerts')
┌─────────────────────┐
│  Apache Kafka       │  → Distributed message broker
│  + Zookeeper        │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│ RCA Consumer        │  → Flask web app with dashboard
│ (Alert Consumer)    │
└─────────────────────┘
           │
           ↓
    http://localhost:5000
```

## 🏗️ Project Structure

```
Automated-Root-Cause-Analysis/
├── docker-compose.yml          # Docker Compose configuration for all services
├── README.md                   # This file
├── nagios_simulator/           # Alert producer service
│   ├── Dockerfile              # Container image definition
│   ├── producer.py             # Generates mock Nagios alerts
│   └── requirements.txt         # Python dependencies
└── rca_consumer/               # Flask dashboard consumer
    ├── Dockerfile              # Container image definition
    ├── app.py                  # Flask web app with dashboard UI
    └── requirements.txt         # Python dependencies
```

## 🔧 System Components

### 1. **Apache Kafka & Zookeeper**
- **Role**: Message broker for alert streaming
- **Images**: `confluentinc/cp-kafka:7.4.1`, `confluentinc/cp-zookeeper:7.4.1`
- **Ports**: Kafka (9092), Zookeeper (2181)
- **Why**: Enables scalable, decoupled communication between alert sources and consumers

### 2. **Nagios Simulator** (`nagios_simulator/`)
- **Purpose**: Simulates Nagios/Icinga alert sources
- **Function**: Generates mock infrastructure alerts (CPU, memory, network, HTTP status)
- **Output**: Publishes alerts to Kafka topic `alerts` in JSON format
- **Alert Fields**:
  - `host`: Server/host name
  - `service`: Service name (e.g., HTTP, SNMP, Disk)
  - `state`: Alert severity (CRITICAL, WARNING, OK)
  - `output`: Alert message/description
  - `timestamp`: Unix timestamp

### 3. **RCA Consumer** (`rca_consumer/`)
- **Purpose**: Real-time alert dashboard and visualization
- **Framework**: Flask (Python web framework)
- **Function**: 
  - Consumes alerts from Kafka in real-time
  - Maintains event history (last 50 events)
  - Serves a responsive web UI
- **Port**: 5000

## 📊 Dashboard Features

### Live Statistics
- **Critical Events**: Count of critical-level alerts
- **Warning Events**: Count of warning-level alerts
- **Total Events**: Cumulative event count

### Alert Cards
Each alert is displayed with:
- **Host & Service**: Equipment/service name
- **Status Badge**: Color-coded severity (Critical, Warning, OK)
- **Alert Message**: Description of the issue
- **Timestamp**: When the alert was received

### Visual Indicators
- 🚨 Critical alerts (red) — immediate attention required
- 🟠 Warning alerts (orange) — investigate soon
- 🟢 OK alerts (green) — issue resolved
- Auto-refresh every 3 seconds

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** installed on your system
  - Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop)
  - macOS: [Docker Desktop](https://www.docker.com/products/docker-desktop)
  - Linux: `sudo apt-get install docker.io docker-compose` (Ubuntu/Debian)
- **Git** (optional, for cloning the repo)
- **Web Browser** (Chrome, Firefox, Safari, Edge)

### Installation & Setup (Windows/PowerShell)

1. **Clone or download the repository**
   ```powershell
   git clone https://github.com/Lingaraj08/Automated-Root-Cause-Analysis.git
   cd Automated-Root-Cause-Analysis
   ```

2. **Build and start all services**
   ```powershell
   docker compose up --build -d
   ```
   This will:
   - Build the `nagios_simulator` and `rca_consumer` Docker images
   - Pull pre-built Kafka and Zookeeper images
   - Start all 4 services in detached mode (background)

3. **Wait for services to be ready** (typically 20-30 seconds)
   ```powershell
   docker compose ps
   ```
   You should see all services with status "Up":
   ```
   NAME                                    IMAGE                           STATUS
   automated-root-cause-analysis-kafka-1   confluentinc/cp-kafka:7.4.1    Up X seconds
   automated-root-cause-analysis-rca_consumer-1   ...rca_consumer:latest   Up X seconds
   automated-root-cause-analysis-zookeeper-1  confluentinc/cp-zookeeper:7.4.1  Up X seconds
   automated-root-cause-analysis-nagios_simulator-1   ...nagios_simulator:latest  Up X seconds
   ```

4. **Open the dashboard**
   - Open your browser and navigate to: **http://localhost:5000**
   - You should see the RCA Dashboard with live alerts

### Installation & Setup (macOS/Linux)

```bash
# Clone the repository
git clone https://github.com/Lingaraj08/Automated-Root-Cause-Analysis.git
cd Automated-Root-Cause-Analysis

# Start services
docker compose up --build -d

# Verify all services are running
docker compose ps

# Open dashboard
open http://localhost:5000  # macOS
# or
xdg-open http://localhost:5000  # Linux
```

## 📸 Screenshots

### Dashboard Home
The main dashboard displays:
- Header with project title and description
- Statistics cards showing alert counts (Critical, Warnings, Total)
- Real-time alert list with color-coded severity badges
- Auto-refreshing interface

**Current State:**
- Critical Events: 34
- Warning Events: 16
- Total Events: 50

### Alert Card Example
Each alert shows:
```
🖥️ web-01 (Hostname)
   HTTP (Service)
   📝 HTTP 500 (Issue description)
   ⏰ 19/11/2025, 11:26:44 (Timestamp)
   [CRITICAL] (Status badge)
```

## 🛠️ Common Commands

### View logs
```powershell
# All services
docker compose logs -f

# Specific service
docker compose logs -f rca_consumer
docker compose logs -f nagios_simulator
docker compose logs -f kafka
```

### Restart services
```powershell
# Restart all
docker compose restart

# Restart specific service
docker compose restart rca_consumer
```

### Stop services
```powershell
# Stop but keep data
docker compose stop

# Stop and remove (clean)
docker compose down
```

### Rebuild after code changes
```powershell
docker compose up --build
```

### Check container status
```powershell
docker compose ps
```

## 🔍 Troubleshooting

### Dashboard shows "No events yet"
- **Cause**: Producer hasn't generated alerts yet
- **Solution**: Wait 5-10 seconds, refresh the page (F5)
- **Check producer logs**: `docker compose logs nagios_simulator`

### Connection refused on localhost:5000
- **Cause**: Flask app not running or not fully started
- **Solution**: 
  ```powershell
  docker compose logs rca_consumer
  ```
  Wait for message: `"Running on http://0.0.0.0:5000"`

### Kafka connection errors
- **Cause**: Kafka/Zookeeper services not healthy
- **Solution**:
  ```powershell
  docker compose restart kafka zookeeper
  docker compose logs kafka
  ```

### All services exited unexpectedly
- **Cause**: Port conflicts or insufficient resources
- **Solution**:
  ```powershell
  docker compose down
  docker compose up --build
  ```

## 📝 API Endpoints

### Consumer Service (`rca_consumer`)

#### GET `/`
- **Returns**: HTML dashboard page
- **Port**: 5000

#### GET `/api/events`
- **Returns**: JSON array of recent alerts
- **Example**:
  ```json
  [
    {
      "host": "web-01",
      "service": "HTTP",
      "state": "CRITICAL",
      "output": "HTTP 500",
      "timestamp": 1700000000,
      "_received_at": 1700000005
    },
    ...
  ]
  ```

## 🔌 Kafka Topic Structure

### Topic: `alerts`
- **Message Format**: JSON
- **Schema**:
  ```json
  {
    "host": "string",          // Server hostname
    "service": "string",       // Service name
    "state": "string",         // CRITICAL | WARNING | OK
    "output": "string",        // Alert message
    "timestamp": "integer"     // Unix timestamp
  }
  ```

## 🎓 How It Works

1. **Producer (Nagios Simulator)**
   - Generates random mock alerts every 1-5 seconds
   - Alerts represent different severity levels and services
   - Publishes to Kafka `alerts` topic

2. **Kafka Broker**
   - Receives alerts from producer
   - Buffers and persists messages
   - Delivers to all connected consumers

3. **Consumer (Flask App)**
   - Subscribes to `alerts` Kafka topic
   - Runs background thread to listen for new messages
   - Maintains list of recent events (max 50)
   - Serves live dashboard via web interface

4. **Dashboard UI**
   - Fetches events from `/api/events` endpoint every 3 seconds
   - Renders alerts with appropriate styling
   - Updates statistics in real-time
   - Displays most recent alerts first

## 🚢 Deployment Notes

### For Production Use
- Replace mock Nagios simulator with real Nagios/Icinga integrations
- Add persistent storage (PostgreSQL, MongoDB) for long-term alert history
- Implement authentication and authorization
- Add SSL/TLS for secure communication
- Deploy using Kubernetes or cloud-native platforms
- Add monitoring and alerting for the platform itself
- Implement role-based access control (RBAC)
- Add data retention policies and archival

### Performance Considerations
- Current design handles ~50 events in memory
- For high-volume environments (1000+ alerts/sec), add:
  - Time-series database (InfluxDB, Prometheus)
  - Caching layer (Redis)
  - Horizontal scaling with multiple consumer instances
  - Alert aggregation and deduplication

## 📚 Technologies Used

- **Apache Kafka** v7.4.1 - Message streaming
- **Apache Zookeeper** v7.4.1 - Distributed coordination
- **Python** 3.11 - Application language
- **Flask** - Web framework
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 📄 License

This project is provided as-is for educational and prototype purposes.

## 🤝 Contributing

To enhance this project:
1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

## 📞 Support

For issues or questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review Docker logs: `docker compose logs`
- Verify all containers are running: `docker compose ps`

---

**Last Updated**: November 2025 | **Status**: Active Development
