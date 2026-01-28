"""
Concert Booking Agent using LangChain and AWS Bedrock with Simple Guardrails
"""

import os
from typing import List
from langchain_aws import ChatBedrock
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
# from langchain_core.tools import Tool
from concert_tools import (
    search_concerts,
    check_venue_availability,
    get_ticket_prices,
    book_concert_tickets,
    get_artist_info,
    check_date_availability
)

from dotenv import load_dotenv

from langfuse import get_client
from langfuse.langchain import CallbackHandler

# Import simple guardrails
from guardrails_integration import create_guardrails

# Import trajectory evaluation
try:
    from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT
    TRAJECTORY_EVAL_AVAILABLE = True
except ImportError:
    TRAJECTORY_EVAL_AVAILABLE = False
    print("[AGENT] agentevals not installed. Trajectory evaluation disabled.")

load_dotenv()

# Initialize Langfuse client
langfuse = get_client()
 
# Initialize Langfuse CallbackHandler for Langchain (tracing)
langfuse_handler = CallbackHandler()


class ConcertBookingAgent:
    """Concert Booking Agent with specialized tools for searching and booking concerts"""
    
    def __init__(self, aws_region: str = "us-east-1", model_id: str = None, use_guardrails: bool = True, guardrail_threshold: float = 0.60, use_trajectory_eval: bool = False):
        """
        Initialize Concert Booking Agent
        
        Args:
            aws_region: AWS region for Bedrock
            model_id: Bedrock model ID
            use_guardrails: Whether to enable guardrails (default: True)
            guardrail_threshold: Similarity threshold for guardrails (default: 0.60)
            use_trajectory_eval: Whether to enable trajectory evaluation (default: False)
        """
        self.aws_region = aws_region
        self.model_id = model_id or os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
        self.use_guardrails = use_guardrails
        self.use_trajectory_eval = use_trajectory_eval
        
        # Initialize guardrails if enabled
        self.guardrails = None
        if self.use_guardrails:
            try:
                self.guardrails = create_guardrails(threshold=guardrail_threshold)
            except Exception as e:
                print(f"[AGENT] Guardrails initialization failed: {e}")
                print("[AGENT] Continuing without guardrails")
                self.use_guardrails = False
        
        # Initialize trajectory evaluator if enabled
        self.trajectory_evaluator = None
        if self.use_trajectory_eval and TRAJECTORY_EVAL_AVAILABLE:
            try:
                self.trajectory_evaluator = create_trajectory_llm_as_judge(
                    model=f"bedrock:{self.model_id}",
                    prompt=TRAJECTORY_ACCURACY_PROMPT,
                )
                print("[AGENT] Trajectory evaluation enabled")
            except Exception as e:
                print(f"[AGENT] Trajectory evaluation initialization failed: {e}")
                self.use_trajectory_eval = False
        
        # Initialize tools
        self.tools = self._create_tools()
        
        # Initialize LLM
        self.llm = ChatBedrock(
            model_id=self.model_id,
            region_name=self.aws_region,
            model_kwargs={
                "temperature": 0.7,
                "max_tokens": 2048,
            }
        )
        
        # Create agent
        self.agent_executor = self._create_agent()
    
    def _create_tools(self) -> List:
        """Create tools for Concert Booking agent"""
        return [
            search_concerts,
            check_venue_availability,
            get_ticket_prices,
            book_concert_tickets,
            get_artist_info,
            check_date_availability
        ]
    
    def _create_agent(self):
        """Create the Concert Booking agent using LangChain's create_agent"""
        
        # Bind tools to the model
        llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Create agent using the simplified pattern
        self.agent_executor = create_agent(
            llm_with_tools,
            self.tools
        )
        
        return self.agent_executor
    
    def process_query(self, query: str) -> str:
        """Process a user query with guardrails check"""
        guardrail_response = self.guardrails.run(query)
        
        if guardrail_response is not None:
            return guardrail_response
        
        return self._process_standard(query)
    
    def _process_standard(self, query: str) -> str:
        """Standard processing without guardrails"""
        try:
            # Create messages format for the agent
            result = self.agent_executor.invoke(
                {"messages": [HumanMessage(content=query)]},
                config={"callbacks": [langfuse_handler]}
            )
            
            # Evaluate trajectory if enabled
            if self.use_trajectory_eval and self.trajectory_evaluator:
                try:
                    evaluation = self.trajectory_evaluator(outputs=result["messages"])
                    score = evaluation.get('score', 'N/A')
                    print(f"[TRAJECTORY EVAL] Score: {score}")
                    if 'comment' in evaluation:
                        print(f"[TRAJECTORY EVAL] {evaluation['comment']}...")
                except Exception as e:
                    print(f"[TRAJECTORY EVAL]  Evaluation failed: {e}")
            
            # Extract the response from the messages
            if "messages" in result and len(result["messages"]) > 0:
                return result["messages"][-1].content
            return "I apologize, but I couldn't process your query."
        except Exception as e:
            return f"Error processing query: {str(e)}"


def create_bedrock_agent(use_guardrails: bool = True, use_trajectory_eval: bool = True) -> ConcertBookingAgent:
    """
    Factory function to create Concert Booking agent
    
    Args:
        use_guardrails: Enable guardrails integration (default: True)
        use_trajectory_eval: Enable trajectory evaluation (default: False)
    
    Returns:
        ConcertBookingAgent instance
    """
    return ConcertBookingAgent(use_guardrails=use_guardrails, use_trajectory_eval=use_trajectory_eval)


def main():
    """
    Main function to demonstrate the concert booking agent.
    """
    # Create the agent
    print("Initializing Concert Booking Agent...")
    agent = create_bedrock_agent()

    # Interactive mode
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
            print("Thank you for using Concert Booking Agent. Goodbye!")
            # langfuse.flush()
            break
        
        if not user_input:
            continue
        
        try:
            # Process query using the agent
            response = agent.process_query(user_input)
            print(f"\nAgent: {response}")
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again with a different query.")


if __name__ == "__main__":
    main()
