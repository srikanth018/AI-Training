import os
import json
import uuid
import boto3
import chromadb
from pypdf import PdfReader


CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 4
EMBED_MODEL = "amazon.titan-embed-text-v1"
LLM_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"

CHROMA_DIR = "chroma"
COLLECTION = "rag_docs"

# Bedrock Clients
bedrock = boto3.client("bedrock-runtime")

# ChromaDB
chroma = chromadb.PersistentClient(path=CHROMA_DIR)

collection = chroma.get_or_create_collection(
    name=COLLECTION,
    metadata={"hnsw:space": "cosine"}
)

# Helpers
def embed(text: str):
    response = bedrock.invoke_model(
        modelId=EMBED_MODEL,
        body=json.dumps({"inputText": text})
    )
    return json.loads(response["body"].read())["embedding"]

def chunk_text(text):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + CHUNK_SIZE])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def load_pdf(path):
    reader = PdfReader(path)
    return "\n".join(
        page.extract_text() or "" for page in reader.pages
    )

# Ingestion
def ingest_pdfs():
    for file in os.listdir('pdfs'):
        if not file.endswith(".pdf"):
            continue

        text = load_pdf(os.path.join('pdfs', file))
        chunks = chunk_text(text)

        for chunk in chunks:
            collection.add(
                ids=[str(uuid.uuid4())],
                documents=[chunk],
                embeddings=[embed(chunk)],
                metadatas=[{"source": file}]
            )

        print(f"Ingested: {file}")

# Retrieval
def retrieve(query):
    results = collection.query(
        query_embeddings=[embed(query)],
        n_results=TOP_K
    )
    return "\n".join(results["documents"][0])

# Generation
def generate(context, question):
    prompt = f"""
Answer ONLY using the context below.
If the answer is not found, say "Given context does not provide an answer. I will give you the answer based on my knowledge.", then find the answer for the question.

Context:
{context}

Question:
{question}
"""
    print (prompt)
    response = bedrock.invoke_model(
        modelId=LLM_MODEL,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.2
        })
    )

    return json.loads(response["body"].read())["content"][0]["text"]

# Chat
def chat():
    while True:
        q = input("\nAsk (or 'exit'): ")
        if q.lower() == "exit":
            break
        context = retrieve(q)
        print("\nAnswer:\n", generate(context, q))

# Main
if __name__ == "__main__":
    # ingest_pdfs()
    chat()
