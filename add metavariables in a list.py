import requests
import json
import pandas as pd
import urllib3
import sys
from dotenv import load_dotenv
import os

# Load environment variables from .env file
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

# Function to add multiple metadata variables in a single API call
def add_metadata_variables(adom, api_url, headers, metadata_list):
    """Adds multiple metadata variables in a single API request."""
    
    payload = {
        "id": 1,
        "method": "add",
        "params": [
            {
                "url": f"pm/config/adom/{adom}/obj/fmg/variable",
                "data": metadata_list  # Sending multiple metadata variables at once
            }
        ]
    }

    response = requests.post(api_url, headers=headers, json=payload, verify=False)
    data = response.json()

    if response.status_code == 200 and "result" in data and data["result"][0]["status"]["code"] == 0:
        print(f"Metadata variables added successfully.")
        return True
    else:
        print(f"Error adding metadata variables: {json.dumps(data, indent=4)}")
        return False

# Process metadata from Excel
def process_metadata(metadata_file, adom, api_url, headers):
    metadata_df = pd.read_excel(metadata_file)

    # Collect all metadata variables in a list for batch processing
    metadata_list = []
    for _, meta_row in metadata_df.iterrows():
        variable_name = meta_row['VariableName']
        new_value = meta_row['Value']
        description = meta_row['Description']

        # Ensure the values are not empty before adding to the list
        if pd.notna(variable_name) and pd.notna(new_value) and pd.notna(description):
            metadata_list.append({
                "name": variable_name,
                "value": new_value,
                "description": description
            })

    if metadata_list:  # Only make the API call if there's data to send
        add_metadata_variables(adom, api_url, headers, metadata_list)
    else:
        print("No valid metadata variables found in the file.")

# Example usage
process_metadata('variables.xlsx', adom, api_url, headers)
