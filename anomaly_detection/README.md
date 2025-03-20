# Anomaly Detection Module

This module is part of the Continuous Intelligence Demo project, focusing on detecting anomalies in data streams from IoT Devices. It leverages Apache Pinot for real-time data ingestion and querying to identify deviations from expected operational parameters.

## Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Configuration](#configuration)
  - [Query Definitions](#query-definitions)
- [How it Works](#configuration)
  - [Fetching from Apache Pinot](#fetching-from-apache-pinot)
  - [Generating Alert Using Amazon Bedrock](#generating-alert-using-amazon-bedrock)
  - [Sending Alerts](#sending-alerts)
  - [Summary](#summary)

## Overview

Anomaly Detection is a critical component of the Continuous Intelligence Demo that enables real-time anomaly detection. It continuously monitors incoming data, detects anomalies, and generates actionable insights using Apache Pinot for querying and Amazon Bedrock for generating recommendations.

## Directory Structure

```
anomaly_detection/ 
  ├── detection.py 
  ├── queries.json
  ├── README.md
  └── requirements.txt
```

- `detection.py`: The python script that runs on a configured frequecy to issue queries defined in queries.json
- `queries.json`: The parameterized queries for detection.py to run
- `requirements.txt`: the python libraries needed for this script

## Configuration

### Query Definitions

The queries.json file contains the SQL queries used to detect anomalies. Each query is defined with the following structure:

```json
{
  "queries": [
    {
      "name": "Compressor Current Anomaly",
      "sql": "SELECT * FROM rtu_data WHERE machine_id = '%machine_id%' and compressor_current < %limit%",
      "parameters": {"machine_id": ["machine_1"], "limit": [10]},
      "narrative": "A description used in anomaly detection for vector lookup",
    }
  ]
}
```

- name: A descriptive name for the anomaly detection query.​
- sql: The SQL query to execute against the Pinot database. Use ? as a placeholder for the threshold value.​
- parameters: The value to replace the placeholder in the SQL query.​
- narrative: A brief explanation of what the query detects.

## How it works

***Fetching from Apache Pinot:***

The process begins with the script querying Apache Pinot, which stores real-time telemetry data.

- The script loads a set of predefined anomaly detection queries from queries.json.
- Each query is designed to detect specific conditions.
- It iterates over a list of RTUs and executes queries against Apache Pinot to pull the most recent data for each machine.

***Generating Alert Using Amazon Bedrock***

Instead of just sending raw anomaly data, the script leverages Amazon Bedrock to generate a human-readable alert message with troubleshooting recommendations.

It constructs a prompt containing:

- The anomaly details detected.
- The historical context of the RTU.
- Troubleshooting knowledge stored in the vector database.

It then sends this information to Amazon Bedrock, where an AI model (Claude 3.7) analyzes the situation and generates a detailed alert with actionable recommendations.

If multiple anomalies are detected, they are stored together in the file.
The Flask web application reads from this file to display alerts in the UI.

***Sending Alerts***

The script notifies the front-end web application about new alerts by making a POST request to the Flask API.

This allows the UI to dynamically update and display alerts in real-time, ensuring that technicians and operators are instantly informed of system issues.

***Summary***

- Queries Apache Pinot to fetch real-time RTU telemetry data.
- Checks for anomalies by comparing against predefined thresholds.
- Generates human-readable alerts using Amazon Bedrock AI.
- Stores alerts in alerts.json for persistent tracking.
- Pushes alerts to the web UI for real-time display.

By automating real-time anomaly detection, detection.py enables proactive monitoring of RTUs, helping to prevent equipment failure and optimize system performance.







