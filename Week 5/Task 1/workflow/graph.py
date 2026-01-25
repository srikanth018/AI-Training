"""
LangGraph Workflow for Multi-Agent Support System
Orchestrates the flow between Supervisor, IT Agent, and Finance Agent
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from agents import create_supervisor_agent, create_it_agent, create_finance_agent


class WorkflowState(TypedDict):
    """State for the multi-agent workflow"""
    query: str
    category: str
    reasoning: str
    response: str
    error: str


class MultiAgentWorkflow:
    """Multi-agent workflow using LangGraph"""
    
    def __init__(self):
        """Initialize the workflow"""
        # Initialize agents
        self.supervisor = create_supervisor_agent()
        self.it_agent = create_it_agent()
        self.finance_agent = create_finance_agent()
        
        # Build workflow graph
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create workflow graph
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("supervisor", self._supervisor_node)
        workflow.add_node("it_agent", self._it_agent_node)
        workflow.add_node("finance_agent", self._finance_agent_node)
        
        # Set entry point
        workflow.set_entry_point("supervisor")
        
        # Add conditional edges from supervisor
        workflow.add_conditional_edges(
            "supervisor",
            self._route_decision,
            {
                "IT": "it_agent",
                "FINANCE": "finance_agent"
            }
        )
        
        # Add edges to end
        workflow.add_edge("it_agent", END)
        workflow.add_edge("finance_agent", END)
        
        return workflow
    
    def _supervisor_node(self, state: WorkflowState) -> WorkflowState:
        """Supervisor node - routes queries"""
        
        try:
            decision = self.supervisor.route_query(state["query"])
            state["category"] = decision["category"]
            state["reasoning"] = decision["reasoning"]
            
            print(f"Classification: {decision['category']}")
            print(f"Reasoning: {decision['reasoning']}")
            print(f"Routing to {decision['category']} Agent...")
        
        except Exception as e:
            state["error"] = f"Supervisor error: {str(e)}"
            state["category"] = "IT"  # Default fallback
        
        return state
    
    def _it_agent_node(self, state: WorkflowState) -> WorkflowState:
        """IT Agent node - handles IT queries"""
        print("IT AGENT ACTIVATED")
        
        try:
            response = self.it_agent.process_query(state["query"])
            state["response"] = response
        
        except Exception as e:
            state["error"] = f"IT Agent error: {str(e)}"
            state["response"] = "I apologize, but I encountered an error processing your IT query."
        
        return state
    
    def _finance_agent_node(self, state: WorkflowState) -> WorkflowState:
        """Finance Agent node - handles Finance queries"""
        print("FINANCE AGENT ACTIVATED")
        
        try:
            response = self.finance_agent.process_query(state["query"])
            state["response"] = response
        
        except Exception as e:
            state["error"] = f"Finance Agent error: {str(e)}"
            state["response"] = "I apologize, but I encountered an error processing your Finance query."
        
        return state
    
    def _route_decision(self, state: WorkflowState) -> Literal["IT", "FINANCE"]:
        """Determine which agent to route to"""
        return state.get("category", "IT")
    
    def run(self, query: str) -> dict:
        """
        Run the workflow with a user query
        
        Args:
            query: User's question
            
        Returns:
            Final state with response
        """
        # Initialize state
        initial_state = {
            "query": query,
            "category": "",
            "reasoning": "",
            "response": "",
            "error": ""
        }
        
        # Run workflow
        final_state = self.app.invoke(initial_state)
        
        return final_state


def create_workflow() -> MultiAgentWorkflow:
    """Factory function to create workflow"""
    return MultiAgentWorkflow()
