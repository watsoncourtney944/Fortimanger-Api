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
def add_metadata_variable(variable_name, new_value, description):
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

# Process metadata from a defined list
def process_metadata(metadata_list):
    for meta in metadata_list:
        variable_name = meta['VariableName']
        new_value = meta['VariableValue']
        meta_description = meta['Description']

        if not add_metadata_variable(variable_name, new_value, meta_description):
            print("Aborting process due to metadata variable creation failure.")
            return

# Example metadata list
metadata_list = [
    {"VariableName": "SiteIP", "VariableValue": "", "Description": "IP address for site A"},
    {"VariableName": "Gateway", "VariableValue": "", "Description": "Default gateway for site A"}
]

# Run the metadata processing
process_metadata(metadata_list)
