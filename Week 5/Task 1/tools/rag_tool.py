"""
Generic RAG Tool using FAISS Vector Database
Provides semantic search capabilities over internal documents
"""

from typing import List
from langchain_core.tools import Tool
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os


class RAGTool:
    """Generic RAG tool for document retrieval using FAISS"""
    
    def __init__(self, 
                 document_dir: str,
                 index_name: str,
                 aws_region: str = "us-east-1",
                 chunk_size: int = 500,
                 chunk_overlap: int = 50):
        """
        Initialize RAG tool
        
        Args:
            document_dir: Directory containing documents to index
            index_name: Name for the FAISS index
            aws_region: AWS region for Bedrock
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.document_dir = document_dir
        self.index_name = index_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize Bedrock embeddings
        self.embeddings = BedrockEmbeddings(
            region_name=aws_region,
            model_id="amazon.titan-embed-text-v1"
        )
        
        # Initialize vector store
        self.vector_store = None
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """Load existing index or create new one"""
        index_path = f"{self.index_name}_index"
        
        if os.path.exists(index_path):
            self.vector_store = FAISS.load_local(
                index_path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            print(f"Creating new FAISS index: {index_path}")
            self._create_index()
    
    def _load_documents(self) -> List[Document]:
        """Load documents from directory"""
        documents = []
        
        if not os.path.exists(self.document_dir):
            print(f"Warning: Document directory {self.document_dir} does not exist")
            return documents
        
        for filename in os.listdir(self.document_dir):
            if filename.endswith('.txt') or filename.endswith('.md'):
                file_path = os.path.join(self.document_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append(Document(
                        page_content=content,
                        metadata={"source": filename}
                    ))
        
        return documents
    
    def _create_index(self):
        """Create FAISS index from documents"""
        # Load documents
        documents = self._load_documents()
        
        if not documents:
            # Create empty index
            self.vector_store = FAISS.from_texts(
                ["Empty index - no documents found"],
                self.embeddings
            )
            return
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        splits = text_splitter.split_documents(documents)
        
        # Create vector store
        self.vector_store = FAISS.from_documents(splits, self.embeddings)
        
        # Save index
        index_path = f"{self.index_name}_index"
        self.vector_store.save_local(index_path)
        print(f"Created and saved FAISS index with {len(splits)} chunks")
    
    def search(self, query: str, k: int = 3) -> str:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            Formatted search results
        """
        print(f"\n[TOOL: {self.index_name.upper()} RAG] Searching internal documentation...")
        print(f"[TOOL: {self.index_name.upper()} RAG] Query: '{query}'")
        
        if not self.vector_store:
            return "No documents available in the knowledge base."
        
        try:
            # Perform similarity search
            results = self.vector_store.similarity_search(query, k=k)
            
            if not results:
                return "No relevant information found in the knowledge base."
            
            # Format results
            formatted_results = []
            for i, doc in enumerate(results, 1):
                source = doc.metadata.get('source', 'Unknown')
                content = doc.page_content.strip()
                formatted_results.append(
                    f"--- Result {i} (Source: {source}) ---\n{content}\n"
                )
            
            return "\n".join(formatted_results)
        
        except Exception as e:
            return f"Error searching knowledge base: {str(e)}"
    
    def as_tool(self, name: str, description: str) -> Tool:
        """
        Convert to LangChain Tool
        
        Args:
            name: Tool name
            description: Tool description
            
        Returns:
            LangChain Tool instance
        """
        return Tool(
            name=name,
            func=self.search,
            description=description
        )


def create_rag_tool(document_dir: str, 
                   index_name: str,
                   tool_name: str,
                   tool_description: str) -> Tool:
    """
    Factory function to create a RAG tool
    
    Args:
        document_dir: Directory containing documents
        index_name: Name for the FAISS index
        tool_name: Name for the tool
        tool_description: Description for the tool
        
    Returns:
        LangChain Tool instance
    """
    rag = RAGTool(document_dir=document_dir, index_name=index_name)
    return rag.as_tool(name=tool_name, description=tool_description)
