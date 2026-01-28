# AWS Bedrock Web Scraper

A complete web scraping solution powered by AWS Bedrock Agent, Lambda functions, and a modern Vite React UI. This system allows users to crawl publicly accessible web pages through a conversational AI interface.

## 🏗️ Architecture

The system consists of three main components:

1. **AWS Bedrock Agent** - AI-powered conversational interface
2. **AWS Lambda Function** - Backend web scraping service
3. **Vite React UI** - Modern frontend chat interface

```
┌─────────────────┐
│   Vite React    │
│    Frontend     │
└────────┬────────┘
         │
         │ AWS SDK
         ▼
┌─────────────────┐
│  AWS Bedrock    │
│     Agent       │
└────────┬────────┘
         │
         │ Invokes
         ▼
┌─────────────────┐      ┌──────────────┐
│  Lambda Layer   │─────▶│   Lambda     │
│  (Dependencies) │      │   Function   │
└─────────────────┘      └──────┬───────┘
                                │
                                │ Scrapes
                                ▼
                         ┌──────────────┐
                         │   Website    │
                         └──────────────┘
```

---

## 📦 Components

### 1. AWS Bedrock Agent

The Bedrock Agent acts as an intelligent intermediary that interprets user requests and invokes the appropriate Lambda function for web crawling.

#### System Prompt

```
You are a web crawling assistant.

Your sole responsibility is to extract and crawl publicly accessible web pages using the provided crawling tool.

Rules you MUST follow:
1. Only respond to requests that clearly ask to crawl, scrape, or extract content from a website or URL.
2. Always extract the URL from the user's message before invoking the tool.
3. If no valid URL is present, respond with a short message asking the user to provide a valid website link.
4. Use the crawling tool exactly once per request unless explicitly asked otherwise.
5. Do NOT answer questions from your own knowledge. Always rely on the tool output.
6. Do NOT summarize, modify, or hallucinate content beyond what the tool returns.
7. If the tool fails, return a clear error message explaining that the website could not be crawled.
8. Do NOT attempt to browse private, authenticated, or restricted websites.
9. Do NOT perform actions outside web crawling (no Q&A, no reasoning, no recommendations).

Output format:
- If successful, return the crawled content clearly.
- If unsuccessful, return a concise error message.

You are not a general assistant.
You are a web crawler.
```

#### Model Configuration
- **Model**: Claude 3.7 (Anthropic)
- **Purpose**: Natural language understanding and tool invocation

#### Setup Instructions

1. **Create Bedrock Agent**:
   - Go to AWS Console → Amazon Bedrock → Agents
   - Click "Create Agent"
   - Name: `web-scraper-agent`
   - Model: `anthropic.claude-3-sonnet-20240229-v1:0` or `claude-3-7`
   - Add the system prompt above

2. **Create Action Group**:
   - Name: `crawl-website`
   - Lambda Function: Select your deployed Lambda function
   - API Schema: Function-based or API-based
   - Add function: `crawl_website`
   - Description: "Crawls a website and extracts its text content"
   - Parameters:
     - `query` (string, required): "URL or text containing URL to crawl"

3. **Deploy Agent**:
   - Create an alias (e.g., `prod`)
   - Note the Agent ID and Alias ID for frontend configuration

---

### 2. AWS Lambda Function

The Lambda function performs the actual web scraping using BeautifulSoup and Requests.

#### Files

- **`lambda_func.py`** - Main Lambda handler
- **`lambda-layer/`** - Python dependencies

#### Dependencies (Lambda Layer)

The Lambda layer includes the following packages:
- `requests==2.32.5` - HTTP library for web requests
- `beautifulsoup4==4.14.3` - HTML parsing and web scraping
- `certifi==2026.1.4` - SSL certificate validation
- `charset-normalizer==3.4.4` - Character encoding detection
- `idna==3.11` - Internationalized Domain Names support
- `soupsieve==2.8.3` - CSS selector library for BeautifulSoup
- `urllib3==2.6.3` - HTTP client
- `typing_extensions==4.15.0` - Typing extensions for Python

