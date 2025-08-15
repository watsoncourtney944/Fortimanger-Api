import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# FortiManager details
fortimanager_ip = "10.80.29.30"
api_token = "yy1uehcg9fxgyn4tann3gbkzzr7gdkyy"  # Replace with a valid token
adom = "NGDSTesting"
api_url = f"https://{fortimanager_ip}/jsonrpc"

# Define headers with API token
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Helper function to send a POST request
def send_request(payload):
    response = requests.post(api_url, headers=headers, json=payload, verify=False)
    return response.json()

# Function to create a model device
def create_model_device(device_name, hwmodel, psk, description, metadata):
    payload = {
        "method": "exec",
        "params": [
            {
                "url": "dvm/cmd/add/device",
                "data": {
                    "adom": adom,
                    "device": {
                        "name": device_name,
                        "adm_usr": "admin",
                        "os_ver": 7,
                        "version": 700,
                        "os_type": 0,
                        "mr": 4,
                        "mgmt_mode": 3,
                        "psk": psk,
                        "device action": "add_model",
                        "meta variables": metadata,
                        "device blueprint": {
                            "platform": hwmodel,
                            "port-provisioning": 1,
                            "linked-to-model": True
                        },
                        "flags": "create_task",
                        "faz.perm": 15,
                        "faz.quota": 0,
                    }
                }
            }
        ]
    }
    data = send_request(payload)
    if data["result"][0]["status"]["code"] == 0:
        print(f"Device '{device_name}' created successfully.")
        return True
    elif data["result"][0]["status"]["code"] == -3:
        print(f"Device '{device_name}' already exists.")
        return True
    else:
        print(f"Error creating device '{device_name}': {json.dumps(data, indent=4)}")
        return False

# Function to add dynamic mapping after device creation
def add_dynamic_mapping(variable_name, new_value, device_name):
    payload = {
        "id": 1,
        "method": "add",
        "params": [
            {
                "url": f"pm/config/adom/{adom}/obj/fmg/variable/{variable_name}/dynamic_mapping",
                "data": {
                    "value": new_value,
                    "_scope": [{"name": device_name, "vdom": "root"}]
                }
            }
        ]
    }
    data = send_request(payload)
    if data["result"][0]["status"]["code"] == 0:
        print(f"Dynamic mapping for '{variable_name}' added to device '{device_name}' successfully.")
        return True
    else:
        print(f"Error adding dynamic mapping for '{variable_name}' on device '{device_name}': {json.dumps(data, indent=4)}")
        return False

# Example device list with metadata
devices = [
    {
        "DeviceName": "Branch1-FW",
        "HWModel": "FortiGate-40F",
        "PSK": "securepsk1",
        "Description": "Branch Office Firewall 1",
        "Metadata": {
            "SiteID": "001",
            "Location": "New York",
            "WAN_IP": "192.168.1.1"
        }
    },
    {
        "DeviceName": "Branch2-FW",
        "HWModel": "FortiGate-40F",
        "PSK": "securepsk2",
        "Description": "Branch Office Firewall 2",
        "Metadata": {
            "SiteID": "002",
            "Location": "Los Angeles",
            "WAN_IP": "192.168.2.1"
        }
    }
]

# Process devices and apply dynamic mappings
for device in devices:
    device_name = device["DeviceName"]
    hwmodel = device["HWModel"]
    psk = device["PSK"]
    description = device["Description"]
    metadata = device["Metadata"]

    if create_model_device(device_name, hwmodel, psk, description, metadata):
        for variable_name, new_value in metadata.items():
            if not add_dynamic_mapping(variable_name, new_value, device_name):
                print(f"Failed to apply dynamic mapping for '{variable_name}' on device '{device_name}'.")
    else:
        print(f"Skipping dynamic mapping for '{device_name}' due to device creation failure.")
