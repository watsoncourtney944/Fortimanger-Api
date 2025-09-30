import requests
import json
import pandas as pd  # Import pandas to read Excel files
import urllib3
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
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

def add_metadata_variable(adom, api_url, headers, variable_name, new_value, description):
    # Payload for adding a new metadata variable
    add_variable_payload = {
        "id": 1,
        "method": "add",  # Action to add the new variable
        "params": [
            {
                "url": f"pm/config/adom/{adom}/obj/fmg/variable",  # Correct endpoint for metadata variables
                "data": {
                    "name": variable_name,  # The new metadata variable name
                    "value": new_value,  # The value for the metadata variable
                    "description":description
                }
            }
        ]
    }

    try:
        # Send the request to the FortiManager API to add the metadata variable
        response = requests.post(api_url, headers=headers, json=add_variable_payload, verify=False)
        data = response.json()

        # Check for successful response
        if response.status_code == 200 and "result" in data and data["result"][0]["status"]["code"] == 0:
            return f"Metadata variable '{variable_name}' added successfully."
        else:
            return f"Error adding {variable_name}: {json.dumps(data, indent=4)}"

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def add_device_mapping(adom, api_url, headers, variable_name, new_value, device_name):
    # Payload for adding a new device mapping to the metadata variable
    add_device_mapping_payload = {
        "id": 1,
        "method": "add",  # Action to add the mapping
        "params": [
            {
                "url": f"pm/config/adom/{adom}/obj/fmg/variable/{variable_name}/dynamic_mapping",  # URL for dynamic mapping
                "data": {
                    "value": new_value,  # The value for the metadata variable
                    "_scope": [  # Scope definition for device and VDOM
                        {
                            "name": device_name,  # The device name
                            "vdom": "global"  # VDOM name (can be modified if necessary)
                        }
                    ]
                }
            }
        ]
    }

    try:
        # Send the request to the FortiManager API to add the device mapping
        response = requests.post(api_url, headers=headers, json=add_device_mapping_payload, verify=False)
        data = response.json()

        # Check for successful response
        if response.status_code == 200 and "result" in data and data["result"][0]["status"]["code"] == 0:
            return f"Device mapping for '{variable_name}' on device '{device_name}' added successfully."
        else:
            return f"Error adding device mapping for {variable_name} on device {device_name}: {json.dumps(data, indent=4)}"

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def create_variables_and_mappings_from_excel(filename, adom, api_url, headers):
    try:
        #Read Excel file into a DataFrame
        df = pd.read_excel(filename)

        #Ensure columns are (VariableName, Value, DeviceName)
        for index, row in df.iterrows():
            variable_name = row['VariableName']
            new_value = row['Value']
            device_name = row['DeviceName']
            description = row['Description']

            print(f"Creating variable: {variable_name} with value: {new_value}")

           # Add metadata variable
            variable_result = add_metadata_variable(adom, api_url, headers, variable_name, new_value, description)
            print(variable_result)

            if "successfully" in variable_result:
                # After the variable is created successfully, add the device mapping
                mapping_result = add_device_mapping(adom, api_url, headers, variable_name, new_value, device_name)
                print(mapping_result)
            else:
                print("Skipping device mapping due to failure in creating the variable.")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

#Execute the function to create variables and mappings from the Excel file
create_variables_and_mappings_from_excel('variables.xlsx', adom, api_url, headers)
