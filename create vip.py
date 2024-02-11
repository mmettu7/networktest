import requests
from requests.auth import HTTPBasicAuth
import json

# Replace with your Netscaler details
NS_IP = 'YOUR_NETSCALER_IP'
NS_USER = 'YOUR_NETSCALER_USER'
NS_PASSWORD = 'YOUR_NETSCALER_PASSWORD'

# Function to make POST requests
def post_request(url, payload):
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, auth=HTTPBasicAuth(NS_USER, NS_PASSWORD), headers=headers, data=json.dumps(payload), verify=False)
    return response

# Function to create CSVs
def create_csv(name, ipv46):
    url = f'http://{NS_IP}/nitro/v1/config/csvserver'
    payload = {
        'csvserver': {
            'name': name,
            'ipv46': ipv46
        }
    }
    response = post_request(url, payload)
    return response.json()

# Function to create LBVs
def create_lbv(name, ipv46):
    url = f'http://{NS_IP}/nitro/v1/config/lbvserver'
    payload = {
        'lbvserver': {
            'name': name,
            'ipv46': ipv46,
            'lbmethod': 'LEASTCONNECTION'
        }
    }
    response = post_request(url, payload)
    return response.json()

# Function to create Service Groups
def create_service_group(name, servername, port):
    url = f'http://{NS_IP}/nitro/v1/config/servicegroup'
    payload = {
        'servicegroup': {
            'servicegroupname': name,
            'servicetype': 'HTTP',
            'protocol': 'TCP',
            'servername': servername,
            'port': port
        }
    }
    response = post_request(url, payload)
    return response.json()

# Function to bind Service Groups to LBVs
def bind_service_group_to_lbv(lbv_name, servicegroup_name):
    url = f'http://{NS_IP}/nitro/v1/config/lbvserver_servicegroup_binding'
    payload = {
        'lbvserver_servicegroup_binding': {
            'lbvserver_name': lbv_name,
            'servicegroupname': servicegroup_name
        }
    }
    response = post_request(url, payload)
    return response.json()

# Main function
def main():
    # CSVs
    csv_configs = [
        {'name': 'csv1', 'ipv46': '10.0.0.1'},
        {'name': 'csv2', 'ipv46': '10.0.0.2'}
    ]

    # LBVs
    lbv_configs = [
        {'name': 'lbv1', 'ipv46': '10.0.0.3'},
        {'name': 'lbv2', 'ipv46': '10.0.0.4'}
    ]

    # Service Groups
    service_group_configs = [
        {'name': 'servicegroup1', 'servername': 'server1', 'port': 80},
        {'name': 'servicegroup2', 'servername': 'server2', 'port': 80}
    ]

    # Create CSVs
    for config in csv_configs:
        response = create_csv(config['name'], config['ipv46'])
        print("CSV Creation Response:", response)

    # Create LBVs
    for config in lbv_configs:
        response = create_lbv(config['name'], config['ipv46'])
        print("LBV Creation Response:", response)

    # Create Service Groups
    for config in service_group_configs:
        response = create_service_group(config['name'], config['servername'], config['port'])
        print("Service Group Creation Response:", response)

    # Bind Service Groups to LBVs
    for lbv_config in lbv_configs:
        for service_group_config in service_group_configs:
            response = bind_service_group_to_lbv(lbv_config['name'], service_group_config['name'])
            print("Binding Response:", response)

if __name__ == "__main__":
    main()
