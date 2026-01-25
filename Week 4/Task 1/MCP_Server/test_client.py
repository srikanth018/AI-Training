import requests
import json
import re
import threading
import time

session_id = None
messages = {}

def keep_sse_alive():
    """Keep consuming SSE events to keep connection alive"""
    global session_id, messages
    
    # Wait for session_id to be set
    timeout = 5
    start = time.time()
    while session_id is None and (time.time() - start) < timeout:
        time.sleep(0.1)
    
    if session_id is None:
        print("[SSE] No session ID available")
        return
    
    try:
        print(f"1. Connecting to MCP endpoint with session ID: {session_id}...")
        headers = {
            'Accept': 'application/json, text/event-stream',
            'mcp-session-id': session_id
        }
        sse_response = requests.get('http://localhost:3000/mcp', stream=True, headers=headers)
        
        print(f"Response status: {sse_response.status_code}")
        print(f"Response headers: {dict(sse_response.headers)}\n")
        
        print("[SSE] Listening for events...")
        current_event = None
        for line in sse_response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                print(f"[DEBUG] Received line: {decoded}")
                
                if decoded.startswith('event:'):
                    current_event = decoded.split(':', 1)[1].strip()
                    print(f"[DEBUG] Event type: {current_event}")
                elif decoded.startswith('data:'):
                    data = decoded.split(':', 1)[1].strip()
                    print(f"[DEBUG] Data: {data}")
                    
                    # Extract session ID from endpoint event
                    if session_id is None and current_event == 'endpoint':
                        try:
                            endpoint_data = json.loads(data)
                            print(f"[DEBUG] Parsed endpoint data: {endpoint_data}")
                            if 'sessionId' in endpoint_data:
                                session_id = endpoint_data['sessionId']
                                print(f"✓ SessionId: {session_id}\n")
                        except json.JSONDecodeError as e:
                            print(f"[DEBUG] JSON decode error: {e}")
                    
                    # Parse JSON messages
                    if current_event == 'message':
                        try:
                            msg = json.loads(data)
                            if 'id' in msg:
                                messages[msg['id']] = msg
                                print(f"[SSE] Received response for request ID {msg['id']}")
                        except json.JSONDecodeError:
                            pass
    except Exception as e:
        print(f"[SSE] Connection ended: {e}")

def test_mcp_server():
    global session_id, messages
    
    print("Testing MCP Server...\n")
    
    # Send initialize request first to set up the session
    print("1. Sending initialize request...")
    initialize_payload = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    # Initialize with SSE response
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream'
    }
    
    print("Starting SSE connection with initialize...")
    init_response = requests.post(
        'http://localhost:3000/mcp',
        headers=headers,
        json=initialize_payload,
        stream=True
    )
    
    print(f"Initialize response: {init_response.status_code}")
    print(f"Response headers: {dict(init_response.headers)}")
    
    # Read the SSE response to get session ID
    for line in init_response.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            print(f"[INIT] {decoded}")
            
            if decoded.startswith('data:'):
                data = decoded.split(':', 1)[1].strip()
                try:
                    init_data = json.loads(data)
                    if 'result' in init_data:
                        print(f"✓ Initialized successfully")
                        # Check headers for session ID
                        if 'x-mcp-session-id' in init_response.headers:
                            session_id = init_response.headers['x-mcp-session-id']
                            print(f"✓ Session ID from header: {session_id}\n")
                            break
                        elif 'mcp-session-id' in init_response.headers:
                            session_id = init_response.headers['mcp-session-id']
                            print(f"✓ Session ID from header: {session_id}\n")
                            break
                        else:
                            # Session ID might be in the response data or we use stateless mode
                            print("No session ID in headers - using stateless mode\n")
                            session_id = "stateless"
                            break
                except json.JSONDecodeError:
                    pass
    
    if session_id is None:
        print("❌ Failed to get session ID from initialize")
        return
    
    # Now start the SSE listener in background
    print("2. Starting SSE listener...")
    sse_thread = threading.Thread(target=keep_sse_alive, daemon=True)
    sse_thread.start()
    
    time.sleep(1)
    
    # Step 3: List tools
    print("3. Listing available tools...")
    list_tools_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream'
    }
    if session_id:
        headers['mcp-session-id'] = session_id
    
    response = requests.post(
        'http://localhost:3000/mcp',
        headers=headers,
        json=list_tools_payload,
        stream=True
    )
    
    print(f"List tools response: {response.status_code}")
    if response.status_code == 200:
        # Read SSE response
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith('data:'):
                    data = decoded.split(':', 1)[1].strip()
                    try:
                        result = json.loads(data)
                        if 'result' in result:
                            tools = result['result'].get('tools', [])
                            print(f"✓ Found {len(tools)} tools:")
                            for tool in tools:
                                print(f"  - {tool['name']}: {tool['description']}")
                            break
                    except json.JSONDecodeError:
                        pass
    else:
        print(f"Error: {response.text}")
    print()
    
    # Step 4: Call Google Doc tool
    print("4. Testing read_google_doc tool...")
    doc_id = '1GeCvppxgN4xtqSihz7rxpLESeGt5Ei6oLSepqYQarjI'
    
    call_tool_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "read_google_doc",
            "arguments": {
                "docId": doc_id
            }
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream'
    }
    if session_id:
        headers['mcp-session-id'] = session_id
    
    print("Sending request to read Google Doc...")
    response = requests.post(
        'http://localhost:3000/mcp',
        headers=headers,
        json=call_tool_payload,
        stream=True
    )
    
    print(f"Response status: {response.status_code}")
    if response.status_code == 200:
        # Read SSE response
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith('data:'):
                    data = decoded.split(':', 1)[1].strip()
                    try:
                        result = json.loads(data)
                        if 'result' in result:
                            content = result['result'].get('content', [])
                            
                            print("\n" + "="*60)
                            print("GOOGLE DOC CONTENT")
                            print("="*60 + "\n")
                            
                            for item in content:
                                if item.get('type') == 'text':
                                    print(item.get('text', ''))
                            
                            print("\n" + "="*60)
                            break
                    except json.JSONDecodeError:
                        pass
    else:
        print(f"Error: {response.text}")
    
    # Keep alive for a moment before exiting
    time.sleep(1)

if __name__ == "__main__":
    try:
        test_mcp_server()
    except Exception as e:
        print(f"❌ Error: {e}")
