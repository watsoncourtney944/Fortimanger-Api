import requests
import json

# FortiManager details
fortimanager_ip = "10.80.29.30"
api_token = "upzt9n3x3thi1s4cji4r758j9eanfu8b"  # Replace with your actual API token
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
        "method": "set",
        "params": [
            {
                "data": [
                    {
                        "oid": 6152,
                        "name": "device1_blueprint",
                        "enforce-device-config": "enable",
                        "linked-to-model": "enable",
                        "pkg": "default",
                        "platform": "FortiGate-40F",
                        "prerun-cliprof": ["test4"],
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
                        "oid": 6153,
                        "name": "device2_blueprint",
                        "enforce-device-config": "enable",
                        "linked-to-model": "enable",
                        "pkg": "default",
                        "platform": "FortiGate-40F",
                        "prerun-cliprof": ["test4"],
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

    # Make the API request
    try:
        response = requests.post(api_url, json=payload, headers=headers, verify=False)
        response.raise_for_status()  # This will raise an error for non-200 responses

        data = response.json()

        if response.status_code == 200 and "result" in data:
            print(f"Successfully updated device templates: {json.dumps(data, indent=4)}")
            return data["result"]
        else:
            print(f"Error in response: {json.dumps(data, indent=4)}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Example usage
device_templates = get_device_templates(adom, api_url, headers)