#### Key Features

- **URL Extraction**: Automatically extracts URLs from user input using regex
- **Intelligent Content Extraction**: 
  - Removes scripts, styles, headers, footers, and navigation
  - Optimized for Wikipedia and other content-heavy sites
  - Limits response to 4000 characters to avoid token limits
- **Multiple Input Formats**: Supports both function-based and API-based Bedrock Agent formats
- **Comprehensive Error Handling**:
  - Timeout errors
  - HTTP errors
  - Invalid URLs
  - General exceptions
- **User-Agent Spoofing**: Uses realistic browser headers to avoid blocking

#### Deployment Steps

1. **Create Lambda Layer**:
   ```bash
   cd lambda-layer
   zip -r web-scraper-layer.zip python
   ```

2. **Upload Layer to AWS**:
   - Go to AWS Lambda → Layers → Create Layer
   - Name: `web-scraper-dependencies`
   - Upload: `web-scraper-layer.zip`
   - Compatible runtimes: Python 3.11 or 3.12

3. **Create Lambda Function**:
   - Go to AWS Lambda → Create Function
   - Name: `web-scraper-function`
   - Runtime: Python 3.11 or 3.12
   - Upload code from `lambda_func.py`

4. **Attach Layer**:
   - In Lambda function configuration
   - Add layer → Custom layers
   - Select `web-scraper-dependencies`

5. **Configure Permissions**:
   - Ensure Lambda has basic execution role
   - Add permissions for Bedrock if needed

6. **Set Environment Variables** (if needed):
   - Timeout: 30 seconds or more
   - Memory: 256 MB minimum

#### Testing

You can test the Lambda function directly with:

```json
{
  "inputText": "Crawl https://www.wikipedia.org",
  "messageVersion": "1.0",
  "function": "crawl_website"
}
```

---

### 3. Vite React UI

A modern, responsive chat interface built with React and Vite for fast development and optimal performance.

#### Tech Stack

- **React 18.3** - Frontend framework
- **Vite 6.0** - Build tool and dev server
- **AWS SDK** - `@aws-sdk/client-bedrock-agent-runtime`
- **CSS Modules** - Component styling

#### Project Structure

```
web-scraper-ui/
├── src/
│   ├── App.jsx              # Main app component
│   ├── App.css              # Global styles
│   ├── main.jsx             # Entry point
│   ├── components/
│   │   ├── ChatInterface.jsx    # Chat UI component
│   │   └── ChatInterface.css    # Chat styles
│   └── services/
│       └── api.js               # Bedrock API integration
├── index.html               # HTML template
├── package.json             # Dependencies
├── vite.config.js          # Vite configuration
└── README.md               # UI-specific documentation
```

#### Key Features

- 🎨 Modern, responsive chat interface
- 🤖 Direct integration with AWS Bedrock Agent Runtime
- 💬 Session-based conversations with message history
- ⚡ Fast development with Vite HMR
- 🔄 Session management for multi-turn conversations
- 📝 Real-time streaming responses

#### Setup Instructions

1. **Navigate to UI Directory**:
   ```bash
   cd web-scraper-ui
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Configure Environment**:
   
   Create a `.env` file in `web-scraper-ui/`:
   ```env
   # AWS Credentials
   VITE_AWS_ACCESS_KEY_ID=your_access_key_id
   VITE_AWS_SECRET_ACCESS_KEY=your_secret_access_key
   VITE_AWS_SESSION_TOKEN=your_session_token  # Optional for temporary credentials

   # Bedrock Agent Configuration
   VITE_BEDROCK_AGENT_ID=your_bedrock_agent_id
   VITE_BEDROCK_AGENT_ALIAS_ID=your_bedrock_agent_alias_id
   ```

   **⚠️ Security Notes**:
   - Never commit `.env` to version control
   - For production, use AWS Cognito or IAM roles
   - Use temporary credentials when possible

4. **Update Region** (if needed):
   
   Edit `src/services/api.js`:
   ```javascript
   const AWS_CONFIG = {
     region: 'us-east-1', // Change to your region
     // ...
   };
   ```

5. **Run Development Server**:
   ```bash
   npm run dev
   ```
   
   Access at: `http://localhost:5173`

