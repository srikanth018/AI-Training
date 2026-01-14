import boto3
import json

# ---------------- BEDROCK CLIENT ---------------- #

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# ---------------- PROMPTS ---------------- #

# 1. WITHOUT Chain-of-Thought
STANDARD_PROMPT = """
You are a billing assistant specialized in solving customer queries related to billing,
invoices, subscriptions, refunds, late fees, and payments for a SaaS product.

Guidelines:
- Be customer-friendly, polite, and professional
- Responses must be clear, simple, and accurate
- Ask for missing required details such as invoice number, dates, transaction ID, or plan name
- Do not assume any information that is not provided
- Provide clear next steps when applicable
"""

# 2. WITH Chain-of-Thought (Hidden)
COT_PROMPT = """
You are a billing assistant specialized in solving customer queries related to billing,
invoices, subscriptions, refunds, late fees, and payments for a SaaS product.

For every customer query:
- Internally analyze the problem step by step before responding
- Do NOT show your reasoning or analysis to the customer
- Make decisions strictly based on billing policies
- Ask for missing required details such as invoice number, dates, transaction ID, or plan name
- Do not assume information that is not provided

Guidelines:
- Be customer-friendly, polite, and professional
- Responses must be clear, simple, and accurate
- Avoid hallucinations; only respond based on provided data
- Provide clear next steps when applicable
"""

# ---------------- MODE SELECTION ---------------- #

print("Select Billing Assistant Mode:")
print("1. Standard Billing Assistant (Without Chain-of-Thought)")
print("2. Advanced Billing Assistant (With Hidden Chain-of-Thought)")

choice = input("Enter 1 or 2: ").strip()

if choice == "2":
    system_prompt = COT_PROMPT
    print("\nRunning in ADVANCED mode (Hidden Chain-of-Thought)\n")
else:
    system_prompt = STANDARD_PROMPT
    print("\nRunning in STANDARD mode (No Chain-of-Thought)\n")

# ---------------- CHAT LOOP ---------------- #

conversation = []  # ONLY user + assistant messages

print("Billing Support Chatbot (type 'exit' to quit)\n")

while True:
    user_input = input("User: ")

    if user_input.lower() == "exit":
        print("\nAssistant: Thank you for contacting billing support. Have a great day!")
        break

    # Append user message
    conversation.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_input
            }
        ]
    })

    # Invoke Claude 3
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": system_prompt,
            "messages": conversation,
            "max_tokens": 500,
            "temperature": 0.2
        })
    )

    # Parse response
    result = json.loads(response["body"].read())
    assistant_reply = result["content"][0]["text"]

    # Append assistant message
    conversation.append({
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": assistant_reply
            }
        ]
    })

    print("\nAssistant:", assistant_reply, "\n")
