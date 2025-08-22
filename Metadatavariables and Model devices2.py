from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd
import urllib3

load_dotenv()  # Loads environment variables from .env

fortimanager_ip = os.getenv("FORTIMANAGER_IP")
api_token = os.getenv("API_TOKEN")
adom = os.getenv("ADOM")
api_url = f"https://{fortimanager_ip}/jsonrpc"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define headers with API token
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Function to add metadata variable
def add_metadata_variable(adom, api_url, headers, variable_name, new_value, description):
    payload = {
        "id": 1,
        "method": "add",
        "params": [
            {
                "url": f"pm/config/adom/{adom}/obj/fmg/variable",
                "data": {
                    "name": variable_name,
                    "value": new_value,
                    "description": description
                }
            }
        ]
    }

    response = requests.post(api_url, headers=headers, json=payload, verify=False)
    data = response.json()

    if response.status_code == 200 and "result" in data and data["result"][0]["status"]["code"] == 0:
        print(f"Metadata variable '{variable_name}' added successfully.")
        return True
    elif data["result"][0]["status"]["code"] == -3:
        print(f"Metadata variable '{variable_name}' already exists.")
        return True  # Consider it successful if it already exists
    else:
        print(f"Error adding metadata variable '{variable_name}': {json.dumps(data, indent=4)}")
        return False

# Function to create model device
def create_model_device(adom, device_name, hwmodel, psk, description, api_url, headers):
    payload = {
        "method": "exec",
        "params": [
            {
                "url": "dvm/cmd/add/device",
                "data": {
                    "adom": adom,
                    "device": {
                        "device action": "add_model",
                        "meta variables": {
                            "NewVar1": "IP for Branch Office"  # Set any metadata you want here
                        },
                        "name": device_name,
                        "adm_usr": "admin",
                        "os_ver": 7,
                        "version": 700,
                        "os_type": 0,
                        "mr": 4,
                        "mgmt_mode": 3,
                        "psk": psk,
                        "device blueprint":"test",
                        # "device blueprint": {
                        #     "platform": hwmodel,
                        #     "port-provisioning": 1,
                        #     "linked-to-model": True
                        # },
                        "flags": ['None'],  # flags
                        "faz.perm": 15,
                        "faz.quota": 0,
                                "groups": [
                            {
                                "name": "SDWANsites"
                            }
                            ]
                    }
                }
            }
        ]
    }

    response = requests.post(api_url, json=payload, headers=headers, verify=False)
    data = response.json()

    if response.status_code == 200 and "result" in data and data["result"][0]["status"]["code"] == 0:
        print(f"Device '{device_name}' created successfully.")
        return True
    elif data["result"][0]["status"]["code"] == -3:
        print(f"Device '{device_name}' already exists.")
        return True  # Treat as successful if device already exists
    else:
        print(f"Error creating device '{device_name}': {json.dumps(data, indent=4)}")
        return False

# Function to add dynamic mapping after device creation
def add_dynamic_mapping(adom, api_url, headers, variable_name, new_value, device_name):
    payload = {
        "id": 1,
        "method": "add",
        "params": [
            {
                "url": f"pm/config/adom/{adom}/obj/fmg/variable/{variable_name}/dynamic_mapping",
                "data": {
                    "value": new_value,
                    "_scope": [
                        {
                            "name": device_name,
                            "vdom": "root"  # Adjust VDOM if needed
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(api_url, headers=headers, json=payload, verify=False)
    data = response.json()

    if response.status_code == 200 and "result" in data and data["result"][0]["status"]["code"] == 0:
        print(f"Dynamic mapping for '{variable_name}' added to device '{device_name}' successfully.")
        return True
    else:
        print(f"Error adding dynamic mapping for '{variable_name}' on device '{device_name}': {json.dumps(data, indent=4)}")
        return False
       

# Process devices and metadata from Excel
def process_devices_and_metadata(device_file, metadata_file, adom, api_url, headers):
    devices_df = pd.read_excel(device_file)
    metadata_df = pd.read_excel(metadata_file)

    # Step 1: Add metadata variables first
    metadata_success = True
    for _, meta_row in metadata_df.iterrows():
        variable_name = meta_row['VariableName']
        new_value = meta_row['VariableValue']
        meta_description = meta_row['Description']

        if not add_metadata_variable(adom, api_url, headers, variable_name, new_value, meta_description):
            metadata_success = False
            break  # Stop if any metadata variable fails to add

    if not metadata_success:
        print("Aborting process due to metadata variable creation failure.")
        return

    # Step 2: Create devices and apply dynamic mapping
    for index, row in devices_df.iterrows():
        device_name = row['DeviceName']
        hwmodel = row['HWModel']
        psk = row['PSK']
        description = row['Description']

        if create_model_device(adom, device_name, hwmodel, psk, description, api_url, headers):
            # After device creation, apply dynamic mappings
            for _, meta_row in metadata_df.iterrows():
                variable_name = meta_row['VariableName']
                new_value = meta_row['VariableValue']

                if not add_dynamic_mapping(adom, api_url, headers, variable_name, new_value, device_name):
                    print(f"Failed to apply dynamic mapping for '{variable_name}' on device '{device_name}'.")
        else:
            print(f"Skipping dynamic mapping for '{device_name}' due to device creation failure.")

# Example usage
process_devices_and_metadata('Devices.xlsx', 'metadata.xlsx', adom, api_url, headers)
