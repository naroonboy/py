const axios = require('axios');
const readline = require('readline');

// Controller details (replace with yours)
const CONTROLLER_URL = 'https://your-controller.saas.appdynamics.com'; // e.g., https://<account>.saas.appdynamics.com
const CLIENT_NAME = 'your-api-client-name'; // For SaaS OAuth
const CLIENT_SECRET = 'your-api-client-secret'; // For SaaS OAuth

// Create readline interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Function to prompt user for input
const prompt = (question) => new Promise((resolve) => rl.question(question, resolve));

// Function to get OAuth token (for SaaS)
async function getOAuthToken() {
  const response = await axios.post(`${CONTROLLER_URL}/controller/api/oauth/access_token`, null, {
    params: {
      grant_type: 'client_credentials',
      client_id: CLIENT_NAME,
      client_secret: CLIENT_SECRET
    }
  });
  return response.data.access_token;
}

// Function to create EUM browser app
async function createEUMApp() {
  try {
    // Prompt for app name and description
    const appName = await prompt('Enter the EUM application name: ');
    if (!appName.trim()) {
      throw new Error('Application name cannot be empty');
    }
    const appDescription = await prompt('Enter the application description (or press Enter to skip): ');

    // Get OAuth token for SaaS
    const token = await getOAuthToken();
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    };

    // For on-prem basic auth (uncomment if needed):
    // const auth = { username: 'user@account', password: 'password' };
    // const headers = { 'Content-Type': 'application/json' };
    // Use axios.create({ baseURL: CONTROLLER_URL, auth, headers }) below.

    // Create browser app
    const createResponse = await axios.post(`${CONTROLLER_URL}/controller/restui/applications/createApplicationWithType`, {
      name: appName.trim(),
      description: appDescription.trim() || '',
      type: 'BROWSER'
    }, { headers });
    
    const appId = createResponse.data.id;
    console.log(`Successfully created EUM browser app '${appName}' with ID: ${appId}`);
    return appId;

  } catch (error) {
    console.error('Error creating EUM app:', error.response ? error.response.data : error.message);
    throw error;
  } finally {
    rl.close(); // Close readline interface
  }
}

// Execute
createEUMApp();