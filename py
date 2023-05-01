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

# Get the dashboard object
dashboard_url = f"{kibana_url}/api/kibana/dashboards/export?dashboard={dashboard_id}"
dashboard_response = requests.get(dashboard_url, headers=kibana_headers, auth=kibana_auth)
dashboard_response.raise_for_status()
dashboard_object = dashboard_response.json()

# Get the visualizations and index patterns
objects_url = f"{kibana_url}/api/kibana/objects"
objects_response = requests.get(objects_url, headers=kibana_headers, auth=kibana_auth)
objects_response.raise_for_status()
objects_data = objects_response.json()

# Filter the visualizations and index patterns to only include those used in the dashboard
visualization_ids = set()
index_pattern_ids = set()
for panel in dashboard_object['dashboard']['panelsJSON']:
    if panel['type'] == 'visualization':
        visualization_ids.add(panel['id'])
    elif panel['type'] == 'search':
        index_pattern_ids.add(panel['index_pattern_id'])
visualization_objects = [obj for obj in objects_data if obj['type'] == 'visualization' and obj['id'] in visualization_ids]
index_pattern_objects = [obj for obj in objects_data if obj['type'] == 'index-pattern' and obj['id'] in index_pattern_ids]

# Build the final object with all the necessary components
final_object = {
    'dashboard': dashboard_object['dashboard'],
    'visualizations': visualization_objects,
    'index-patterns': index_pattern_objects
}

# Save the final object to a file
with open(output_path, 'w') as f:
    json.dump(final_object, f)

print(f"Dashboard {dashboard_id} exported to {output_path}")
