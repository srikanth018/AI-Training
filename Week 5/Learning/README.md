# Multi-Agent System with LangGraph and LangChain

A sophisticated multi-agent system built with LangGraph and LangChain that demonstrates collaborative AI agent workflows.

## 🎯 Overview

This system implements three specialized agents that work together:

1. **🔍 Researcher Agent** - Gathers comprehensive information about a topic
2. **📊 Analyst Agent** - Analyzes the research data and extracts insights
3. **✍️ Writer Agent** - Creates a final report based on research and analysis

## 🏗️ Architecture

The system uses LangGraph to orchestrate the workflow:

```
┌─────────────┐      ┌──────────┐      ┌────────┐
│ Researcher  │─────▶│ Analyst  │─────▶│ Writer │
└─────────────┘      └──────────┘      └────────┘
```

Each agent receives the previous agent's output and builds upon it, creating a collaborative workflow.

## 📋 Features

- **State Management**: Shared state across all agents using TypedDict
- **Sequential Processing**: Each agent builds on the previous agent's work
- **Conditional Routing**: Smart routing between agents using LangGraph
- **Modular Design**: Easy to add or modify agents
- **Comprehensive Logging**: Track agent progress in real-time

## 🚀 Setup

### 1. Install Dependencies

Dependencies are already installed:
- `langgraph`
- `langchain`
- `langchain-openai`
- `langchain-community`
- `python-dotenv`

### 2. Configure API Key

Create a `.env` file with your OpenAI API key:

```bash
cp .env.example .env
```

Then edit `.env` and add your API key:

```
OPENAI_API_KEY=your_actual_api_key_here
```

## 💻 Usage

### Basic Usage

Run the main script:

```bash
python multi_agent_system.py
```

### Custom Usage

```python
from multi_agent_system import MultiAgentSystem

# Initialize the system
system = MultiAgentSystem(temperature=0.7)

# Run with your task
task = "The future of renewable energy"
result = system.run(task)

# Access outputs
print(result["research_output"])
print(result["analysis_output"])
print(result["final_report"])
```

## 🔧 Customization

### Add New Agents

1. Create a new agent method:

```python
def custom_agent(self, state: AgentState) -> AgentState:
    print("\n🤖 Custom Agent is working...")
    # Your agent logic here
    return {
        **state,
        "custom_output": "your output",
        "messages": state["messages"] + ["Custom: Completed task"],
        "next_agent": "next_agent_name"
    }
```

2. Add the agent to the graph:

```python
workflow.add_node("custom", self.custom_agent)
```

3. Update routing logic in `route_agent` and edges

### Modify Agent Behavior

Each agent uses a system prompt that defines its role. Modify the `SystemMessage` content in each agent method to change behavior.

### Change LLM Model

```python
system = MultiAgentSystem(
    model_name="gpt-4",  # or "gpt-4-turbo", etc.
    temperature=0.5
)
```

## 📊 Example Output

When you run the system, you'll see:

```
🚀 Starting Multi-Agent System
📋 Task: The impact of artificial intelligence on healthcare in 2024

🔍 Researcher Agent is working...
Research completed: 1234 characters

📊 Analyst Agent is working...
Analysis completed: 1567 characters

✍️ Writer Agent is working...
Report completed: 2345 characters

✅ Multi-Agent System Completed
```

## 🎓 Key Concepts

### LangGraph StateGraph
- Manages the workflow and state transitions
- Provides conditional routing between agents
- Ensures proper execution order

### Agent State
- Shared dictionary that passes information between agents
- Contains task, outputs, messages, and routing info
- Updated by each agent as they complete their work

### Conditional Edges
- Smart routing based on agent output
- Determines which agent runs next
- Can terminate the workflow when complete

## 🤝 Contributing

Feel free to extend this system with:
- Additional agents (validators, editors, etc.)
- Parallel agent execution
- Agent collaboration patterns
- External tool integration
- Memory and context management

## 📝 License

This is an educational project for learning multi-agent systems with LangGraph and LangChain.
