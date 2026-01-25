# AI Agent with MCP Server

A comprehensive AI-powered assistant system that provides intelligent access to company policies, employee benefits, and workplace guidelines through multiple data sources.

## Overview

This project consists of two integrated components:

1. **MCP Server** - A Model Context Protocol server that provides Google Docs access
2. **AI Agent** - An intelligent agent powered by AWS Bedrock with multi-source data capabilities

The AI Agent acts as a unified conversational interface, leveraging the MCP Server for document access along with PDF RAG and web search capabilities to answer employee questions about company policies and benefits.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      AI Agent                           │
│  (AWS Bedrock + LangChain + Multi-Tool Integration)   │
└─────────────┬──────────────┬──────────────┬────────────┘
              │              │              │
              │              │              │
      ┌───────▼──────┐  ┌───▼────────┐  ┌──▼──────────┐
      │ MCP Client   │  │ PDF RAG    │  │ Web Search  │
      │ (Google Docs)│  │ (FAISS)    │  │ (Tavily)    │
      └───────┬──────┘  └────────────┘  └─────────────┘
              │
      ┌───────▼──────────┐
      │   MCP Server     │
      │ (HTTP + SSE)     │
      └───────┬──────────┘
              │
      ┌───────▼──────────┐
      │  Google Docs API │
      └──────────────────┘
```

## Features

### AI Agent
- **Conversational Interface** - Natural language interaction
- **Multi-Source Intelligence** - Integrates Google Docs, PDFs, and web search
- **Context-Aware Routing** - Automatically selects the right data source
- **Streaming Responses** - Real-time answer generation
- **AWS Bedrock Integration** - Powered by Claude AI models

### MCP Server
- **MCP Protocol Implementation** - Standard Model Context Protocol
- **Google Docs Integration** - Read and extract structured information
- **HTTP/SSE Transport** - Real-time communication
- **Extensible Architecture** - Easy to add new tools

## Project Structure

```
.
├── AI_Agent/
│   ├── main.py                    # Agent entry point
│   ├── requirements.txt           # Python dependencies
│   ├── agent/
│   │   └── agent.py              # Agent configuration
│   ├── llm/
│   │   └── bedrock.py            # AWS Bedrock setup
│   ├── tools/
│   │   ├── mcp_client.py         # MCP client for Google Docs
│   │   ├── pdf_rag_tool.py       # PDF RAG tool
│   │   └── web_search_tool.py    # Web search tool
│   └── pdf_rag/                  # PDF documents directory
│
└── MCP_Server/
    ├── server.js                  # Server entry point
    ├── package.json               # Node.js dependencies
    ├── transports.js              # SSE transport
    ├── tools/
    │   ├── index.js              # Tool registry
    │   └── googleDocTool.js      # Google Docs tool
    └── utils/
        └── googleApi.js          # Google API utilities
```

## Prerequisites

- **Node.js** v16 or higher (for MCP Server)
- **Python** 3.8 or higher (for AI Agent)
- **AWS Account** with Bedrock access
- **Google Cloud Project** with Docs API enabled
- **Tavily API Key** for web search

## Installation

### 1. MCP Server Setup

```bash
cd MCP_Server
npm install
```

Create `.env` file in `MCP_Server/`:
```env
# Google OAuth2 credentials
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REFRESH_TOKEN=your_refresh_token
```

### 2. AI Agent Setup

```bash
cd AI_Agent
pip install -r requirements.txt
```

Create `.env` file in `AI_Agent/`:
```env
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# Tavily API Key
TAVILY_API_KEY=your_tavily_api_key
```

### 3. PDF Documents Setup

Place your PDF documents in the `AI_Agent/pdf_rag/` directory. The agent will automatically index them on first run.

## Quick Start

### Step 1: Start the MCP Server

```bash
cd MCP_Server
node server.js
```

Expected output:
```
MCP HTTP Server running on http://localhost:3000
MCP endpoint http://localhost:3000/mcp
```

### Step 2: Start the AI Agent

In a new terminal:
```bash
cd AI_Agent
python main.py
```

### Step 3: Ask Questions

```
You: What are the health insurance benefits available?
Agent: [Detailed response from Google Docs...]

