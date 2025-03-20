# Continuous Intelligence Demo

This repository demonstrates Apache Pinot's capabilities in handling IoT data ingestion, performing real-time anomaly detection, functioning as a vector store, and providing recommendations for restoring proper functioning of IoT devices in real-time.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Running the Application](#running-the-application)
- [Components](#components)
  - [MQTT Bridge](#mqtt-bridge)
  - [Anomaly Detection](#anomaly-detection)
  - [Vector Data](#vector-data)

## Overview

The Continuous Intelligence Demo showcases a system where simulated Roof Top Unit (RTU) data is ingested, processed, and analyzed in real-time to detect anomalies and provide actionable recommendations. Apache Pinot serves as the central data store, enabling efficient querying and analysis of large-scale time-series data.

![Flow Chart](./continuous_intelligence_demo.png)

## Repository Structure

- `anomaly_detection/`: Contains scripts and configurations for detecting anomalies in RTU data.
- `control_panel/`: Hosts the web-based interface for monitoring and interacting with the system.
- `mqtt_proxy/`: Implements the MQTT bridge for ingesting MQTT data into the system.
- `pinot_config/`: Includes configurations for setting up Apache Pinot.
- `vector_data/`: Manages vector embeddings and similarity search functionalities.
- `docker-compose.yml`: Defines the Docker services for orchestrating the application components.
- `README.md`: This file.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.8+](https://www.python.org/downloads/)

### Environment Variables

Before running the application, set the following environment variables:

- `AWS_PROFILE`: AWS profile name for authentication.
- `AWS_DEFAULT_REGION`: AWS region for services.
- `PINOT_API_KEY`: API key for accessing Apache Pinot.
- `PINOT_CONTROLLER`: URL of the Pinot controller.
- `PINOT_BROKER`: URL of the Pinot broker.

These variables can be set in your shell or within a `.env` file.

### Running the Application

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/tdenton8772/continuous_intelligence_demo.git
   cd continuous_intelligence_demo
   ```

2. **Set Environment Variables:**

Ensure all required environment variables are set as described above.

3. **Start the Application Using Docker Compose:**

```bash
docker-compose up --build
```

This command will build and start all services defined in the docker-compose.yml file, including the MQTT bridge, anomaly detection service, control panel, and Apache Pinot.

## Components
### MQTT Bridge
The MQTT bridge simulates RTU data and publishes it to an MQTT broker. This data is then ingested into Apache Pinot for real-time analysis.

### Anomaly Detection
The anomaly detection component runs predefined queries against the ingested data to identify anomalies in RTU performance metrics. Detected anomalies trigger alerts and recommendations for corrective actions.

### Vector Data
The vector data component manages vector embeddings of troubleshooting information. It enables similarity searches to provide relevant recommendations based on the current state and detected anomalies of the RTUs.
