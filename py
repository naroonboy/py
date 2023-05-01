import json
import requests

# Set the Kibana URL and credentials
kibana_url = 'http://localhost:5601'
kibana_username = 'your_username'
kibana_password = 'your_password'

# Set the dashboard ID and output file path
dashboard_id = 'your_dashboard_id'
output_path = 'path/to/output/file.json'

# Build the Kibana headers with the authentication credentials
kibana_auth = (kibana_username, kibana_password)
kibana_headers = {
    'Content-Type': 'application/json',
    'kbn-xsrf': 'true'
}

# Build the request body with the dashboard ID and includeReferencesDeep option
request_body = {
    'dashboard': {
        'id': dashboard_id
    },
    'type': 'dashboard',
    'version': 1,
    'attributes': {
        'title': 'Dashboard Title'
    },
    'references': [],
    'includeReferencesDeep': True
}

# Send the export request
export_url = f"{kibana_url}/api/saved_objects/_export"
export_response = requests.post(export_url, headers=kibana_headers, auth=kibana_auth, json=request_body)
export_response.raise_for_status()
export_data = export_response.content

# Save the export data to a file
with open(output_path, 'wb') as f:
    f.write(export_data)

print(f"Dashboard {dashboard_id} exported to {output_path}")
