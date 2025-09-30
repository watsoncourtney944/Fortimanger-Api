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

# Helper function to send a POST request
def send_request(payload):
    response = requests.post(api_url, headers=headers, json=payload, verify=False)
    return response.json()

# Function to create model device
def create_model_device(device_name, hwmodel, psk, description):
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
                        "meta variables": {
                            "device_description": description  # Set any metadata you want here
                        },
                        "device blueprint": "device_test",
                        # "device blueprint": {
                        #     "platform": hwmodel,
                        #     "port-provisioning": 1,
                        #     "linked-to-model": True
                        # },
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
# def add_dynamic_mapping(variable_name, new_value, device_name):
#     payload = {
#         "id": 1,
#         "method": "add",
#         "params": [
#             {
#                 "url": f"pm/config/adom/{adom}/obj/fmg/variable/{variable_name}/dynamic_mapping",
#                 "data": {
#                     "value": new_value,
#                     "_scope": [{"name": device_name, "vdom": "root"}]
                    
#                 }
#             }
#         ]
#     }
#     data = send_request(payload)
#     if data["result"][0]["status"]["code"] == 0:
#         print(f"Dynamic mapping for '{variable_name}' added to device '{device_name}' successfully.")
#         return True
#     else:
#         print(f"Error adding dynamic mapping for '{variable_name}' on device '{device_name}': {json.dumps(data, indent=4)}")
#         return False

# Process devices from Excel
def process_devices(device_file):
    devices_df = pd.read_excel(device_file)

    # Step 1: Create devices
    for _, device_row in devices_df.iterrows():
        device_name = device_row['DeviceName']
        hwmodel = device_row['HWModel']
        psk = device_row['PSK']
        description = device_row['Description']

        # if create_model_device(device_name, hwmodel, psk, description):
        #     # Step 2: Apply dynamic mappings after device creation
        #     for _, mapping_row in devices_df.iterrows():  # Assuming same sheet is used for mappings
        #         variable_name = mapping_row['VariableName']
        #         new_value = mapping_row['VariableValue']

        #         if variable_name and new_value:  # Check if variable_name and new_value are valid
        #             # if not add_dynamic_mapping(variable_name, new_value, device_name):
        #                 print(f"Failed to apply dynamic mapping for '{variable_name}' on device '{device_name}'.")
        #         else:
        #             print(f"Skipping dynamic mapping for invalid data for device '{device_name}'.")
        # else:
        #     print(f"Skipping dynamic mapping for '{device_name}' due to device creation failure.")

# Example usage
process_devices('Devices2.xlsx')
