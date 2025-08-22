from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()  # Loads environment variables from .env

fortimanager_ip = os.getenv("FORTIMANAGER_IP")
api_token = os.getenv("API_TOKEN")
adom = os.getenv("ADOM")
api_url = f"https://{fortimanager_ip}/jsonrpc"

# Define headers with API token for authentication
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

def AddScript():
    # Payload for adding a script
    jsoncontent = {
        "id": 1,
        "jsonrpc": "1.0",
        "method": "add",
        "params": [
            {
                "data": {
                    "content": "get system status",
                    "desc": "Shows device details",
                    "name": "Status Script",
                    "target": "adom_database",
                    "type": "cli"
                },
                "url": f"/dvmdb/adom/{adom}/script"  # Use dynamic adom name
            }
        ],
       # "verbose": 1
    }

    # Send the request with the updated headers and payload
    print("jsoncontent:", json.dumps(jsoncontent, indent=4))
    print("url:", api_url)
    
    try:
        response = requests.post(api_url, headers=headers, json=jsoncontent, verify=False)
        
        # Check the response and handle success or failure
        if response.status_code == 200:
            print("Response Text:", json.dumps(response.json(), indent=4))
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Call the function to add the script
AddScript()
