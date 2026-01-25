"""
Advanced Multi-Agent System Example
Demonstrates more complex agent interactions and workflows
"""

from typing import Annotated, TypedDict, Sequence, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import operator
import os
from dotenv import load_dotenv

load_dotenv()


class AdvancedAgentState(TypedDict):
    """Extended state for advanced multi-agent system"""
    messages: Annotated[Sequence[str], operator.add]
    task: str
    research_output: str
    fact_check_output: str
    analysis_output: str
    final_report: str
    quality_score: int
    next_agent: str
    needs_revision: bool


class AdvancedMultiAgentSystem:
    """
    Advanced multi-agent system with fact-checking and quality control
    
    Workflow:
    1. Researcher - Gathers information
    2. Fact Checker - Validates research accuracy
    3. Analyst - Performs analysis (if facts check out)
    4. Writer - Creates report
    5. Quality Reviewer - Reviews and may request revisions
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.graph = self._build_graph()
    
    def researcher_agent(self, state: AdvancedAgentState) -> AdvancedAgentState:
        """Research specialist agent"""
        print("\n🔍 Researcher Agent is working...")
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a meticulous research specialist. 
            Gather accurate, verifiable information with sources when possible. 
            Focus on facts, statistics, and credible information."""),
            HumanMessage(content=f"Research: {state['task']}")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        
        return {
            **state,
            "research_output": response.content,
            "messages": ["Researcher: Research completed"],
            "next_agent": "fact_checker"
        }
    
    def fact_checker_agent(self, state: AdvancedAgentState) -> AdvancedAgentState:
        """Validates the research for accuracy and credibility"""
        print("\n✅ Fact Checker Agent is working...")
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a fact-checker. Review the research for:
            - Logical consistency
            - Potential inaccuracies
            - Credibility of claims
            Provide a brief assessment and flag any concerns."""),
            HumanMessage(content=f"Review this research:\n\n{state['research_output']}")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        
        return {
            **state,
            "fact_check_output": response.content,
            "messages": state["messages"] + ["Fact Checker: Verification completed"],
            "next_agent": "analyst"
        }
    
    def analyst_agent(self, state: AdvancedAgentState) -> AdvancedAgentState:
        """Analyzes verified research"""
        print("\n📊 Analyst Agent is working...")
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a data analyst. Analyze the verified research 
            and extract key insights, trends, and conclusions. Provide structured analysis."""),
            HumanMessage(content=f"""Research:\n{state['research_output']}
            
            Fact Check:\n{state['fact_check_output']}
            
            Provide detailed analysis.""")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        
        return {
            **state,
            "analysis_output": response.content,
            "messages": state["messages"] + ["Analyst: Analysis completed"],
            "next_agent": "writer"
        }
    
    def writer_agent(self, state: AdvancedAgentState) -> AdvancedAgentState:
        """Creates comprehensive report"""
        print("\n✍️  Writer Agent is working...")
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a professional writer. Create a comprehensive, 
            well-structured report that is engaging and informative. Include:
            - Executive summary
            - Main findings
            - Detailed analysis
            - Conclusions and recommendations"""),
            HumanMessage(content=f"""Create a report based on:
            
            RESEARCH:\n{state['research_output']}
            
            ANALYSIS:\n{state['analysis_output']}""")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        
        return {
            **state,
            "final_report": response.content,
            "messages": state["messages"] + ["Writer: Report completed"],
            "next_agent": "quality_reviewer"
        }
    
    def quality_reviewer_agent(self, state: AdvancedAgentState) -> AdvancedAgentState:
        """Reviews report quality and may request revisions"""
        print("\n⭐ Quality Reviewer Agent is working...")
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a quality reviewer. Rate the report on a scale of 1-10 
            based on clarity, completeness, and quality. If score is below 7, the report needs revision.
            Provide your rating as a number followed by brief feedback."""),
            HumanMessage(content=f"Review this report:\n\n{state['final_report']}")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        review = response.content
        
        # Extract score (simplified - in production, use more robust parsing)
        try:
            score = int(review.split()[0]) if review.split()[0].isdigit() else 8
        except:
            score = 8
        
        needs_revision = score < 7
        
        print(f"Quality Score: {score}/10")
        if needs_revision:
            print("⚠️  Report needs revision")
        
        return {
            **state,
            "quality_score": score,
            "needs_revision": needs_revision,
            "messages": state["messages"] + [f"Quality Reviewer: Score {score}/10"],
            "next_agent": "end" if not needs_revision else "writer"
        }
    
    def route_agent(self, state: AdvancedAgentState) -> str:
        """Router with conditional logic"""
        next_agent = state.get("next_agent", "researcher")
        
        if next_agent == "end":
            return END
        
        # If quality check fails, could route back to writer for revision
        if state.get("needs_revision", False) and next_agent == "writer":
            print("\n🔄 Routing back to writer for revision...")
        
        return next_agent
    
    def _build_graph(self) -> StateGraph:
        """Build the advanced workflow graph"""
        workflow = StateGraph(AdvancedAgentState)
        
        # Add all agent nodes
        workflow.add_node("researcher", self.researcher_agent)
        workflow.add_node("fact_checker", self.fact_checker_agent)
        workflow.add_node("analyst", self.analyst_agent)
        workflow.add_node("writer", self.writer_agent)
        workflow.add_node("quality_reviewer", self.quality_reviewer_agent)
        
        # Set entry point
        workflow.set_entry_point("researcher")
        
        # Define workflow edges
        workflow.add_conditional_edges(
            "researcher",
            self.route_agent,
            {"fact_checker": "fact_checker", END: END}
        )
        
        workflow.add_conditional_edges(
            "fact_checker",
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
            {"quality_reviewer": "quality_reviewer", END: END}
        )
        
        workflow.add_conditional_edges(
            "quality_reviewer",
            self.route_agent,
            {"writer": "writer", END: END}  # Can loop back for revision
        )
        
        return workflow.compile()
    
    def run(self, task: str) -> dict:
        """Run the advanced multi-agent system"""
        print(f"\n{'='*70}")
        print(f"🚀 Starting Advanced Multi-Agent System")
        print(f"📋 Task: {task}")
        print(f"{'='*70}")
        
        initial_state = {
            "messages": [],
            "task": task,
            "research_output": "",
            "fact_check_output": "",
            "analysis_output": "",
            "final_report": "",
            "quality_score": 0,
            "next_agent": "researcher",
            "needs_revision": False
        }
        
        final_state = self.graph.invoke(initial_state)
        
        print(f"\n{'='*70}")
        print(f"✅ System Completed - Quality Score: {final_state['quality_score']}/10")
        print(f"{'='*70}\n")
        
        return final_state


def main():
    """Run advanced example"""
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Please set OPENAI_API_KEY in .env file")
        return
    
    # Initialize advanced system
    system = AdvancedMultiAgentSystem(temperature=0.7)
    
    # Run with a task
    task = "The role of quantum computing in cybersecurity"
    result = system.run(task)
    
    # Display results
    print("\n" + "="*70)
    print("📊 FINAL RESULTS")
    print("="*70)
    
    print("\n✍️  FINAL REPORT:")
    print("-" * 70)
    print(result["final_report"])
    
    print(f"\n\n⭐ Quality Score: {result['quality_score']}/10")
    
    print("\n\n📝 Agent Activity Log:")
    print("-" * 70)
    for msg in result["messages"]:
        print(f"  • {msg}")


if __name__ == "__main__":
    main()
