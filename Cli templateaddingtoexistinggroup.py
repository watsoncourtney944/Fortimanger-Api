import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from .env

# FortiManager details
fortimanager_ip = os.getenv("FORTIMANAGER_IP")
api_token = os.getenv("API_TOKEN")
adom = os.getenv("ADOM")
api_url = f"https://{fortimanager_ip}/jsonrpc"

# Define headers with API token
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Function to get existing device templates
def get_device_templates(adom, api_url, headers):
    payload = {
   
  #"id": 3,
  "method": "add",
  "params": [
    {
      "data": [
          {
          "test3"
          }
      ],
      "url": f"/pm/config/adom/{adom}/obj/cli/template-group/newCliTGroup/scopemember"
    }
    ]
    }

    response = requests.post(api_url, json=payload, headers=headers, verify=False)
    data = response.json()

    if response.status_code == 200 and "result" in data:
        print(f"Existing device templates: {json.dumps(data, indent=4)}")
        return data["result"]
    else:
        print(f"Error fetching device templates: {json.dumps(data, indent=4)}")
        return None


# Example usage
device_templates = get_device_templates(adom, api_url, headers)
