import json
import re
import requests
from bs4 import BeautifulSoup

def extract_url(text: str) -> str | None:
    """Extract URL from text using regex"""
    match = re.search(r'(https?://[^\s]+)', text)
    return match.group(1) if match else None


def crawl_website(url: str, max_chars: int = 4000) -> str:
    """Crawl a website and extract text content"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove junk
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
        tag.decompose()

    # Wikipedia-specific main content
    content_div = soup.find("div", {"id": "mw-content-text"})
    if content_div:
        text = " ".join(content_div.stripped_strings)
    else:
        text = " ".join(soup.stripped_strings)

    return text[:max_chars]


def lambda_handler(event, context):
    """
    AWS Lambda handler for Bedrock Agent web crawling tool
    Supports FUNCTION-BASED Bedrock Agent format
    """
    print("EVENT:", json.dumps(event, indent=2, default=str))

    # Extract user input
    user_input = ""
    
    # Method 1: From inputText (function-based format)
    if event.get("inputText"):
        user_input = event.get("inputText", "")
    
    # Method 2: From parameters (function-based format)
    elif event.get("parameters"):
        for param in event.get("parameters", []):
            if param.get("name") == "query":
                user_input = param.get("value", "")
                break
    
    # Method 3: From requestBody (API-based format)
    elif event.get("requestBody"):
        try:
            content = event["requestBody"].get("content", {})
            if isinstance(content, dict):
                properties = content.get("application/json", {}).get("properties", [])
                for prop in properties:
                    if prop.get("name") == "query":
                        user_input = prop.get("value", "")
                        break
        except Exception as e:
            print("Error parsing requestBody:", str(e))
    
    # Method 4: Legacy/test formats
    elif event.get("query"):
        user_input = event.get("query", "")

    print(f"Extracted user_input: {user_input}")

    # Build response - this is the KEY fix!
    def build_response(status_code, body_content):
        """
        Build response in the format Bedrock Agent expects
        For FUNCTION-BASED agents, the response is simpler
        """
        # For function-based agents (has "function" field), use simpler format
        if "function" in event:
            return {
                "messageVersion": event.get("messageVersion", "1.0"),
                "response": {
                    "actionGroup": event.get("actionGroup", ""),
                    "function": event.get("function", ""),
                    "functionResponse": {
                        "responseBody": {
                            "TEXT": {
                                "body": json.dumps(body_content)
                            }
                        }
                    }
                }
            }
        
        # For API-based agents (has "apiPath" field), use API format
        else:
            response = {
                "messageVersion": event.get("messageVersion", "1.0"),
                "response": {
                    "httpStatusCode": status_code,
                    "responseBody": {
                        "application/json": {
                            "body": json.dumps(body_content)
                        }
                    }
                }
            }
            
            # Include optional fields if present
            if event.get("actionGroup"):
                response["response"]["actionGroup"] = event["actionGroup"]
            if event.get("apiPath"):
                response["response"]["apiPath"] = event["apiPath"]
            if event.get("httpMethod"):
                response["response"]["httpMethod"] = event["httpMethod"]
            
            return response

    # Validate input
    if not user_input:
        return build_response(400, {
            "error": "No query provided. Please provide a URL to crawl."
        })

    # Extract URL
    url = extract_url(user_input)
    
    if not url:
        return build_response(400, {
            "error": "No valid URL found in the query. Please provide a valid URL."
        })

    print(f"Crawling URL: {url}")

    # Attempt to crawl the website
    try:
        content = crawl_website(url)
        print(f"Successfully crawled {len(content)} characters")
        
        return build_response(200, {
            "url": url,
            "content": content,
            "content_length": len(content),
            "status": "success"
        })
    
    except requests.exceptions.Timeout:
        print(f"TIMEOUT crawling {url}")
        return build_response(504, {
            "error": f"Timeout: The website {url} took too long to respond."
        })
    
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        print(f"HTTP ERROR crawling {url}: {e}")
        return build_response(status_code, {
            "error": f"HTTP Error: {str(e)}"
        })
    
    except Exception as e:
        print(f"UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return build_response(500, {
            "error": f"Failed to crawl website: {str(e)}"
        })