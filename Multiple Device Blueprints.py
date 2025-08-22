from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()  # Loads environment variables from .env

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

  "method": "add",
  "params": [
    {
      "data": [
      {
        "name":"device1_blueprint",
        # "auth-template": [
        #   "fat_001"
        # ],
        # # "dev-group": [
        #   "dev_grp_sites"
        # ],
        "enforce-device-config": "enable",
        # "ha-config": "enable",
        # "ha-hbdev": [
        #   "a",
        #   "0"
        # ],
        # "ha-monitor": [
        #   "lan",
        #   "wan"
        # ],
        #"ha-password": "fortinet",
        "linked-to-model": "enable",
        #"name": "device1",
        "pkg": "default",
        "platform": "FortiGate-40F",
        #"prefer-img-ver": "7.4.3-b2573",
        "prerun-cliprof": [
          "test4"
        ],
       #"prov-type": "template-group",
       #"template-group": "newCliTGroup"
        "prov-type": "template",
        "templates": [
            "4-1240__BRANCH_BGP_Recommended"
        ],
        "cliprofs": [
          "test"
              ],
        "template-group": "test"
      },
      {
        "name":"device2_blueprint",
        # "auth-template": [
        #   "fat_001"
        # ],
        # # "dev-group": [
        #   "dev_grp_sites"
        # ],
        "enforce-device-config": "enable",
        # "ha-config": "enable",
        # "ha-hbdev": [
        #   "a",
        #   "0"
        # ],
        # "ha-monitor": [
        #   "lan",
        #   "wan"
        # ],
        #"ha-password": "fortinet",
        "linked-to-model": "enable",
        #"name": "device1",
        "pkg": "default",
        "platform": "FortiGate-40F",
        #"prefer-img-ver": "7.4.3-b2573",
        "prerun-cliprof": [
          "test4"
        ],
              "prov-type": "template",
              "templates": [
                  "4-1240__BRANCH_BGP_Recommended"
              ],
              "cliprofs": [
               "test"
                    ],
        "template-group": "test"
      }
    ],
  
      "url": f"/pm/config/adom/{adom}/obj/fmg/device/blueprint"
    }
  ],
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
