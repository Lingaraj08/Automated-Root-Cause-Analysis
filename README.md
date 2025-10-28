# Automated Root Cause Analysis - Prototype

This repository is a minimal prototype for the "Automated Root Cause Analysis Platform".
It contains:
- a Kafka (bitnami) broker + Zookeeper.
- a **nagios_simulator** service that publishes mock alerts to Kafka.
- a **rca_consumer** Flask app that consumes alerts from Kafka and shows a tiny dashboard.

## Files & folders
- docker-compose.yml
- nagios_simulator/
  - Dockerfile
  - producer.py
  - requirements.txt
- rca_consumer/
  - Dockerfile
  - app.py
  - requirements.txt

## How to unzip the provided zip (in Ubuntu)
1. Open Terminal (Ctrl+Alt+T).
2. Move to the directory where you downloaded the zip. For example, if it's in `~/Downloads`:
   ```
   cd ~/Downloads
   ```
3. Unzip to a folder (example will create `~/rca_project`):
   ```
   unzip rca_project.zip -d ~/rca_project
   ```
4. The project will be available at `~/rca_project/rca_project` (note double path because the zip contains the project root).
   To move it to `~/rca_project`:
   ```
   mv ~/rca_project/rca_project/* ~/rca_project/
   rmdir ~/rca_project/rca_project
   ```

## Run the project using Docker Compose
1. Open VS Code.
2. Click `File` -> `Open Folder...` and choose `~/rca_project` (or wherever you unzipped).
3. In VS Code, open a new terminal: `Terminal` -> `New Terminal`.
4. From the terminal run:
   ```
   docker compose up --build
   ```
   (or `docker-compose up --build` if your docker-compose command is the older one).
5. Wait until services start. You should see logs from zookeeper, kafka, nagios_simulator and rca_consumer.
6. Open a browser and visit: `http://localhost:5000` to see the dashboard of received alerts.

## What to choose in VS Code (GUI guidance)
- After opening the project folder:
  - If prompted to "Install recommended extensions", you can install Python and Docker extensions.
  - Use the bottom-left corner to select the interpreter: click the Python version in the status bar and pick a Python 3 interpreter (system or a virtual env). This only matters if you run Python locally — our services run in Docker.
  - To run Docker Compose from the Docker extension: open the "Docker" panel (left activity bar) -> "Compose" -> right-click `docker-compose.yml` -> `Compose Up`.

## Useful Docker commands (if VS Code GUI not preferred)
- Build & start in background:
  ```
  docker compose up --build -d
  ```
- See container logs:
  ```
  docker compose logs -f
  ```
- Stop and remove:
  ```
  docker compose down
  ```

## Notes
- This is a small prototype using mock alerts; it demonstrates integration between a "monitoring" simulator, Kafka, and a consumer that provides a dashboard.
- For production-grade Nagios/Kafka/SNMP integration you'd replace the simulator with actual Nagios event scripts and add persistent storage, authentication and monitoring.
