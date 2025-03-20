# Vector Data Module

This module is part of the Continuous Intelligence Demo project, focusing on managing vector data to enhance the system's ability to understand and process complex information. It leverages vector databases to efficiently store and retrieve high-dimensional data representations, facilitating advanced similarity searches and recommendations.​

## Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Configuration](#configuration)
   - [Schema Definition](#schema-definitions)
   - [Table Configuration](#table-configuration)
- [Usage](#usage) 
- [Generating Vectors](#generating-vector)
- [Creating Test Queries](#creating-test-queries)

## Overview

The Vector Data module is designed to handle high-dimensional vector data, enabling efficient similarity searches and data retrieval. By converting complex data types into vector representations, the system can perform advanced analyses that traditional databases may not efficiently handle. This capability is crucial for applications like recommendation systems, anomaly detection, and more.

## Directory Structure

```
vector_data/
│
├── data/
│   └── ...
├── create_test_query.py
├── create_vectors.py
├── requirements.txt
├── schema.json
├── table.json
└── ttahtf_lookinside.pdf
```

- data/: Contains data files used for vector generation and testing.​
- create_test_query.py: Script to create test queries for the vector database.​
- create_vectors.py: Script to generate vector embeddings from raw data.​
- requirements.txt: Lists the Python dependencies required for the scripts.​
- schema.json: Defines the schema for the vector data.​
- table.json: Configuration file for setting up the vector database table.​
- ttahtf_lookinside.pdf: A sample PDF document included for testing purposes.

## Configuration

### Schema Definition 
The schema.json file outlines the structure of the data to be stored in the vector database. It specifies the fields, data types, and any indexing required for efficient querying. Proper schema definition ensures that the database can handle the vector data effectively.​

### Table Configuration

The table.json file contains the configuration settings for the vector database table. This includes parameters like table name, storage settings, and indexing options. Configuring the table correctly is essential for optimal performance and accurate query results. This is wherr the vector index is defined.

## Usage

### Generating Vectors

To convert raw data into vector embeddings:​

- Install Dependencies: Ensure all required Python packages are installed.​

```bash
pip install -r requirements.txt
```

- Prepare Data: Place the raw data files into the data/ directory.​

- Run Vector Generation Script: Execute the create_vectors.py script to generate vector embeddings.​

```bash
python create_vectors.py
```

This script will process the raw data and produce vector embeddings into json files for storage in s3 and ingestion into Apache Pinot.​

### Creating Test Queries
To create and execute test queries against the vector database:​

- Ensure Vector Data is Available: Confirm that vector embeddings have been generated and stored in the database.​
- Run Test Query Script: Use the create_test_query.py script to formulate and execute test queries.​

```bash
python create_test_query.py
```

This script will perform similarity searches or other vector-based queries to validate the functionality of the vector database.​

