"""
LangChain Agent with AWS Bedrock and Tool Calling
This example demonstrates a simple agent using AWS Bedrock with custom tools.
"""

import boto3
from langchain_aws import ChatBedrock
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from langfuse import get_client
from langfuse.langchain import CallbackHandler
 
# Initialize Langfuse client
langfuse = get_client()
 
# Initialize Langfuse CallbackHandler for Langchain (tracing)
langfuse_handler = CallbackHandler()


# Define a simple calculator tool
@tool
def calculator(operation: str, a: float, b: float) -> float:
    """
    Perform basic arithmetic operations.
    
    Args:
        operation: The operation to perform (add, subtract, multiply, divide)
        a: First number
        b: Second number
    
    Returns:
        The result of the operation
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Error: Cannot divide by zero"
        return a / b
    else:
        return f"Error: Unknown operation {operation}"


# Define a weather tool (simulated)
@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a city.
    
    Args:
        city: The name of the city
    
    Returns:
        A description of the weather
    """
    # This is a simulated response - in reality, you'd call a weather API
    weather_data = {
        "New York": "Sunny, 72°F",
        "London": "Cloudy, 60°F",
        "Tokyo": "Rainy, 65°F",
        "Paris": "Partly cloudy, 68°F",
    }
    return weather_data.get(city, f"Weather data not available for {city}")


def create_bedrock_agent():
    """
    Create and configure a LangChain agent with AWS Bedrock.
    
    Returns:
        An agent instance
    """
    # Initialize AWS Bedrock client
    # Make sure you have AWS credentials configured
    # You can set them via environment variables or AWS CLI
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"  # Change to your preferred region
    )
    
    # Initialize the Bedrock LLM
    # Using Claude 3 Sonnet model
    llm = ChatBedrock(
        client=bedrock_runtime,
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={
            "temperature": 0.7,
            "max_tokens": 2048
        }
    )
    
    # Define the tools
    tools = [calculator, get_weather]
    
    # Bind tools to the model
    llm_with_tools = llm.bind_tools(tools)
    
    # Create the agent using create_agent
    agent_executor = create_agent(llm_with_tools, tools)
    
    return agent_executor


def main():
    """
    Main function to demonstrate the agent in action.
    """
    print("Initializing LangChain Agent with AWS Bedrock...\n")
    
    # Create the agent
    agent = create_bedrock_agent()
    
    # Example queries
    queries = [
        "What is 25 multiplied by 4?",
        "What's the weather like in Tokyo?",
        "Calculate 100 divided by 5, then add 10 to the result"
    ]
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        try:
            result = agent.invoke({
                "messages": [HumanMessage(content=query)],
            },
            config={"callbacks": [langfuse_handler]})
            
            # Extract the response from the messages
            if "messages" in result and len(result["messages"]) > 0:
                response_text = result["messages"][-1].content
            else:
                response_text = "I apologize, but I couldn't process your query."
            
            print(f"\nResponse: {response_text}")
        except Exception as e:
            print(f"\nError: {str(e)}")
    
    print("\n" + "="*60)
    print("Agent demonstration complete!")
    langfuse.flush() 


if __name__ == "__main__":
    main()
