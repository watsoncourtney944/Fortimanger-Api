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
                        "name": device_name,
                        "adm_usr": "admin",
                        "os_ver": 7,
                        "version": 700,
                        "os_type": 0,
                        "mr": 4,
                        "mgmt_mode": 3,
                        "psk": psk,
                        "device blueprint": {
                            "platform": hwmodel,
                            "port-provisioning": 1,
                            "linked-to-model": True
                        },
                        "flags": 262176,  # You can modify flags here if needed
                        "faz.perm": 15,
                        "faz.quota": 0
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
    else:
        print(f"Error creating device '{device_name}': {json.dumps(data, indent=4)}")
        return False


# Function to process devices and metadata
def process_devices_and_metadata(device_file, metadata_file, adom, api_url, headers):
    devices_df = pd.read_excel(device_file)
    metadata_df = pd.read_excel(metadata_file)

    for index, row in devices_df.iterrows():
        device_name = row['DeviceName']
        hwmodel = row['HWModel']
        psk = row['PSK']
        description = row['Description']

        # Step 1: Add metadata variables first, but don't block device creation
        for _, meta_row in metadata_df.iterrows():
            variable_name = meta_row['VariableName']
            new_value = meta_row['VariableValue']
            meta_description = meta_row['Description']

            # Add metadata variable, continue to next if it fails
            if not add_metadata_variable(adom, api_url, headers, variable_name, new_value, meta_description):
                print(f"Skipping metadata variable '{variable_name}' due to failure but continuing with other variables.")
        
        # Step 2: Create the model device after processing metadata
        print(f"Attempting to create device '{device_name}'...")
        create_model_device(adom, device_name, hwmodel, psk, description, api_url, headers)


# Example usage
process_devices_and_metadata('Devices.xlsx', 'metadata.xlsx', adom, api_url, headers)
