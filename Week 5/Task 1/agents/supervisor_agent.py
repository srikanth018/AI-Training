"""
Supervisor Agent - Routes queries to appropriate specialist agents
Classifies user queries as IT or Finance
"""

from typing import Literal
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import os


class RouteDecision(BaseModel):
    """Route decision model"""
    category: Literal["IT", "FINANCE"] = Field(
        description="The category of the user query: IT or FINANCE"
    )
    reasoning: str = Field(
        description="Brief explanation of why this category was chosen"
    )


class SupervisorAgent:
    """Supervisor Agent that routes queries to specialist agents"""
    
    def __init__(self, aws_region: str = "us-east-1", model_id: str = None):
        """
        Initialize Supervisor Agent
        
        Args:
            aws_region: AWS region for Bedrock
            model_id: Bedrock model ID
        """
        self.aws_region = aws_region
        self.model_id = model_id or os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
        
        # Initialize LLM
        self.llm = ChatBedrock(
            model_id=self.model_id,
            region_name=self.aws_region,
            model_kwargs={
                "temperature": 0.0,  # Use deterministic routing
                "max_tokens": 500,
            }
        )
        
        # Create routing prompt
        self.routing_prompt = self._create_routing_prompt()
    
    def _create_routing_prompt(self) -> ChatPromptTemplate:
        """Create prompt for query classification"""
        
        system_message = """You are a Supervisor Agent responsible for routing employee queries to the appropriate department.

You must classify each query as either IT or FINANCE based on the content.

IT QUERIES include:
- VPN setup and connectivity issues
- Software installation and approval requests
- Hardware requests (laptops, monitors, etc.)
- Password resets and account access
- Network and technical issues
- Email and communication tools
- Security and antivirus questions
- General technical support

FINANCE QUERIES include:
- Expense reimbursement and claims
- Budget reports and financial statements
- Payroll questions and schedules
- Purchase orders and procurement
- Travel expense policies
- Invoice and payment questions
- Tax and compensation questions
- Financial procedures and policies

Analyze the user's query carefully and determine which category it belongs to.
Provide your reasoning for the classification."""

        human_message = """User Query: {query}

Classify this query as IT or FINANCE and explain your reasoning."""

        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", human_message)
        ])
    
    def route_query(self, query: str) -> dict:
        """
        Route a query to the appropriate agent
        
        Args:
            query: User's question
            
        Returns:
            Dictionary with 'category' and 'reasoning'
        """
        try:
            # Create structured output using LLM
            structured_llm = self.llm.with_structured_output(RouteDecision)
            
            # Format prompt
            prompt_value = self.routing_prompt.format_messages(query=query)
            
            # Get routing decision
            decision = structured_llm.invoke(prompt_value)
            
            return {
                "category": decision.category,
                "reasoning": decision.reasoning
            }
        
        except Exception as e:
            # Default to IT if classification fails
            print(f"Error in routing: {str(e)}")
            return {
                "category": "IT",
                "reasoning": f"Classification error, defaulting to IT: {str(e)}"
            }


def create_supervisor_agent() -> SupervisorAgent:
    """Factory function to create Supervisor agent"""
    return SupervisorAgent()
