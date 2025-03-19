import boto3
from langchain_aws.embeddings import BedrockEmbeddings
import os
import requests
import json

session = boto3.Session(profile_name="default")
bedrock_client = session.client(service_name='bedrock-runtime', 
                              region_name='us-east-1')
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0",
                                        client=bedrock_client)

PINOT_BROKER = os.getenv("PINOT_BROKER")
PINOT_API_KEY = os.getenv("PINOT_API_KEY")
PINOT_QUERY_URL = f"{PINOT_BROKER}/query/sql" 

text = "Alert: The Fan Speed from the RTU is to High: RTU-2"
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
    exit

resultsTable = raw_data['resultTable']
column_names = resultsTable.get("dataSchema", {}).get("columnNames", [])
rows = resultsTable.get("rows", [])
prompt = [f"There was an alert associated with this machine: {text} \n additional information used for generating content is here: \n"]
if len(rows) > 0:
    for row in rows:
        prompt.append(f"{row}")
prompt.append("use the previous information to generate an alert and recommendation for an HMI")

prompt = "\n".join(prompt)
llm_response = bedrock_client.invoke_model(
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }),
    modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
)
response_body = json.loads(llm_response["body"].read())
assistant_message = response_body["content"][0]['text']
print(assistant_message)
    
