# app/vectorstore/pinecone_store.py
import os
from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings

# Create Pinecone client instance
pc = Pinecone(
    api_key=settings.pinecone_api_key
)

index_name = settings.pinecone_index_name

# Create index if it doesn't exist
if index_name not in [idx.name for idx in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=384,  # sentence-transformers/all-MiniLM-L6-v2 embedding size
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",  # adjust cloud region
            region="us-east-1"
        )
    )

# Connect to the index
index = pc.Index(index_name)

def upsert_vectors(vectors: list[dict], namespace: str = "default"):
    index.upsert(vectors=vectors, namespace=namespace)

def query_vectors(vector: list[float], top_k: int = 3, namespace: str = "default"):
    return index.query(vector=vector, top_k=top_k, include_metadata=True, namespace=namespace)