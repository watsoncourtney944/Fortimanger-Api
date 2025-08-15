import requests
import json

# FortiManager details
fortimanager_ip = "10.80.29.30"
api_token = "yy1uehcg9fxgyn4tann3gbkzzr7gdkyy"  # Replace with your actual token
adom = "NGDSTesting"  # Specify your ADOM name
api_url = f"https://{fortimanager_ip}/jsonrpc"

# Define headers with API token for authentication
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

def AddScript():
    # Payload for adding a script
    jsoncontent = {
        "id": 1,
        "jsonrpc": "1.0",
        "method": "add",
        "params": [
            {
                "data": {
                    "content": "get system status",
                    "desc": "Shows device details",
                    "name": "Status Script",
                    "target": "adom_database",
                    "type": "cli"
                },
                "url": f"/dvmdb/adom/{adom}/script"  # Use dynamic adom name
            }
        ],
       # "verbose": 1
    }

    # Send the request with the updated headers and payload
    print("jsoncontent:", json.dumps(jsoncontent, indent=4))
    print("url:", api_url)
    
    try:
        response = requests.post(api_url, headers=headers, json=jsoncontent, verify=False)
        
        # Check the response and handle success or failure
        if response.status_code == 200:
            print("Response Text:", json.dumps(response.json(), indent=4))
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Call the function to add the script
AddScript()
