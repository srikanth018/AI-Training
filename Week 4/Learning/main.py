from langchain_ollama import ChatOllama

llm = ChatOllama(model="deepseek-r1:7b")   # or mistral, gemma, etc.
resp = llm.invoke("Hello! How are you?")
print(resp.content)