6. **Build for Production**:
   ```bash
   npm run build
   ```
   
   Output: `dist/` directory

---

## 🚀 Complete Setup Guide

### Prerequisites

- AWS Account with Bedrock access
- AWS CLI configured
- Node.js 18+ and npm
- Python 3.11+
- Basic knowledge of AWS services

### Step-by-Step Setup

#### Step 1: Deploy Lambda Function

```bash
# 1. Package Lambda Layer
cd lambda-layer
zip -r web-scraper-layer.zip python

# 2. Create Lambda Layer in AWS Console
# Upload web-scraper-layer.zip
# Note the Layer ARN

# 3. Create Lambda Function in AWS Console
# Upload lambda_func.py
# Attach the layer
# Set timeout to 30s and memory to 256MB
```

#### Step 2: Configure Bedrock Agent

```bash
# 1. Go to AWS Bedrock Console
# 2. Create a new Agent with:
#    - Name: web-scraper-agent
#    - Model: Claude 3.7 or Claude 3 Sonnet
#    - System prompt: (paste the prompt from above)
# 3. Create Action Group:
#    - Name: crawl-website
#    - Lambda: Select your Lambda function
#    - Add function with name: crawl_website
# 4. Deploy Agent and create alias
# 5. Note Agent ID and Alias ID
```

#### Step 3: Setup Frontend

```bash
# 1. Install dependencies
cd web-scraper-ui
npm install

# 2. Create .env file
cat > .env << EOF
VITE_AWS_ACCESS_KEY_ID=your_key
VITE_AWS_SECRET_ACCESS_KEY=your_secret
VITE_BEDROCK_AGENT_ID=your_agent_id
VITE_BEDROCK_AGENT_ALIAS_ID=your_alias_id
EOF

# 3. Run development server
npm run dev
```

#### Step 4: Test the System

1. Open browser to `http://localhost:5173`
2. Enter a query like: "Crawl https://www.wikipedia.org"
3. Wait for the agent to invoke Lambda and return results

---

## 💡 Usage Examples

### Basic Web Crawling

```
User: "Crawl https://www.example.com"
Agent: [Returns extracted text content from the website]
```

### Multiple URLs

```
User: "Please scrape https://www.wikipedia.org"
Agent: [Returns Wikipedia content]

User: "Now crawl https://www.github.com"
Agent: [Returns GitHub content]
```

### Error Handling

```
User: "Crawl https://invalid-site.xyz"
Agent: "HTTP Error: Failed to connect to the website"
```

---

## 🔧 Configuration Options

### Lambda Configuration

Edit `lambda_func.py` to customize:

```python
def crawl_website(url: str, max_chars: int = 4000) -> str:
    # Adjust max_chars to change content length
    # Default: 4000 characters
```

### Bedrock Agent Settings

- **Temperature**: Control response randomness (0.0 - 1.0)
- **Max Tokens**: Maximum response length
- **Stop Sequences**: Custom stop sequences

### UI Configuration

Edit `src/services/api.js`:

```javascript
// Change AWS region
const AWS_CONFIG = {
  region: 'us-west-2', // Your preferred region
};

// Customize session ID generation
const generateSessionId = () => {
  return `custom-session-${Date.now()}`;
};
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "No valid URL found"

**Cause**: URL not detected in user input

**Solution**: Ensure URL starts with `http://` or `https://`

#### 2. "Timeout: The website took too long"