You: What is the hybrid work policy?
Agent: [Response from PDF documents...]

You: What are the latest changes in labor laws?
Agent: [Response from web search...]

You: exit
```

## Use Cases

### 1. Health Insurance Queries
The agent retrieves information from Google Docs about:
- Policy overview and plan types
- Coverage features and benefits
- Eligibility requirements
- Enrollment process and steps
- Claims procedures
- Premiums and costs
- FAQs and tips
- Customer feedback

**Example:**
```
You: How do I enroll in the health insurance plan?
Agent: Based on the Corporate Health Insurance Guide, here's the enrollment process...
```

### 2. Hybrid Work Policy Questions
The agent searches PDF documents for:
- Work-from-home rules and guidelines
- Office attendance requirements
- Employee eligibility criteria
- Approval workflows
- Working hours and schedules
- Security and compliance
- Equipment usage policies
- Performance expectations

**Example:**
```
You: How many days per week can I work from home?
Agent: According to the Corporate Hybrid Work Policy...
```

### 3. Current Information Lookup
The agent searches the web for:
- Recent news and updates
- Regulatory changes
- Market trends
- Real-time information
- External resources

**Example:**
```
You: What are the recent changes in remote work regulations?
Agent: Based on current information from web search...
```

## Agent Tools

### Tool 1: Google Docs Reader (`read_google_doc`)
- **Source:** MCP Server → Google Docs API
- **Use Case:** Corporate health insurance information
- **Trigger:** Questions about health benefits, insurance, medical coverage

### Tool 2: PDF RAG Search (`search_pdf_documents`)
- **Source:** Local PDF documents with FAISS vector search
- **Use Case:** Corporate hybrid work policy
- **Trigger:** Questions about remote work, office attendance, workplace policies

### Tool 3: Web Search (`web_search`)
- **Source:** Tavily API
- **Use Case:** Current events and external information
- **Trigger:** Questions about news, recent updates, external topics

## Configuration

### AWS Bedrock Configuration

The agent uses Claude models via AWS Bedrock. Required:
1. AWS credentials with Bedrock access
2. Model access enabled for Claude
3. Region set to `us-east-1` or your preferred region

### Google API Setup

For MCP Server to access Google Docs:
1. Create a Google Cloud Project
2. Enable Google Docs API
3. Create OAuth2 credentials
4. Run `get_refresh_token.js` to obtain refresh token
5. Add credentials to `.env`

### Vector Store Configuration

PDF RAG uses:
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Store:** FAISS
- **Chunk Size:** 1000 characters
- **Overlap:** 200 characters

## API Reference

### MCP Server Endpoints

**POST /mcp**
- Main MCP protocol endpoint
- Supports `tools/list` and `tools/call` methods
- Returns JSON-RPC 2.0 responses

**Example Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "read_google_doc",
    "arguments": {
      "docId": "your-doc-id"
    }
  }
}
```

## Troubleshooting

### MCP Server Issues

**Server won't start:**
- Check if port 3000 is already in use: `lsof -i :3000`
- Verify Node.js version: `node --version`
- Check dependencies: `npm install`

**Google Docs access fails:**
- Verify credentials in `.env` file
- Check if Docs API is enabled in Google Cloud Console
- Refresh the OAuth token if expired

### AI Agent Issues

**Can't connect to MCP server:**
```
Error: Connection refused
```
- Ensure MCP server is running on port 3000
- Check network/firewall settings
- Verify MCP_SERVER_URL in configuration

**AWS Bedrock errors:**
```
Error: Access denied
```
- Verify AWS credentials are correct
- Check IAM permissions for Bedrock
- Confirm model access is granted

**PDF indexing fails:**
```
Error: No PDF files found
```
- Verify PDFs are in `AI_Agent/pdf_rag/` directory
- Check PDF file permissions
- Ensure sufficient memory for embeddings

**Web search fails:**
```
Error: Tavily API key not found
```
- Check TAVILY_API_KEY in `.env`
- Verify API key is valid
- Check API quota limits

## Development

### Adding New Tools to MCP Server

