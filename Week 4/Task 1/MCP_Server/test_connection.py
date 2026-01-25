import requests
import json

print("Testing MCP connection...")
print("1. Testing GET request to /mcp...")

try:
    response = requests.get('http://localhost:3000/mcp', stream=True, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    
    # Read first few lines
    count = 0
    for line in response.iter_lines(decode_unicode=True):
        if line:
            print(f"Line {count}: {line}")
            count += 1
            if count > 10:
                break
except Exception as e:
    print(f"Error: {e}")
