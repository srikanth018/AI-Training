# Multi-Agent Support System

A sophisticated multi-agent support system that intelligently routes user queries to specialized IT and Finance agents using LangGraph orchestration, LangChain agents, AWS Bedrock, FAISS vector database, and Tavily web search.

## 🎯 Overview

This system demonstrates a production-ready multi-agent architecture where:
- A **Supervisor Agent** classifies and routes queries
- Specialized **IT** and **Finance** agents handle domain-specific questions
- Each agent uses **RAG (FAISS)** for internal knowledge and **Tavily** for web search
- **LangGraph** orchestrates the entire workflow

## 🏗️ Architecture

```
User Query → Supervisor Agent (AWS Bedrock)
                    ↓
        ┌──────────┴──────────┐
        ↓                     ↓
    IT Agent            Finance Agent
    (AWS Bedrock)       (AWS Bedrock)
        ↓                     ↓
    ┌───┴───┐            ┌───┴───┐
    │ RAG   │            │ RAG   │
    │(FAISS)│            │(FAISS)│
    └───┬───┘            └───┬───┘
        │                     │
    ┌───┴───┐            ┌───┴───┐
    │ Web   │            │ Web   │
    │Search │            │Search │
    │(Tavily)│           │(Tavily)│
    └───────┘            └───────┘
```

## ✨ Features

- **🤖 Intelligent Routing**: Automatic query classification using Claude 3
- **📚 RAG Integration**: FAISS-based semantic search over internal documents
- **🌐 Web Search**: Tavily integration for external information
- **🔄 LangGraph Workflow**: State-based orchestration
- **⚡ ReAct Agents**: Reasoning and action framework
- **🛠️ Extensible**: Easy to add new agents and tools

## 📋 Prerequisites

- Python 3.9+
- AWS Account with Bedrock access (Claude 3 and Titan Embeddings)
- Tavily API key

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# - AWS_ACCESS_KEY_ID
# - AWS_SECRET_ACCESS_KEY
# - TAVILY_API_KEY
```

### 3. Run the System

```bash
python main.py
```

## 💬 Example Usage

```
🔵 Your Question: How do I set up the VPN?

[SUPERVISOR] Category: IT
[SUPERVISOR] Reasoning: Query about VPN setup is IT-related

[IT AGENT] Processing query...
[Tool: ReadITDocs] Searching internal documentation...

📝 Response:
To set up the company VPN:
1. Download Cisco AnyConnect from IT Portal
2. Install with administrator privileges
3. Configure with vpn.company.com
4. Use your company email and password with 2FA
...
```

```
🔵 Your Question: How do I file a reimbursement?

[SUPERVISOR] Category: FINANCE
[SUPERVISOR] Reasoning: Expense reimbursement is a finance procedure

[FINANCE AGENT] Processing query...
[Tool: ReadFinanceDocs] Searching finance documentation...

📝 Response:
To file an expense reimbursement:
1. Log in to finance.company.com
2. Upload receipts and expense details
3. Manager approves (1-2 business days)
4. Payment processed (5-7 business days)
...
```

## 🧪 Testing

Run component tests:

```bash
python test.py
```

This tests:
- RAG tool functionality
- Web search integration
- Supervisor routing logic

## 📁 Project Structure

```
Task 1/
├── agents/                    # Agent implementations
│   ├── supervisor_agent.py   # Query routing
│   ├── it_agent.py           # IT specialist
│   └── finance_agent.py      # Finance specialist
├── tools/                     # Tool implementations
│   ├── rag_tool.py           # FAISS RAG
│   └── web_search_tool.py    # Tavily search
├── workflow/                  # LangGraph workflow
│   └── graph.py              # Orchestration logic
├── documents/                 # Knowledge bases
│   ├── it_docs/              # IT documentation
│   └── finance_docs/         # Finance documentation
├── main.py                    # Application entry
└── requirements.txt           # Dependencies
```

## 🛠️ Technology Stack

- **LangChain** - Agent framework
- **LangGraph** - Multi-agent orchestration
- **AWS Bedrock** - LLM provider (Claude 3 Sonnet)
- **FAISS** - Vector database for RAG
- **Tavily** - Web search API
- **Python 3.9+** - Implementation language

## 🔧 Customization

### Add New Documents

Add `.txt` files to `documents/it_docs/` or `documents/finance_docs/`, then restart the application.

### Add New Agents

1. Create agent file in `agents/`
2. Define tools and prompt
3. Update workflow in `workflow/graph.py`

### Adjust Agent Behavior

Edit prompts in agent files:
- `agents/it_agent.py`
- `agents/finance_agent.py`
- `agents/supervisor_agent.py`

## 🎓 Learning Outcomes

This project demonstrates:
- Multi-agent system design
- LangGraph state management
- RAG implementation with FAISS
- Tool integration patterns
- AWS Bedrock usage
- Production-ready error handling

## 📝 Sample Queries

**IT Queries:**
- How do I set up the VPN?
- What software is approved for use?
- How do I request a new laptop?
- How do I reset my password?

**Finance Queries:**
- How do I file a reimbursement?
- Where can I find last month's budget report?
- When is payroll processed?
- How do I create a purchase order?
