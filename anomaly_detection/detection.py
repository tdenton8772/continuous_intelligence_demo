import json
import requests
import os
import boto3
from langchain_aws.embeddings import BedrockEmbeddings

PINOT_BROKER = os.getenv("PINOT_BROKER")
PINOT_API_KEY = os.getenv("PINOT_API_KEY")
PINOT_QUERY_URL = f"{PINOT_BROKER}/query/sql" 

session = boto3.Session(profile_name="default")
bedrock_client = session.client(service_name='bedrock-runtime', 
                              region_name='us-east-1')
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0",
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
                        alerts.append(f"{narrative}: {value}")
                else:
                    json.dumps({"error": "Failed to fetch data"}), response.status_code
        if len(alerts) > 0:
            text = " ".join(alerts)
            response = bedrock_embeddings.embed_query(text)
            sql = f'''SELECT original_text,
                    l2_distance(vector_data, ARRAY{response}) AS l2_dist
                    FROM vector_example_v1
                    WHERE VECTOR_SIMILARITY(vector_data, ARRAY{response}, 3)
                    order by l2_dist
                    limit 10
                    '''
            headers = {
                "Content-Type": "application/json",
                "authorization": f"Bearer {PINOT_API_KEY}"
            }
            response = requests.post(PINOT_QUERY_URL, json={"sql": sql}, headers=headers)

            if response.status_code == 200:
                raw_data = response.json()
            else:
                print(json.dumps({"error": "Failed to fetch data"}))
                exit(1)
            resultsTable = raw_data['resultTable']
            rows = resultsTable.get("rows", [])
            prompt = []
            prompt.append(f"There was an alert associated with this machine: {text} \n additional information used for generating content is here: \n")

            if len(rows) > 0:
                for row in rows:
                    prompt.append(str(row))  # Convert row to a string
                    prompt.append("use the previous information to generate an alert and recommendation for an HMI")

                final_prompt = "\n".join(prompt)
                llm_response = bedrock_client.invoke_model(
                    body=json.dumps({
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 1000,
                        "messages": [
                            {
                                "role": "user",
                                "content": final_prompt
                            }
                        ]
                    }),
                    modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
                )

                API_URL = "http://localhost:5000/api/alert"

                # Extract response from Claude 3.7
                response_body = json.loads(llm_response["body"].read())
                assistant_message = response_body["content"][0]["text"]

                # Create the payload
                response_object = {
                    "alerts": alerts,
                    "message": assistant_message  # Remove quotes; pass the variable itself
                }

                # Send the alert to the Flask API
                try:
                    response = requests.post(API_URL, json=response_object)
                    print(f"Response from API: {response.status_code}, {response.text}")
                except requests.exceptions.RequestException as e:
                    print(f"Error sending alert: {e}")
                                # need to post this back to the HMI
        print("No alert detected!")
    except Exception as e:
        print("Execution Error:", str(e))

if __name__ == "__main__":
    main()