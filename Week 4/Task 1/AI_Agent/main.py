from dotenv import load_dotenv
from agent.agent import build_agent

# Load environment variables from .env file
load_dotenv()

def main():
    agent = build_agent()

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # New API uses messages format
        inputs = {"messages": [{"role": "user", "content": user_input}]}
        
        # Stream the response
        for chunk in agent.stream(inputs, stream_mode="updates"):
            if "model" in chunk:
                messages = chunk["model"].get("messages", [])
                for msg in messages:
                    if hasattr(msg, "content") and msg.content:
                        print("\nAgent:", msg.content)

if __name__ == "__main__":
    main()
