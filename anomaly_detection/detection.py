import json
import requests
import os

PINOT_BROKER = os.getenv("PINOT_BROKER")
PINOT_API_KEY = os.getenv("PINOT_API_KEY")
PINOT_QUERY_URL = f"{PINOT_BROKER}/query/sql" 

def main():
    try:
        with open("./queries.json", 'r') as f:
            raw_data = f.read()
        data = json.loads(raw_data)
        for record in data:
            query = record['sql']
            headers = {
                "Content-Type": "application/json",
                "authorization": f"Bearer {PINOT_API_KEY}" 
            }
            response = requests.post(PINOT_QUERY_URL, json={"sql": query, "queryOptions": "useMultistageEngine=true"}, headers=headers)

            if response.status_code == 200:
                raw_response = response.json()
                resultsTable = raw_response['resultTable']
                column_names = resultsTable.get("dataSchema", {}).get("columnNames", [])
                rows = resultsTable.get("rows", [])
                if len(rows) > 0:
                    structured_data = {column_names[i]: rows[0][i] for i in range(len(column_names))}
                    print(structured_data)
            else:
                json.dumps({"error": "Failed to fetch data"}), response.status_code
            
    except Exception as e:
        print("Execution Error:", str(e))
        return {"statusCode": 500, "body": str(e)}

if __name__ == "__main__":
    main()