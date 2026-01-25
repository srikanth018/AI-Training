"""
Web Search Tool using Tavily API
Provides external information retrieval capabilities
"""

from typing import Optional
from langchain_core.tools import Tool
from tavily import TavilyClient
import os


class WebSearchTool:
    """Web search tool using Tavily"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize web search tool
        
        Args:
            api_key: Tavily API key (if not provided, reads from env)
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("Tavily API key not found. Set TAVILY_API_KEY environment variable.")
        
        self.client = TavilyClient(api_key=self.api_key)
    
    def search(self, query: str, max_results: int = 3) -> str:
        """
        Search the web for information
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Formatted search results
        """
        print("\n[TOOL: WEB SEARCH] Searching external sources...")        
        try:
            # Perform search
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="basic"
            )
            
            results = response.get('results', [])
            
            if not results:
                return "No web search results found."
            
            # Format results
            formatted_results = []
            for i, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                content = result.get('content', 'No content')
                
                formatted_results.append(
                    f"--- Result {i} ---\n"
                    f"Title: {title}\n"
                    f"URL: {url}\n"
                    f"Content: {content}\n"
                )
            
            return "\n".join(formatted_results)
        
        except Exception as e:
            return f"Error performing web search: {str(e)}"
    
    def as_tool(self, name: str, description: str) -> Tool:
        """
        Convert to LangChain Tool
        
        Args:
            name: Tool name
            description: Tool description
            
        Returns:
            LangChain Tool instance
        """
        return Tool(
            name=name,
            func=self.search,
            description=description
        )


def create_web_search_tool(tool_name: str, tool_description: str) -> Tool:
    """
    Factory function to create a web search tool
    
    Args:
        tool_name: Name for the tool
        tool_description: Description for the tool
        
    Returns:
        LangChain Tool instance
    """
    web_search = WebSearchTool()
    return web_search.as_tool(name=tool_name, description=tool_description)
