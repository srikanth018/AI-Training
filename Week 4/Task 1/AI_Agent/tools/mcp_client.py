import requests
import json
import re
import threading
import time
from typing import Optional, Dict, Any
from langchain.tools import BaseTool

class MCPClient:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.session_id: Optional[str] = None
        self.messages: Dict[int, Any] = {}
        self.request_counter = 0
        self.sse_thread = None
        self.connected = False
        # Don't connect in __init__, do it lazily

    def _initialize(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "langchain-mcp-client",
                    "version": "0.1.0"
                }
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }

        r = requests.post(f"{self.base_url}/mcp", json=payload, headers=headers, timeout=5, stream=True)
        if r.status_code != 200:
            raise Exception(f"MCP initialize failed: {r.text}")
        
        # Extract session ID from headers or response
        if 'x-mcp-session-id' in r.headers:
            self.session_id = r.headers['x-mcp-session-id']
            print(f"[MCP] Got session ID from header: {self.session_id}")
        elif 'mcp-session-id' in r.headers:
            self.session_id = r.headers['mcp-session-id']
            print(f"[MCP] Got session ID from header: {self.session_id}")
        else:
            # Read SSE response to confirm initialization
            for line in r.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith('data:'):
                        data = decoded.split(':', 1)[1].strip()
                        try:
                            init_data = json.loads(data)
                            if 'result' in init_data:
                                print(f"[MCP] Initialized successfully")
                                self.session_id = "stateless"
                                break
                        except json.JSONDecodeError:
                            pass

    
    def _ensure_connected(self):
        """Ensure connection is established before making requests"""
        if not self.connected:
            self._connect()
    
    def _connect(self):
        if self.sse_thread and self.sse_thread.is_alive():
            return

        print("[MCP] Initializing server...")
        self._initialize()

        if self.session_id is None:
            raise Exception("Failed to get session ID from initialize")

        print("[MCP] Opening SSE stream...")

        def listen_sse():
            headers = {
                "Accept": "application/json, text/event-stream"
            }
            if self.session_id:
                headers['mcp-session-id'] = self.session_id
            
            try:
                with requests.get(f"{self.base_url}/mcp", stream=True, headers=headers) as r:
                    print(f"[MCP] SSE connected with status: {r.status_code}")
                    for line in r.iter_lines(decode_unicode=True):
                        if not line:
                            continue

                        if line.startswith("data:"):
                            try:
                                msg = json.loads(line[5:].strip())
                                if "id" in msg:
                                    self.messages[msg["id"]] = msg
                                    print(f"[MCP] Received response for request ID {msg['id']}")
                            except Exception as e:
                                print(f"[MCP] Error parsing message: {e}")
            except Exception as e:
                print(f"[MCP] SSE connection ended: {e}")

        self.sse_thread = threading.Thread(target=listen_sse, daemon=True)
        self.sse_thread.start()

        # Wait to ensure stream is live
        time.sleep(1)
        self.connected = True
        print("[MCP] Connected and ready")

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call an MCP tool and return the result"""
        self._ensure_connected()
        
        if self.session_id is None:
            return "Error: Not connected to MCP server"
        
        self.request_counter += 1
        request_id = self.request_counter
        
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/event-stream'
            }
            if self.session_id:
                headers['mcp-session-id'] = self.session_id
            
            print(f"[MCP] Calling tool: {tool_name}")
            response = requests.post(
                f'{self.base_url}/mcp',
                headers=headers,
                json=payload,
                timeout=10,
                stream=True
            )
            
            # Read SSE response for result
            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith('data:'):
                        data = decoded.split(':', 1)[1].strip()
                        try:
                            result = json.loads(data)
                            if 'result' in result:
                                content = result['result'].get('content', [])
                                
                                # Extract text content
                                text_parts = []
                                for item in content:
                                    if item.get('type') == 'text':
                                        text_parts.append(item.get('text', ''))
                                
                                return '\n'.join(text_parts) if text_parts else str(result['result'])
                        except json.JSONDecodeError:
                            pass
            
            return f"Error: No valid response received from MCP server for tool '{tool_name}'"
                
        except Exception as e:
            return f"Error calling MCP tool: {str(e)}"
    
    def list_tools(self) -> list:
        """List available MCP tools"""
        self._ensure_connected()
        
        if self.session_id is None:
            return []
        
        self.request_counter += 1
        request_id = self.request_counter
        
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/list",
            "params": {}
        }
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/event-stream'
            }
            if self.session_id:
                headers['mcp-session-id'] = self.session_id
            
            response = requests.post(
                f'{self.base_url}/mcp',
                headers=headers,
                json=payload,
                timeout=5,
                stream=True
            )
            
            # Read SSE response
            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith('data:'):
                        data = decoded.split(':', 1)[1].strip()
                        try:
                            result = json.loads(data)
                            if 'result' in result:
                                return result['result'].get('tools', [])
                        except json.JSONDecodeError:
                            pass
                
        except Exception as e:
            print(f"Error listing tools: {e}")
        
        return []


class ReadGoogleDocTool(BaseTool):
    name: str = "read_google_doc"
    description: str = (
        "Reads content from the company's Corporate Health Insurance Google Doc. "
        "Use this tool to answer questions about health insurance policies, coverage, "
        "benefits, enrollment, claims, premiums, and employee medical benefits. "
        "Input should be a question or topic you want to search for in the health insurance document."
    )
    
    mcp_url: str = "http://localhost:3000"
    mcp_client: Optional[MCPClient] = None
    
    def _get_client(self) -> MCPClient:
        """Get or create MCP client"""
        if self.mcp_client is None:
            self.mcp_client = MCPClient(self.mcp_url)
        return self.mcp_client
    
    def _run(self, query: str) -> str:
        """Read the Google Doc (doc ID is hardcoded in server)"""
        try:
            client = self._get_client()
            # Call without docId since it's hardcoded in the server
            result = client.call_tool("read_google_doc", {})
            
            # Add context about what was retrieved
            if result and not result.startswith("Error"):
                return f"Health Insurance Policy Information:\n\n{result}"
            return result
        except Exception as e:
            return f"Error reading Google Doc: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version not implemented"""
        return self._run(query)
