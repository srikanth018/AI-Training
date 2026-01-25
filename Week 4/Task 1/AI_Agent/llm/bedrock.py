from langchain_aws import ChatBedrock

def get_bedrock_llm():
    return ChatBedrock(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        region_name="us-east-1",
        model_kwargs={
            "temperature": 0.2,
            "max_tokens": 1024
        }
    )
