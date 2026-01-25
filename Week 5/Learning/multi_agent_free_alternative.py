"""
Multi-Agent System with FREE alternatives to OpenAI
Uses Ollama (local) or other free API services
"""

from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
import operator


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


class FreeMultiAgentSystem:
    """
    Multi-agent system using FREE alternatives
    
    Options:
    1. Ollama (local, completely free) - RECOMMENDED
    2. Mock/Simulation mode for testing
    """
    
    def __init__(self, use_ollama: bool = True, model_name: str = "llama2"):
        """
        Initialize the multi-agent system with free alternatives
        
        Args:
            use_ollama: Use Ollama local models (requires Ollama installation)
            model_name: Model to use with Ollama (llama2, mistral, codellama, etc.)
        """
        self.use_ollama = use_ollama
        
        if use_ollama:
            # Use Ollama for local, free LLM
            self.llm = ChatOllama(model=model_name, temperature=0.7)
            print(f"✅ Using Ollama with model: {model_name}")
        else:
            # Simulation mode
            self.llm = None
            print("⚠️  Running in SIMULATION mode (no actual LLM)")
        
        self.graph = self._build_graph()
    
    def _simulate_response(self, prompt: str, role: str) -> str:
        """Simulate LLM response for testing without API"""
        responses = {
            "researcher": f"""
            SIMULATED RESEARCH RESPONSE:
            This is a simulated research output for: {prompt[:100]}
            
            Key findings:
            1. Topic is relevant and important
            2. Multiple aspects need to be considered
            3. Current trends show significant interest
            
            [This is a simulation - install Ollama for real responses]
            """,
            "analyst": f"""
            SIMULATED ANALYSIS RESPONSE:
            Analysis of the provided research.
            
            Key insights:
            - Pattern 1: Increasing relevance
            - Pattern 2: Multiple stakeholders involved
            - Conclusion: Requires further investigation
            
            [This is a simulation - install Ollama for real responses]
            """,
            "writer": f"""
            SIMULATED FINAL REPORT:
            
            Executive Summary:
            This report covers the topic in detail based on research and analysis.
            
            Introduction:
            The topic is of significant importance...
            
            Main Findings:
            - Finding 1: Important discovery
            - Finding 2: Key insight
            
            Conclusion:
            Based on the analysis, we recommend...
            
            [This is a simulation - install Ollama for real responses]
            """
        }
        return responses.get(role, "Simulated response")
    
    def researcher_agent_node(self, state: AgentState) -> AgentState:
        """Researcher Agent Node"""
        print("\n🔍 Researcher Agent is working...")
        
        prompt = f"Research the following topic: {state['task']}"
        
        if self.use_ollama:
            response = self.llm.invoke(prompt)
            research_output = response.content if hasattr(response, 'content') else str(response)
        else:
            research_output = self._simulate_response(prompt, "researcher")
        
        print(f"Research completed: {len(research_output)} characters")
        
        return {
            **state,
            "research_output": research_output,
            "messages": state["messages"] + [AIMessage(content="Researcher completed")],
            "next_agent": "analyst"
        }
    
    def analyst_agent_node(self, state: AgentState) -> AgentState:
        """Analyst Agent Node"""
        print("\n📊 Analyst Agent is working...")
        
        prompt = f"Analyze this research:\n\n{state['research_output']}"
        
        if self.use_ollama:
            response = self.llm.invoke(prompt)
            analysis_output = response.content if hasattr(response, 'content') else str(response)
        else:
            analysis_output = self._simulate_response(prompt, "analyst")
        
        print(f"Analysis completed: {len(analysis_output)} characters")
        
        return {
            **state,
            "analysis_output": analysis_output,
            "messages": state["messages"] + [AIMessage(content="Analyst completed")],
            "next_agent": "writer"
        }
    
    def writer_agent_node(self, state: AgentState) -> AgentState:
        """Writer Agent Node"""
        print("\n✍️  Writer Agent is working...")
        
        prompt = f"""Create a report based on:
        
        RESEARCH: {state['research_output']}
        ANALYSIS: {state['analysis_output']}
        """
        
        if self.use_ollama:
            response = self.llm.invoke(prompt)
            final_report = response.content if hasattr(response, 'content') else str(response)
        else:
            final_report = self._simulate_response(prompt, "writer")
        
        print(f"Report completed: {len(final_report)} characters")
        
        return {
            **state,
            "final_report": final_report,
            "messages": state["messages"] + [AIMessage(content="Writer completed")],
            "next_agent": "end"
        }
    
    def route_agent(self, state: AgentState) -> str:
        """Router function"""
        next_agent = state.get("next_agent", "researcher")
        if next_agent == "end":
            return END
        return next_agent
    
    def _build_graph(self) -> StateGraph:
        """Build the workflow graph"""
        workflow = StateGraph(AgentState)
        
        workflow.add_node("researcher", self.researcher_agent_node)
        workflow.add_node("analyst", self.analyst_agent_node)
        workflow.add_node("writer", self.writer_agent_node)
        
        workflow.set_entry_point("researcher")
        
        workflow.add_conditional_edges(
            "researcher",
            self.route_agent,
            {"analyst": "analyst", END: END}
        )
        
        workflow.add_conditional_edges(
            "analyst",
            self.route_agent,
            {"writer": "writer", END: END}
        )
        
        workflow.add_conditional_edges(
            "writer",
            self.route_agent,
            {END: END}
        )
        
        return workflow.compile()
    
    def run(self, task: str) -> dict:
        """Run the multi-agent system"""
        print(f"\n{'='*60}")
        print("🚀 Starting FREE Multi-Agent System")
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
        
        final_state = self.graph.invoke(initial_state)
        
        print(f"\n{'='*60}")
        print("✅ Multi-Agent System Completed")
        print(f"{'='*60}\n")
        
        return final_state


def main():
    """Example usage"""
    print("""
╔════════════════════════════════════════════════════════════╗
║     FREE Multi-Agent System - No API Key Required!         ║
╚════════════════════════════════════════════════════════════╝

Choose your mode:
1. Ollama (local, free) - RECOMMENDED
   - Install: https://ollama.ai/
   - Run: ollama pull llama2
   
2. Simulation mode (for testing structure only)

""")
    
    mode = input("Enter choice (1 or 2): ").strip()
    
    if mode == "1":
        print("\n🔧 Checking Ollama availability...")
        try:
            system = FreeMultiAgentSystem(use_ollama=True, model_name="llama2")
            print("✅ Ollama is ready!")
        except Exception as e:
            print(f"❌ Ollama not available: {e}")
            print("\nInstall Ollama:")
            print("1. Visit: https://ollama.ai/")
            print("2. Download and install")
            print("3. Run: ollama pull llama2")
            return
    else:
        system = FreeMultiAgentSystem(use_ollama=False)
    
    # Run with a task
    task = "The benefits of renewable energy"
    result = system.run(task)
    
    # Display results
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    
    print("\n✍️  FINAL REPORT:")
    print("-" * 60)
    print(result["final_report"])


if __name__ == "__main__":
    main()
