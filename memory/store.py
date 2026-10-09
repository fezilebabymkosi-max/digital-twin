"""
memory/store.py
Manages document ingestion, chunking, vector embeddings, and retrieval using ChromaDB.
"""

import os
from dotenv import load_dotenv
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

class MemoryStore:
    def __init__(self, collection_name: str = "digital_twin_memory", persist_dir: str = "./memory/chroma_db"):
        # Initialize persistent ChromaDB client using default local embeddings
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Default collection uses built-in ONNX MiniLM embeddings locally
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )
        
        # Configure text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

    def add_documents(self, texts: list[str], metadatas: list[dict] = None):
        """Splits raw documents into chunks and stores them in ChromaDB."""
        chunks = []
        chunk_metadatas = []
        chunk_ids = []

        counter = 0
        for idx, text in enumerate(texts):
            doc_chunks = self.text_splitter.split_text(text)
            doc_meta = metadatas[idx] if metadatas else {}
            
            for c_idx, chunk in enumerate(doc_chunks):
                chunks.append(chunk)
                meta = doc_meta.copy()
                meta["chunk_id"] = c_idx
                chunk_metadatas.append(meta)
                chunk_ids.append(f"doc_{idx}_chunk_{c_idx}_{counter}")
                counter += 1

        if chunks:
            self.collection.add(
                documents=chunks,
                metadatas=chunk_metadatas,
                ids=chunk_ids
            )
            print(f"Successfully added {len(chunks)} chunks to memory.")

    def query_memory(self, query: str, n_results: int = 3) -> list[str]:
        """Retrieves top N most semantically relevant context chunks for a query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results["documents"][0] if results["documents"] else []