import requests
import json
import sys 

# FortiManager details
fortimanager_ip = "10.80.29.30"
api_token = "yy1uehcg9fxgyn4tann3gbkzzr7gdkyy"  # Replace with a valid token
adom = "GLOBAL_LAB"  # Specify the ADOM name
api_url = f"https://{fortimanager_ip}/jsonrpc"

# Define headers with API token
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Redirect stdout to a file
output_file = "metadatavariable_output.txt"
sys.stdout = open(output_file, "w")

# Construct the request payload to get metadata variables
payload = {
    "id": 1,
    "method": "get",
    "params": [
        {
            "url": f"pm/config/adom/{adom}/obj/fmg/variable"
        }
    ]
}

# Send the request
try:
    response = requests.post(api_url, headers=headers, json=payload, verify=False)

    # Check response status
    if response.status_code == 200:
        data = response.json()
        print("Metadata Variables:")
        print(json.dumps(data, indent=4))  # Pretty print JSON response

        # Extract and display metadata variables
        if "result" in data and data["result"][0]["status"]["code"] == 0:
            metadata_variables = data["result"][0].get("data", [])
            if metadata_variables:
                for variable in metadata_variables:
                    print(f"Name: {variable.get('name', 'N/A')}")
                    print(f"  Value: {variable.get('value', 'N/A')}")
                    print(f"  Type: {variable.get('type', 'N/A')}")
                    print(f"  Description: {variable.get('description', 'N/A')}")
                    print()
            else:
                print("No metadata variables found.")
        else:
            print("Error retrieving metadata variables:", json.dumps(data, indent=4))
    else:
        print(f"HTTP Error {response.status_code}: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
