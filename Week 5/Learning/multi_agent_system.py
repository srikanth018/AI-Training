"""
Multi-Agent System using LangGraph and LangChain
This system demonstrates a collaborative multi-agent workflow where:
- Researcher Agent: Gathers information and conducts research
- Analyst Agent: Analyzes the researched data
- Writer Agent: Creates a final report based on analysis

Uses LangChain's create_react_agent for proper agent creation.
"""

from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, END
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
import operator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Define tools for agents
@tool
def search_information(query: str) -> str:
    """Search for information about a topic. Useful for research."""
    return f"Searched information about: {query}"


@tool
def analyze_data(data: str) -> str:
    """Analyze the provided data and extract insights."""
    return f"Analyzed data: {data[:100]}..."


@tool
def format_report(content: str) -> str:
    """Format content into a professional report."""
    return f"Formatted report from: {content[:100]}..."


class AgentState(TypedDict):
    """State shared across all agents in the graph"""
    messages: Annotated[List[BaseMessage], operator.add]
    task: str
    research_output: str
    analysis_output: str
    final_report: str
    next_agent: str


class MultiAgentSystem:
    """Multi-agent system orchestrated by LangGraph using create_react_agent"""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7):
        """
        Initialize the multi-agent system
        
        Args:
            model_name: OpenAI model to use
            temperature: Model temperature for creativity
        """
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        
        # Create specialized agents using create_react_agent
        self.researcher = self._create_researcher_agent()
        self.analyst = self._create_analyst_agent()
        self.writer = self._create_writer_agent()
        
        self.graph = self._build_graph()
    
    def _create_researcher_agent(self):
        """Create a researcher agent with search tools"""
        tools = [search_information]
        
        # Create specialized model for researcher
        model = ChatOpenAI(
            model=self.llm.model_name,
            temperature=self.llm.temperature,
            max_tokens=1000,
            timeout=30
        )
        
        # Create agent with tools using create_agent
        agent = create_agent(model, tools=tools)
        return agent
    
    def _create_analyst_agent(self):
        """Create an analyst agent with analysis tools"""
        tools = [analyze_data]
        
        # Create specialized model for analyst
        model = ChatOpenAI(
            model=self.llm.model_name,
            temperature=self.llm.temperature,
            max_tokens=1000,
            timeout=30
        )
        
        # Create agent with tools using create_agent
        agent = create_agent(model, tools=tools)
        return agent
    
    def _create_writer_agent(self):
        """Create a writer agent with formatting tools"""
        tools = [format_report]
        
        # Create specialized model for writer
        model = ChatOpenAI(
            model=self.llm.model_name,
            temperature=self.llm.temperature,
            max_tokens=1500,
            timeout=30
        )
        
        # Create agent with tools using create_agent
        agent = create_agent(model, tools=tools)
        return agent
    
    def researcher_agent_node(self, state: AgentState) -> AgentState:
        """
        Researcher Agent Node: Gathers information about the task
        """
        print("\n🔍 Researcher Agent is working...")
        
        # Prepare input for the agent with system context
        system_context = """You are a research specialist. Gather comprehensive information 
        about the topic with key facts, statistics, and important details."""
        input_message = HumanMessage(content=f"{system_context}\n\nResearch the following topic: {state['task']}")
        
        # Invoke the researcher agent
        result = self.researcher.invoke({
            "messages": [input_message]
        })
        
        # Extract the final response
        research_output = ""
        for message in result["messages"]:
            if isinstance(message, AIMessage):
                research_output = message.content
        
        print(f"Research completed: {len(research_output)} characters")
        
        return {
            **state,
            "research_output": research_output,
            "messages": state["messages"] + [AIMessage(content=f"Researcher completed research on '{state['task']}'")],
            "next_agent": "analyst"
        }
    
    def analyst_agent_node(self, state: AgentState) -> AgentState:
        """
        Analyst Agent Node: Analyzes the research data
        """
        print("\n📊 Analyst Agent is working...")
        
        # Prepare input for the agent with system context
        system_context = """You are a data analyst. Analyze the research and extract 
        key insights, patterns, and conclusions."""
        input_message = HumanMessage(
            content=f"""{system_context}\n\nAnalyze the following research:
            
            {state['research_output']}
            
            Provide a detailed analysis with key insights and conclusions."""
        )
        
        # Invoke the analyst agent
        result = self.analyst.invoke({
            "messages": [input_message]
        })
        
        # Extract the final response
        analysis_output = ""
        for message in result["messages"]:
            if isinstance(message, AIMessage):
                analysis_output = message.content
        
        print(f"Analysis completed: {len(analysis_output)} characters")
        
        return {
            **state,
            "analysis_output": analysis_output,
            "messages": state["messages"] + [AIMessage(content="Analyst completed analysis of research data")],
            "next_agent": "writer"
        }
    
    def writer_agent_node(self, state: AgentState) -> AgentState:
        """
        Writer Agent Node: Creates final report based on research and analysis
        """
        print("\n✍️  Writer Agent is working...")
        
        # Prepare input for the agent with system context
        system_context = """You are a professional writer. Create a comprehensive, 
        well-structured report that is clear, engaging, and informative."""
        input_message = HumanMessage(
            content=f"""{system_context}\n\nCreate a comprehensive report based on the following:
            
            RESEARCH:
            {state['research_output']}
            
            ANALYSIS:
            {state['analysis_output']}
            
            Write a well-structured final report with an introduction, main findings, and conclusion."""
        )
        
        # Invoke the writer agent
        result = self.writer.invoke({
            "messages": [input_message]
        })
        
        # Extract the final response
        final_report = ""
        for message in result["messages"]:
            if isinstance(message, AIMessage):
                final_report = message.content
        
        print(f"Report completed: {len(final_report)} characters")
        
        return {
            **state,
            "final_report": final_report,
            "messages": state["messages"] + [AIMessage(content="Writer completed final report")],
            "next_agent": "end"
        }
    
    def route_agent(self, state: AgentState) -> str:
        """
        Router function to determine next agent
        """
        next_agent = state.get("next_agent", "researcher")
        
        if next_agent == "end":
            return END
        return next_agent
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow with agents created using create_react_agent
        """
        workflow = StateGraph(AgentState)
        
        # Add agent nodes (using the node wrappers)
        workflow.add_node("researcher", self.researcher_agent_node)
        workflow.add_node("analyst", self.analyst_agent_node)
        workflow.add_node("writer", self.writer_agent_node)
        
        # Set entry point
        workflow.set_entry_point("researcher")
        
        # Add edges with conditional routing
        workflow.add_conditional_edges(
            "researcher",
            self.route_agent,
            {
                "analyst": "analyst",
                END: END
            }
        )
        
        workflow.add_conditional_edges(
            "analyst",
            self.route_agent,
            {
                "writer": "writer",
                END: END
            }
        )
        
        workflow.add_conditional_edges(
            "writer",
            self.route_agent,
            {
                END: END
            }
        )
        
        return workflow.compile()
    
    def run(self, task: str) -> dict:
        """
        Run the multi-agent system on a given task
        
        Args:
            task: The task/topic for the agents to work on
            
        Returns:
            Final state with all outputs
        """
        print(f"\n{'='*60}")
        print("🚀 Starting Multi-Agent System (using create_agent)")
        print(f"📋 Task: {task}")
        print(f"{'='*60}")
        
        initial_state = {
            "messages": [],
            "task": task,
            "research_output": "",
            "analysis_output": "",
            "final_report": "",
            "next_agent": "researcher"
        }
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        print(f"\n{'='*60}")
        print("✅ Multi-Agent System Completed")
        print(f"{'='*60}\n")
        
        return final_state


def main():
    """Example usage of the multi-agent system"""
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
        return
    
    # Initialize the system (agents created with create_agent)
    print("\n🔧 Initializing Multi-Agent System...")
    print("   Using LangChain's create_agent for each agent")
    system = MultiAgentSystem(temperature=0.7)
    
    # Define a task
    task = "The impact of artificial intelligence on healthcare in 2024"
    
    # Run the system
    result = system.run(task)
    
    # Display results
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    
    print("\n🔍 RESEARCH OUTPUT:")
    print("-" * 60)
    print(result["research_output"])
    
    print("\n\n📊 ANALYSIS OUTPUT:")
    print("-" * 60)
    print(result["analysis_output"])
    
    print("\n\n✍️  FINAL REPORT:")
    print("-" * 60)
    print(result["final_report"])
    
    print("\n\n📝 Agent Activity Log:")
    print("-" * 60)
    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            print(f"  • {msg.content}")


if __name__ == "__main__":
    main()
