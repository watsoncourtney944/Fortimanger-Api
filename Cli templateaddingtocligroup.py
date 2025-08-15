import requests
import json

# FortiManager details
fortimanager_ip = "10.80.29.30"
api_token = "yy1uehcg9fxgyn4tann3gbkzzr7gdkyy"  # Replace with your actual API token
adom = "NGDSTesting"  # Replace with your ADOM
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
      "data": {
        "member": [
          "test",
          "test2"
        ],
        "name": "newCliTGroup"
      },
      "url": f"/pm/config/adom/{adom}/obj/cli/template-group"
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
