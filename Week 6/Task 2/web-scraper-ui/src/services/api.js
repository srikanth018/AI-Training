import { BedrockAgentRuntimeClient, InvokeAgentCommand } from '@aws-sdk/client-bedrock-agent-runtime';

// AWS Configuration - Update these with your values
const AWS_CONFIG = {
  region: 'us-east-1',
  credentials: {
    accessKeyId: import.meta.env.VITE_AWS_ACCESS_KEY_ID || '',
    secretAccessKey: import.meta.env.VITE_AWS_SECRET_ACCESS_KEY || '',
    sessionToken: import.meta.env.VITE_AWS_SESSION_TOKEN || undefined,
  },
};

// Bedrock Agent Configuration - Update with your agent details
const AGENT_CONFIG = {
  agentId: import.meta.env.VITE_BEDROCK_AGENT_ID || 'YOUR_AGENT_ID',
  agentAliasId: import.meta.env.VITE_BEDROCK_AGENT_ALIAS_ID || 'YOUR_AGENT_ALIAS_ID',
};

// Initialize Bedrock Agent Runtime Client
const bedrockClient = new BedrockAgentRuntimeClient(AWS_CONFIG);

// Generate a unique session ID for each user session
const generateSessionId = () => {
  return `session-${Date.now()}-${Math.random().toString(36).substring(7)}`;
};

let currentSessionId = generateSessionId();

export const crawlWebContent = async (query) => {
  try {
    const command = new InvokeAgentCommand({
      agentId: AGENT_CONFIG.agentId,
      agentAliasId: AGENT_CONFIG.agentAliasId,
      sessionId: currentSessionId,
      inputText: query,
    });

    const response = await bedrockClient.send(command);
    
    // Process the streaming response
    let fullResponse = '';
    
    if (response.completion) {
      for await (const chunk of response.completion) {
        if (chunk.chunk && chunk.chunk.bytes) {
          const decodedChunk = new TextDecoder().decode(chunk.chunk.bytes);
          fullResponse += decodedChunk;
        }
      }
    }

    return {
      content: fullResponse || 'No response from agent',
      sessionId: currentSessionId,
    };
  } catch (error) {
    console.error('Error calling Bedrock Agent:', error);
    throw new Error(`Bedrock Agent Error: ${error.message}`);
  }
};

// Function to reset the session (start a new conversation)
export const resetSession = () => {
  currentSessionId = generateSessionId();
  return currentSessionId;
};