1. Create tool in `MCP_Server/tools/`:
```javascript
export function getMyTool() {
  return {
    name: "my_tool",
    description: "Tool description",
    inputSchema: {
      type: "object",
      properties: { /* params */ },
      required: []
    }
  };
}
```

2. Register in `tools/index.js`

### Adding New Tools to AI Agent

1. Create tool class in `AI_Agent/tools/`:
```python
from langchain.tools import BaseTool

class MyTool(BaseTool):
    name: str = "my_tool"
    description: str = "Tool description"
    
    def _run(self, query: str) -> str:
        # Implementation
        pass
```

2. Add to agent in `agent/agent.py`

### Customizing Agent Behavior

Edit the `system_prompt` in `AI_Agent/agent/agent.py` to:
- Modify response style
- Add new tool usage guidelines
- Change routing logic
- Add domain-specific instructions

## Testing

### Test MCP Server

```bash
cd MCP_Server
node test_connection.js
```

### Test AI Agent Tools Individually

```python
from tools.pdf_rag_tool import PDFRAGTool

tool = PDFRAGTool(pdf_directory="./pdf_rag")
result = tool._run("What is the hybrid work policy?")
print(result)
```

## Performance Optimization

- **Connection Pooling:** MCP client reuses connections
- **Vector Store Caching:** RAG tool caches embeddings
- **Lazy Initialization:** Tools initialize on first use
- **Streaming:** Real-time response generation
- **Batch Processing:** Efficient document chunking

## Security Best Practices

- ✅ Store credentials in `.env` files (never commit to Git)
- ✅ Use IAM roles for AWS when possible
- ✅ Implement rate limiting in production
- ✅ Validate all user inputs
- ✅ Use HTTPS in production environments
- ✅ Rotate API keys regularly
- ✅ Monitor API usage and logs

## Deployment

### Production Checklist

- [ ] Set up environment variables securely
- [ ] Configure HTTPS/TLS for MCP server
- [ ] Implement authentication and authorization
- [ ] Set up logging and monitoring
- [ ] Configure rate limiting
- [ ] Set up backup for vector stores
- [ ] Document disaster recovery procedures
- [ ] Configure auto-scaling if needed

## Monitoring

Key metrics to track:
- MCP server response times
- Agent query processing time
- Tool execution success rates
- API quota usage (AWS Bedrock, Tavily)
- Vector store query performance
- Error rates and types

## Dependencies

### MCP Server (Node.js)
- `@modelcontextprotocol/sdk` - MCP implementation
- `express` - Web server
- `googleapis` - Google APIs client
- `cors` - CORS middleware
- `dotenv` - Environment variables

### AI Agent (Python)
- `langchain` - LangChain framework
- `langchain-aws` - AWS Bedrock integration
- `boto3` - AWS SDK
- `faiss-cpu` - Vector store
- `pypdf` - PDF processing
- `tavily-python` - Web search
- `sentence-transformers` - Embeddings

## Contributing

When adding new features:
1. Follow existing code structure
2. Add appropriate error handling
3. Update documentation
4. Test thoroughly before deployment

## Known Limitations

- MCP server currently supports only Google Docs
- PDF RAG limited to local documents
- Web search depends on Tavily API availability
- AWS Bedrock region availability varies

## Future Enhancements

- [ ] Add support for Google Sheets in MCP server
- [ ] Implement conversation history/memory
- [ ] Add multi-language support
- [ ] Create web UI for the agent
- [ ] Add support for more document types
- [ ] Implement user authentication
- [ ] Add analytics dashboard

## Support

For issues or questions:
- Check troubleshooting section
- Review logs in terminal output
- Verify environment configuration
- Test components individually

## License

ISC

## Author

Presidio Network Solutions - AI Training Week 4

---

## Quick Reference Commands

```bash
# Start MCP Server
cd MCP_Server && node server.js

# Start AI Agent
cd AI_Agent && python main.py

# Install MCP Server dependencies
cd MCP_Server && npm install

# Install AI Agent dependencies
cd AI_Agent && pip install -r requirements.txt

# Test MCP connection
cd MCP_Server && node test_connection.js

# Check MCP server status
curl http://localhost:3000/mcp
```
