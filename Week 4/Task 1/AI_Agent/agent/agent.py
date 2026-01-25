from langchain.agents import create_agent
from llm.bedrock import get_bedrock_llm
from tools.mcp_client import ReadGoogleDocTool
from tools.pdf_rag_tool import PDFRAGTool
from tools.web_search_tool import WebSearchTool

def build_agent():
    llm = get_bedrock_llm()

    # Initialize MCP tools
    google_doc_tool = ReadGoogleDocTool(
        mcp_url="http://localhost:3000"
    )
    
    # Initialize RAG tool for PDF documents
    pdf_rag_tool = PDFRAGTool(
        pdf_directory="./pdf_rag"
    )
    
    # Initialize Web Search tool
    web_search_tool = WebSearchTool()

    tools = [google_doc_tool, pdf_rag_tool, web_search_tool]

    # Create agent using new API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt = (
            "You are an intelligent AI agent that can access multiple data sources related to company policies, "
            "employee benefits, and workplace guidelines.\n\n"
            "You can:\n"
            "1. Read Google Docs using the read_google_doc tool to extract and answer questions about Corporate Health Insurance, "
            "   including policy overview, plan types, coverage features, eligibility, enrollment process, claims, benefits, "
            "   premiums, FAQs, and employee tips.\n Also it has customer feedbacks about health insurance plans.\n"
            "2. Search PDF documents using the search_pdf_documents tool to answer questions about the company’s Corporate Hybrid Work Policy, "
            "   including work-from-home rules, office attendance requirements, eligibility, approval workflows, "
            "   working hours, security guidelines, equipment usage, leave alignment, performance expectations, "
            "   and compliance requirements.\n"
            "3. Search the internet using the web_search tool for current information, regulatory updates, "
            "   or topics not covered in internal company documents.\n\n"
            "Guidelines:\n"
            "- When a user provides a Google Doc ID or asks about health insurance or employee medical benefits, "
            "  always use the read_google_doc tool.\n"
            "- When a user asks about hybrid work arrangements, remote work rules, office presence, "
            "  or workplace policies stored as PDFs, use the search_pdf_documents tool.\n"
            "- When users ask about recent news, labor laws, market trends, or real-time information, "
            "  use the web_search tool.\n\n"
            "Response Style:\n"
            "- Provide clear, structured, and policy-aligned answers.\n"
            "- Summarize lengthy policy text when appropriate.\n"
            "- Highlight key rules, eligibility criteria, do’s and don’ts, and employee responsibilities.\n"
            "- Use simple language suitable for employees and managers."
        ),
        debug=False
    )

    return agent