import asyncio
import httpx
from mcp import ClientSession
from mcp.client.sse import sse_client

async def test_mcp_server():
    """Test the MCP server functionality"""
    server_url = "http://localhost:3000"
    
    print(f"Connecting to MCP server at {server_url}...")
    
    try:
        async with sse_client(f"{server_url}/sse") as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                print("Connected and initialized successfully!\n")
                
                # Test 1: List available tools
                print("=" * 50)
                print("TEST 1: Listing available tools")
                print("=" * 50)
                tools_result = await session.list_tools()
                for tool in tools_result.tools:
                    print(f"✓ Tool: {tool.name}")
                    print(f"  Description: {tool.description}")
                    print()
                
                # Test 2: Call weather tool
                print("=" * 50)
                print("TEST 2: Calling 'get_weather' tool")
                print("=" * 50)
                weather_result = await session.call_tool(
                    "get_weather",
                    arguments={"city": "London", "units": "celsius"}
                )
                for content in weather_result.content:
                    if hasattr(content, 'text'):
                        print(f"Result: {content.text}")
                print()
                
                print("Tests completed!")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
