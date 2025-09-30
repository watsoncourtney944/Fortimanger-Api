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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def update_metadata_variable(adom, api_url, headers, existing_variable_name, new_variable_name, new_value, description):
    # Prepare the payload to update the metadata variable based on the existing variable name
    update_variable_payload = {
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": f"pm/config/adom/{adom}/obj/fmg/variable/{existing_variable_name}",
                "data": {
                    "name": new_variable_name,  # Update with the new variable name
                    "value": new_value,
                    "description": description
                }
            }
        ]
    }

    try:
        # Send the request to the FortiManager API to update the metadata variable
        response = requests.post(api_url, headers=headers, json=update_variable_payload, verify=False)
        data = response.json()

        # Check if the update was successful
        if response.status_code == 200 and "result" in data and data["result"][0]["status"]["code"] == 0:
            return f"Metadata variable '{existing_variable_name}' updated to '{new_variable_name}' successfully."
        else:
            return f"Error updating {existing_variable_name}: {json.dumps(data, indent=4)}"

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def process_metadata_from_excel(filename, adom, api_url, headers):
    try:
        # Read Excel file into a DataFrame
        df_metadata = pd.read_excel(filename)

        # Loop over the DataFrame rows and update metadata variables
        for index, row in df_metadata.iterrows():
            existing_variable_name = row['ExistingVariableName']
            new_variable_name = row['NewVariableName']
            new_value = row['Value']
            description = row['Description']
            device_name = row['DeviceName']  # Ensure this column is present in your Excel file

            print(f"Checking and updating metadata variable: {existing_variable_name} to {new_variable_name} with value: {new_value}")
            variable_result = update_metadata_variable(adom, api_url, headers, existing_variable_name, new_variable_name, new_value, description)
            print(variable_result)

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
process_metadata_from_excel('variables2.xlsx', adom, api_url, headers)
