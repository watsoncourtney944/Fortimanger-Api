from dotenv import load_dotenv
import os
import requests
import json
import sys

load_dotenv()  # Loads environment variables from .env

fortimanager_ip = os.getenv("FORTIMANAGER_IP")
api_token = os.getenv("API_TOKEN")
adom = os.getenv("ADOM")
api_url = f"https://{fortimanager_ip}/jsonrpc"
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Redirect stdout to a file
#output_file = "fortiswitch_output.txt"
#sys.stdout = open(output_file, "w")

def get_fortiswitch_ports_from_vlans():
    resource_path = "/api/v2/cmdb/switch-controller/managed-switch"
    payload = {
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": "sys/proxy/json",
                "data": {
                    "target": [f"adom/{adom}/device/{device_name}"],
                    "action": "get",
                    "resource": resource_path
                }
            }
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, verify=False, timeout=30)
        if response.status_code == 200:
            data = response.json()
            #print(f"Raw Data from {resource_path}:")
           # print(json.dumps(data, indent=4))
            # print(response)

            if "result" in data and data["result"][0]["status"]["code"] == 0:
                vlans = data["result"][0]["data"]
                print("Port Details from VLANs:")
                for vlan in vlans:
                    print(f"VLAN Name: {vlan.get('name', 'N/A')}")
                    if "ports" in vlan:
                        print("  Ports:")
                        for port in vlan["ports"]:
                            print(f"    Port Name: {port.get('name', 'N/A')}")
                            print(f"      Status: {port.get('status', 'N/A')}")
                            print(f"      Speed: {port.get('speed', 'N/A')}")
                    else:
                        print("  No ports associated with this VLAN.")
                    print()
            else:
                print(f"Error retrieving data from {resource_path}: {data}")
        else:
            print(f"HTTP Error {response.status_code} for {resource_path}:")
            print(response.text)
    except Exception as e:
        print(f"Error querying {resource_path}: {e}")


# Call the function
get_fortiswitch_ports_from_vlans()