**Cause**: Website not responding within 10 seconds

**Solution**: Increase timeout in Lambda or target a faster website

#### 3. Lambda Layer Not Found

**Cause**: Layer not attached to Lambda function

**Solution**: 
```bash
# Recreate layer
cd lambda-layer
zip -r web-scraper-layer.zip python
# Upload to AWS and attach to Lambda
```

#### 4. Bedrock Agent Not Responding

**Cause**: Incorrect Agent ID or credentials

**Solution**: Verify `.env` file has correct Agent ID and Alias ID

#### 5. CORS Errors in Frontend

**Cause**: Browser blocking AWS requests

**Solution**: AWS SDK handles CORS automatically, but ensure credentials are valid

---

## 📊 Performance Considerations

### Lambda Optimization

- **Cold Start**: First request may take 2-3 seconds
- **Memory**: 256 MB sufficient for most websites
- **Timeout**: 30 seconds recommended
- **Concurrent Executions**: Set reserved concurrency if needed

### Content Limits

- **Max Characters**: 4000 by default (configurable)
- **Bedrock Token Limit**: ~100K tokens for Claude 3.7
- **Lambda Response Size**: 6 MB max

### Cost Estimation

- **Lambda**: ~$0.20 per 1M requests + compute time
- **Bedrock**: Variable based on model and tokens
- **Data Transfer**: Negligible for typical usage

---

## 🔒 Security Best Practices

1. **Never Hardcode Credentials**: Use environment variables or AWS Secrets Manager
2. **Use IAM Roles**: For production, use IAM roles instead of access keys
3. **Implement Rate Limiting**: Prevent abuse of crawling functionality
4. **Validate URLs**: Add allowlist/blocklist for allowed domains
5. **Use VPC**: Deploy Lambda in VPC for additional security
6. **Enable CloudWatch Logging**: Monitor for suspicious activity
7. **Rotate Credentials**: Regularly rotate AWS access keys
8. **Use HTTPS**: Always use HTTPS for API calls

---

## 📚 Additional Resources

### AWS Documentation

- [AWS Bedrock Agents Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [AWS Lambda Python Guide](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
- [Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html)

### Libraries

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Library](https://requests.readthedocs.io/)
- [Vite Guide](https://vitejs.dev/guide/)
- [React Documentation](https://react.dev/)

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📝 License

This project is for educational purposes. Use responsibly and respect website terms of service when scraping.

---

## 🎯 Roadmap

Future enhancements:

- [ ] Add authentication system
- [ ] Implement URL allowlist/blocklist
- [ ] Support for JavaScript-rendered pages (Selenium/Playwright)
- [ ] Export crawled content to S3
- [ ] Add retry logic for failed requests
- [ ] Implement caching layer
- [ ] Support for multiple concurrent crawls
- [ ] Add content summarization with Bedrock
- [ ] Create mobile-responsive UI improvements
- [ ] Add download functionality for crawled content

---

## ❓ FAQ

**Q: Can this crawl JavaScript-heavy websites?**  
A: No, the current implementation only works with static HTML. For JS-rendered sites, you would need to integrate Selenium or Playwright.

**Q: Is this production-ready?**  
A: This is a training/educational project. For production use, add proper authentication, rate limiting, and error handling.

**Q: Can I crawl authenticated websites?**  
A: No, the current implementation only supports publicly accessible pages.

**Q: How do I change the AWS region?**  
A: Update the `region` field in `src/services/api.js` and ensure your Bedrock Agent is in the same region.

**Q: Why is the response limited to 4000 characters?**  
A: To prevent token limit issues with Bedrock. You can adjust `max_chars` in the Lambda function.

---

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review AWS CloudWatch logs for Lambda errors
3. Verify all configuration values in `.env`
4. Ensure AWS credentials have necessary permissions

---

**Built with ❤️ using AWS Bedrock, Lambda, and React**
