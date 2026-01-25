"""
IT Agent - Handles all IT-related queries
Uses RAG tool for internal docs and web search for external sources
"""

from typing import List
from langchain_core.tools import Tool
from langchain_aws import ChatBedrock
from langchain.agents import create_agent
from tools import create_rag_tool, create_web_search_tool
import os


class ITAgent:
    """IT Support Agent with RAG and Web Search capabilities"""
    
    def __init__(self, aws_region: str = "us-east-1", model_id: str = None):
        """
        Initialize IT Agent
        
        Args:
            aws_region: AWS region for Bedrock
            model_id: Bedrock model ID
        """
        self.aws_region = aws_region
        self.model_id = model_id or os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
        
        # Initialize tools
        self.tools = self._create_tools()
        
        # Initialize LLM
        self.llm = ChatBedrock(
            model_id=self.model_id,
            region_name=self.aws_region,
            model_kwargs={
                "temperature": 0.1,
                "max_tokens": 1000,
            }
        )
        
        # Create agent
        self.agent_executor = self._create_agent()
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for IT agent"""
        
        # RAG tool for internal IT documentation
        it_rag_tool = create_rag_tool(
            document_dir="documents/it_docs",
            index_name="it_docs",
            tool_name="ReadITDocs",
            tool_description=(
                "Search internal IT documentation for information about VPN setup, "
                "approved software, laptop requests, password resets, and other IT policies. "
                "Use this tool FIRST before searching the web."
            )
        )
        
        # Web search tool for external IT information
        web_search_tool = create_web_search_tool(
            tool_name="WebSearch",
            tool_description=(
                "Search the web for external IT information, troubleshooting guides, "
                "or technical documentation not available in internal docs. "
                "Use this when internal docs don't have the answer."
            )
        )
        
        return [it_rag_tool, web_search_tool]
    
    def _create_agent(self):
        """Create the IT agent using LangChain's create_agent"""
        
        # Bind tools to the model
        llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Create agent using the simplified pattern
        self.agent_executor = create_agent(
            llm_with_tools,
            self.tools
        )
        
        return self.agent_executor
    
    def process_query(self, query: str) -> str:
        """
        Process an IT query
        
        Args:
            query: User's IT question
            
        Returns:
            Agent's response
        """
        print(f"\n[IT AGENT] Starting to process query...")
        
        try:
            # Create messages format for the agent
            from langchain_core.messages import HumanMessage
            
            result = self.agent_executor.invoke({
                "messages": [HumanMessage(content=query)]
            })
            
            # Extract the response from the messages
            if "messages" in result and len(result["messages"]) > 0:
                return result["messages"][-1].content
            return "I apologize, but I couldn't process your query."
        except Exception as e:
            return f"Error processing query: {str(e)}"


def create_it_agent() -> ITAgent:
    """Factory function to create IT agent"""
    return ITAgent()
