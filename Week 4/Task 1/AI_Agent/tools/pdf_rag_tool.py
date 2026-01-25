import os
from typing import Optional, List
from langchain.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path


class PDFRAGTool(BaseTool):
    name: str = "search_pdf_documents"
    description: str = (
        "Search and retrieve information from PDF documents related to the company’s "
        "Corporate Hybrid Work Policy. "
        "Use this tool to answer questions about work-from-home and office attendance rules, "
        "employee eligibility, approval processes, working hours, security and compliance guidelines, "
        "equipment usage, performance expectations, leave alignment, and other hybrid workplace policies. "
        "Input should be a natural language question."
    )

    
    pdf_directory: str = "./pdf_rag"
    vectorstore: Optional[FAISS] = None
    embeddings: Optional[HuggingFaceEmbeddings] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def _initialize_vectorstore(self):
        """Initialize the vector store with PDFs from the directory"""
        if self.vectorstore is not None:
            return  # Already initialized
        
        print(f"Initializing RAG system from PDFs in {self.pdf_directory}...")
        
        # Initialize embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Load all PDFs from directory
        pdf_files = list(Path(self.pdf_directory).glob("*.pdf"))
        
        if not pdf_files:
            raise Exception(f"No PDF files found in {self.pdf_directory}")
        
        print(f"Found {len(pdf_files)} PDF file(s)")
        
        # Load and process all PDFs
        all_documents = []
        for pdf_file in pdf_files:
            print(f"Loading {pdf_file.name}...")
            loader = PyPDFLoader(str(pdf_file))
            documents = loader.load()
            all_documents.extend(documents)
        
        print(f"Loaded {len(all_documents)} pages total")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        splits = text_splitter.split_documents(all_documents)
        print(f"Created {len(splits)} text chunks")
        
        # Create vector store
        print("Creating FAISS vector store...")
        self.vectorstore = FAISS.from_documents(splits, self.embeddings)
        print("✓ RAG system initialized successfully")
    
    def _run(self, query: str) -> str:
        """Search the PDF documents for relevant information"""
        try:
            # Initialize on first use
            if self.vectorstore is None:
                self._initialize_vectorstore()
            
            # Perform similarity search
            docs = self.vectorstore.similarity_search(query, k=3)
            
            if not docs:
                return "No relevant information found in the PDF documents."
            
            # Format the results
            result = "Found relevant information from PDF documents:\n\n"
            
            for i, doc in enumerate(docs, 1):
                # Get source filename
                source = doc.metadata.get('source', 'Unknown')
                source_name = Path(source).name if source != 'Unknown' else 'Unknown'
                page = doc.metadata.get('page', 'Unknown')
                
                result += f"**Source {i}** ({source_name}, Page {page}):\n"
                result += doc.page_content.strip() + "\n\n"
            
            return result.strip()
            
        except Exception as e:
            return f"Error searching PDF documents: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version"""
        return self._run(query)
