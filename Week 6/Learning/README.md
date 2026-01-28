# LangChain Agent with AWS Bedrock

A simple demonstration of building an agent using LangChain with AWS Bedrock and tool calling capabilities.

## Prerequisites

- Python 3.8 or higher
- AWS account with Bedrock access
- AWS credentials configured (via AWS CLI or environment variables)

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure AWS credentials:**
   
   You can set up AWS credentials in several ways:
   
   **Option 1: AWS CLI**
   ```bash
   aws configure
   ```
   
   **Option 2: Environment variables**
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

3. **Enable Bedrock model access:**
   - Go to AWS Console → Bedrock → Model access
   - Request access to Claude 3 Sonnet model

## Features

This agent includes two simple tools:

1. **Calculator Tool**: Performs basic arithmetic operations (add, subtract, multiply, divide)
2. **Weather Tool**: Returns simulated weather data for cities

## Usage

Run the agent:
```bash
python bedrock_agent.py
```

The script will execute example queries demonstrating:
- Basic arithmetic calculations
- Weather information retrieval
- Multi-step reasoning with tool usage

## Customization

### Change the Bedrock Model

Edit the `model_id` in `bedrock_agent.py`:
```python
llm = ChatBedrock(
    client=bedrock_runtime,
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",  # Change this
    model_kwargs={
        "temperature": 0.7,
        "max_tokens": 2048
    }
)
```

Available models:
- `anthropic.claude-3-sonnet-20240229-v1:0` (Claude 3 Sonnet)
- `anthropic.claude-3-haiku-20240307-v1:0` (Claude 3 Haiku)
- `anthropic.claude-3-5-sonnet-20240620-v1:0` (Claude 3.5 Sonnet)

### Add Your Own Tools

Create a new tool using the `@tool` decorator:

```python
@tool
def my_custom_tool(param: str) -> str:
    """
    Description of what the tool does.
    
    Args:
        param: Description of parameter
    
    Returns:
        Description of return value
    """
    # Your tool logic here
    return "result"
```

Then add it to the tools list:
```python
tools = [calculator, get_weather, my_custom_tool]
```

### Change AWS Region

Update the region in `bedrock_agent.py`:
```python
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"  # Change to your region
)
```

## Interactive Mode

To use the agent interactively, modify the `main()` function:

```python
def main():
    agent = create_bedrock_agent()
    
    print("Agent initialized. Type 'quit' to exit.\n")
    
    while True:
        query = input("\nYour question: ")
        if query.lower() in ['quit', 'exit', 'q']:
            break
            
        try:
            response = agent.invoke({"input": query})
            print(f"\nAgent: {response['output']}")
        except Exception as e:
            print(f"\nError: {str(e)}")
```

## Troubleshooting

**Error: Access Denied**
- Ensure you have enabled model access in AWS Bedrock console
- Verify your AWS credentials have the necessary permissions

**Error: Model not found**
- Check that the model ID is correct
- Verify the model is available in your region

**Error: boto3 connection issues**
- Verify AWS credentials are properly configured
- Check your internet connection
- Ensure the region supports Bedrock

## Next Steps

- Add more sophisticated tools (API integrations, database queries, etc.)
- Implement memory for conversation context
- Add error handling and retry logic
- Create a web interface using Streamlit or Gradio
