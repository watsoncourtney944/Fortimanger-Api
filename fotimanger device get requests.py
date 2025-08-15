import requests
import json

fortimanager_ip = "10.80.29.30"
api_token = "yy1uehcg9fxgyn4tann3gbkzzr7gdkyy"

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
