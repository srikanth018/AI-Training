import boto3
import json

# Read the large context document
with open("large_context_doc.txt", "r", encoding="utf-8") as f:
    document_content = f.read()

# Get user question
input_text = input("Enter your question about the document: ")

# Construct the prompt with document context
prompt = f"""I'm providing you with enterprise cloud infrastructure documentation. Please read through it carefully and answer my question based on the information in the document.

<document>
{document_content}
</document>

Question: {input_text}

Please provide a detailed answer based solely on the information in the document above. If the information is not in the document, please say so."""

# Initialize Bedrock client
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

print("\nQuerying Claude via AWS Bedrock...")

# Invoke the model
response = bedrock.invoke_model(
    modelId="anthropic.claude-3-sonnet-20240229-v1:0",
    contentType="application/json",
    accept="application/json",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
)

# Parse response
result = json.loads(response["body"].read())
output_text = result["content"][0]["text"]


# Save to file
with open("bedrock_output.txt", "a", encoding="utf-8") as f:
    f.write("="*80 + "\n")
    f.write("Input:\n" + input_text + "\n\n")
    f.write("Output:\n" + output_text + "\n\n")
print("\nResponse saved to bedrock_output.txt")