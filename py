import requests
import json

# Define the URL and credentials for your Kibana instance
kibana_url = 'http://localhost:5601'
username = 'your_username'
password = 'your_password'

# Define the ID of the dashboard you want to export
dashboard_id = 'my_dashboard'

# Define the path where you want to save the exported dashboard JSON file
export_path = '/path/to/exported_dashboard.json'

# Make a GET request to the Kibana API to retrieve the dashboard object
dashboard_url = f'{kibana_url}/api/saved_objects/dashboard/{dashboard_id}'
headers = {
    'Content-Type': 'application/json',
}
auth = (username, password)
response = requests.get(dashboard_url, headers=headers, auth=auth)

# Check the response status code to see if the dashboard was retrieved successfully
if response.status_code == 200:
    dashboard = json.loads(response.content)
    
    # Make a GET request to the Kibana API to retrieve the related objects (visualizations and index patterns)
    related_objects = []
    for panel in dashboard['attributes']['panelsJSON']:
        if panel['type'] == 'visualization':
            vis_id = panel['embeddableConfig']['vis']['id']
            vis_url = f'{kibana_url}/api/saved_objects/visualization/{vis_id}'
            response = requests.get(vis_url, headers=headers, auth=auth)
            if response.status_code == 200:
                vis = json.loads(response.content)
                related_objects.append(vis)
        elif panel['type'] == 'search':
            search_id = panel['embeddableConfig']['savedObjectId']
            search_url = f'{kibana_url}/api/saved_objects/search/{search_id}'
            response = requests.get(search_url, headers=headers, auth=auth)
            if response.status_code == 200:
                search = json.loads(response.content)
                related_objects.append(search)
                
    # Add the related objects to the dashboard object
    dashboard['references'] += related_objects
    
    # Write the dashboard JSON to the export file path
    with open(export_path, 'w') as f:
        json.dump(dashboard, f, indent=4)
    print(f'Dashboard {dashboard_id} exported successfully to {export_path}')
else:
    print(f'Error exporting dashboard {dashboard_id}: {response.content}')
