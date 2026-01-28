# Web Scraper UI

A modern React application built with Vite that provides a chat interface to interact with AWS Bedrock AI Agent directly.

## Features

- 🎨 Modern, responsive chat interface
- 🤖 Direct integration with AWS Bedrock Agent Runtime
- 💬 Session-based conversations with message history
- ⚡ Fast development with Vite and HMR
- 🎯 Clean, intuitive user experience
- 🔄 Session management for multi-turn conversations

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- AWS Account with Bedrock Agent created
- AWS credentials with permissions to invoke Bedrock agents

## Installation

1. Navigate to the project directory:
```bash
cd web-scraper-ui
```

2. Install dependencies:
```bash
npm install
```

3. Configure AWS credentials and Bedrock Agent:

Create a `.env` file in the root directory (copy from `.env.example`):

```env
# AWS Credentials
VITE_AWS_ACCESS_KEY_ID=your_access_key_id
VITE_AWS_SECRET_ACCESS_KEY=your_secret_access_key
VITE_AWS_SESSION_TOKEN=your_session_token_if_using_temporary_credentials

# Bedrock Agent Configuration
VITE_BEDROCK_AGENT_ID=your_bedrock_agent_id
VITE_BEDROCK_AGENT_ALIAS_ID=your_bedrock_agent_alias_id
```

**Important Security Notes:**
- Never commit the `.env` file to version control
- For production, use AWS Cognito or IAM roles instead of hardcoded credentials
- Consider using temporary credentials with session tokens

## Getting Your Bedrock Agent Details

1. Go to AWS Bedrock Console
2. Navigate to "Agents" section
3. Select your agent
4. Copy the **Agent ID** (format: `XXXXXXXXXX`)
5. Copy the **Agent Alias ID** (usually `TSTALIASID` for test or a custom alias)

## Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Building for Production

Build the application:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
web-scraper-ui/
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx    # Main chat UI component
│   │   └── ChatInterface.css    # Chat styling
│   ├── services/
│   │   └── api.js               # Bedrock Agent API integration
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── .env                          # Environment variables (not in git)
├── .env.example                  # Environment template
├── index.html
├── package.json
└── vite.config.js
```

## Usage

1. Type your question in the input field
2. Click the send button (🚀) or press Enter
3. Wait for the Bedrock AI agent to process and respond
4. Continue the conversation - sessions maintain context
5. Clear the chat history using the trash button (🗑️) to start a new session

## How It Works

The application uses the AWS Bedrock Agent Runtime API to:
1. Create a unique session for each user
2. Send user queries to the Bedrock agent
3. Stream responses back to the UI
4. Maintain conversation context across multiple turns

## API Configuration

The Bedrock configuration is in `src/services/api.js`. The app uses environment variables for security:

```javascript
const AWS_CONFIG = {
  region: 'us-east-1',
  credentials: {
    accessKeyId: import.meta.env.VITE_AWS_ACCESS_KEY_ID,
    secretAccessKey: import.meta.env.VITE_AWS_SECRET_ACCESS_KEY,
    sessionToken: import.meta.env.VITE_AWS_SESSION_TOKEN,
  },
};
```

## Technologies Used

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **AWS SDK for JavaScript v3** - Bedrock Agent Runtime client
- **CSS3** - Styling with animations and gradients
- **AWS Bedrock** - AI Agent service

## Troubleshooting

### Error: "Missing credentials"
- Ensure your `.env` file is properly configured
- Check that environment variables start with `VITE_`
- Restart the dev server after changing `.env`

### Error: "Access Denied"
- Verify your AWS credentials have `bedrock:InvokeAgent` permission
- Check that the agent ID and alias ID are correct

### Error: "Agent not found"
- Confirm the agent is deployed and active in AWS Bedrock
- Verify the region matches your agent's region
