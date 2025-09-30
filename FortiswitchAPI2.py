import requests
import json
import sys
import openpyxl
from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from .env

# FortiManager details
fortimanager_ip = os.getenv("FORTIMANAGER_IP")
api_token = os.getenv("API_TOKEN")
adom = os.getenv("ADOM")
device_name = "SPOKE4-FGT-01"  # Specify the device name or serial number
api_url = f"https://{fortimanager_ip}/jsonrpc"
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

#Redirect stdout to a file
# output_file = "fortiswitch_output2.txt"
# sys.stdout = open(output_file, "w")



def get_fortiswitch_ports():
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
            print(f"Raw Data from {resource_path}:")
            print(json.dumps(data, indent=4))  # Debugging: print the entire raw response

            # Check if 'result' and 'data' are present
            if "result" in data and data["result"][0]["status"]["code"] == 0:
                # Access the 'response' -> 'results' to find the detailed switch data
                switch_info = data["result"][0].get("data", [])
                for switch in switch_info:
                    response_data = switch.get("response", {})
                    if "results" in response_data:
                        results = response_data["results"]
                        # Iterate through each result and print the details (such as ports)
                        for item in results:
                            print(f"Switch Name: {item.get('name', 'N/A')}")
                            print(f"  Serial Number: {item.get('sn', 'N/A')}")
                            print(f"  Model: {item.get('model', 'N/A')}")
                            print(f"  Version: {item.get('version', 'N/A')}")
                            print("Ports Information:")

                            # Parse and print port details
                            ports = item.get('ports', [])
                            if ports:
                                for port in ports:
                                    print(f"  Port Name: {port.get('port-name', 'N/A')}")
                                    print(f"    VLAN: {port.get('vlan', 'N/A')}")
                                    print(f"    STATUS: {port.get('status', 'N/A')}")
                                    print(f"    Allowed VLANs: {port.get('allowed-vlans', 'N/A')}")
                                    print(f"    Untagged VLANs: {port.get('untagged-vlans', 'N/A')}")
                                    print(f"    MAC Address: {port.get('mac-addr', 'N/A')}")
                                    print(f"    Export to: {port.get('export-to', 'N/A')}")
                                    print()
                            else:
                                print("  No ports found.")
                            print()
            else:
                print(f"Error retrieving switch data: {data}")
        else:
            print(f"HTTP Error {response.status_code} for {resource_path}:")
            print(response.text)

    except Exception as e:
        print(f"Error querying {resource_path}: {e}")


get_fortiswitch_ports()