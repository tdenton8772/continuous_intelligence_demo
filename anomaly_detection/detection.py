import json
import requests
import os
import boto3
from langchain.embeddings import BedrockEmbeddings

PINOT_BROKER = os.getenv("PINOT_BROKER")
PINOT_API_KEY = os.getenv("PINOT_API_KEY")
PINOT_QUERY_URL = f"{PINOT_BROKER}/query/sql" 

session = boto3.Session(profile_name="default")
bedrock_client = session.client(service_name='bedrock-runtime', 
                              region_name='us-east-1')
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",
                                       client=bedrock_client)

def main():
    try:
        alerts = []
        with open("./queries.json", 'r') as f:
            raw_data = f.read()
        data = json.loads(raw_data)
        for record in data:
            query_template = record['sql']
            parameters = record.get("parameters", {})
            narrative = record["narrative"]
            name = record["name"]

            parameter_keys = parameters.keys()
            param_combinations = [{}]  # Start with an empty combination

            for key in parameter_keys:
                new_combinations = []
                for param_value in parameters[key]:
                    for existing_combination in param_combinations:
                        new_combination = existing_combination.copy()
                        new_combination[key] = param_value
                        new_combinations.append(new_combination)
                param_combinations = new_combinations

            # Execute each generated query
            for param_set in param_combinations:
                query_sql = query_template
                for key, value in param_set.items():
                    query_sql = query_sql.replace(f"%{key}%", value)

                headers = {
                    "Content-Type": "application/json",
                    "authorization": f"Bearer {PINOT_API_KEY}" 
                }
                response = requests.post(PINOT_QUERY_URL, json={"sql": query_sql, "queryOptions": "useMultistageEngine=true"}, headers=headers)

                if response.status_code == 200:
                    raw_response = response.json()
                    resultsTable = raw_response['resultTable']
                    column_names = resultsTable.get("dataSchema", {}).get("columnNames", [])
                    rows = resultsTable.get("rows", [])
                    if len(rows) > 0:
                        alerts.append("{narrative}: {value}")
                else:
                    json.dumps({"error": "Failed to fetch data"}), response.status_code
        if len(alerts) > 0:
            text = " ".join(alerts)
            response = bedrock_embeddings.embed_query(text)
            print(response)
    except Exception as e:
        print("Execution Error:", str(e))
        return {"statusCode": 500, "body": str(e)}

if __name__ == "__main__":
    main()