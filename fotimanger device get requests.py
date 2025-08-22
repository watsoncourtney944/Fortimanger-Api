import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from .env

fortimanager_ip = os.getenv("FORTIMANAGER_IP")
api_token = os.getenv("API_TOKEN")
adom = os.getenv("ADOM")
api_url = f"https://{fortimanager_ip}/jsonrpc"
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

payload = {
    "method": "get",
    "params": [
        {
            "url": "dvm/api/v2/cmdb/system/device"
        }
    ]
}

response = requests.post(api_url, json=payload, headers=headers, verify=False)
data = response.json()

if "result" in data:
    for device in data["result"]:
        print(f"Device Name: {device['name']}, Blueprint: {device.get('device_blueprint', 'N/A')}")
else:
    print("Error: ", data)
