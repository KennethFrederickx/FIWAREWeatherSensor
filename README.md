# IoT Data Processing and Visualization Platform

## Overview
This project sets up an IoT data processing and visualization platform using Docker containers. It includes components for data ingestion, storage, processing, and visualization. The platform utilizes FIWARE components such as Orion-LD for context management, QuantumLeap for time-series data storage, and Grafana for visualization. Additionally, it includes a Python script for subscribing to MQTT messages, processing them, and updating context data in Orion-LD.

## Components
- **Orion-LD:** Context broker for managing context data in NGSI-LD format.
- **QuantumLeap:** Stores time-series data received from Orion-LD.
- **Grafana:** Dashboard visualization tool for analyzing data stored in QuantumLeap.
- **MongoDB:** Database for storing non-time-series data.
- **CrateDB:** Distributed SQL database for storing large volumes of time-series data efficiently.
- **Python Script:** Subscribes to MQTT messages, processes them, and updates context data in Orion-LD.

## Installation Guide
Make sure you have sensor connected and ino script running (Important: Update SSID and WiFiPassword).

Details ino script:
- Board: TTGO T1
- 115200 baud
- Port: COM7

1. Start Docker containers:
    ```
    docker-compose up -d
    ```

2. Change directory to `src`:
    ```
    cd src
    ```

3. Run the Python script:
    ```
    python.exe script.py
    ```

4. Setting up Grafana:
   - Open Grafana in your web browser [localhost:3000](http://localhost:3000).
   - Add a new PostgreSQL data source:
     - Name: CrateDB
     - Host: crate-db:5432 (Important: Do not put localhost)
     - Database: doc
     - User: crate
     - Password: leave it empty
     - SSL mode: disable
   - Import the json file called "GrafanaTemperatureReadings.json" into Grafana
    
   - For more detailed instructions, refer to [this tutorial](https://cratedb.com/blog/visualizing-time-series-data-with-grafana-and-cratedb).

## Dependencies
- Docker Engine
- Docker Compose
- Python (for the Python script)
