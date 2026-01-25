import { google } from 'googleapis';
import readline from 'readline';

// Replace these with your OAuth credentials from Google Cloud Console
const CLIENT_ID = '111046729287-39hnhdm7i6vcg17q43copqhpaup4fvba.apps.googleusercontent.com';
const CLIENT_SECRET = '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';
const REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob';

const oauth2Client = new google.auth.OAuth2(
  CLIENT_ID,
  CLIENT_SECRET,
  REDIRECT_URI
);

// Scopes required for reading Google Docs
const SCOPES = ['https://www.googleapis.com/auth/documents.readonly'];

// Generate the URL for user authorization
const authUrl = oauth2Client.generateAuthUrl({
  access_type: 'offline',
  scope: SCOPES,
});

console.log('\n=== Google OAuth2 Setup ===\n');
console.log('1. Update CLIENT_ID and CLIENT_SECRET in this file');
console.log('2. Go to Google Cloud Console: https://console.cloud.google.com/');
console.log('3. Create OAuth 2.0 Client ID credentials (Desktop app)');
console.log('\n4. Authorize this app by visiting this URL:\n');
console.log(authUrl);
console.log('\n5. After authorization, paste the code here:\n');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question('Enter authorization code: ', async (code) => {
  try {
    const { tokens } = await oauth2Client.getToken(code);
    console.log('\n=== Success! ===\n');
    console.log('Add these to your environment variables:\n');
    console.log(`export GOOGLE_CLIENT_ID="${CLIENT_ID}"`);
    console.log(`export GOOGLE_CLIENT_SECRET="${CLIENT_SECRET}"`);
    console.log(`export GOOGLE_REFRESH_TOKEN="${tokens.refresh_token}"`);
    console.log('\nOr add to your .env file:\n');
    console.log(`GOOGLE_CLIENT_ID=${CLIENT_ID}`);
    console.log(`GOOGLE_CLIENT_SECRET=${CLIENT_SECRET}`);
    console.log(`GOOGLE_REFRESH_TOKEN=${tokens.refresh_token}`);
  } catch (error) {
    console.error('Error retrieving access token:', error.message);
  }
  rl.close();
});
