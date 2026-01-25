import os
from typing import Optional
from langchain.tools import BaseTool
from tavily import TavilyClient


class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = (
        "Search the internet for current information, news, or any topic. "
        "Use this when you need real-time information, recent events, or "
        "information not available in documents. "
        "Input should be a clear search query."
    )
    
    tavily_api_key: Optional[str] = None
    client: Optional[TavilyClient] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def _get_client(self) -> TavilyClient:
        """Get or create Tavily client"""
        if self.client is None:
            # Get API key from environment or use provided one
            api_key = self.tavily_api_key or os.getenv("TAVILY_API_KEY")
            
            if not api_key:
                raise ValueError(
                    "Tavily API key not found. Set TAVILY_API_KEY environment variable "
                    "or provide tavily_api_key parameter."
                )
            
            self.client = TavilyClient(api_key=api_key)
        
        return self.client
    
    def _run(self, query: str) -> str:
        """Search the web using Tavily API"""
        try:
            client = self._get_client()
            
            # Perform search
            response = client.search(
                query=query,
                max_results=5,
                include_answer=True,
                include_raw_content=False
            )
            
            # Format the results
            result = ""
            
            # Add the AI-generated answer if available
            if response.get("answer"):
                result += f"**Summary Answer:**\n{response['answer']}\n\n"
            
            # Add search results
            results_list = response.get("results", [])
            
            if not results_list:
                return "No search results found for your query."
            
            result += "**Top Search Results:**\n\n"
            
            for i, item in enumerate(results_list, 1):
                title = item.get("title", "No title")
                url = item.get("url", "")
                content = item.get("content", "No description available")
                
                result += f"**{i}. {title}**\n"
                result += f"URL: {url}\n"
                result += f"{content}\n\n"
            
            return result.strip()
            
        except ValueError as e:
            return f"Configuration error: {str(e)}"
        except Exception as e:
            return f"Error performing web search: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version"""
        return self._run(query)
