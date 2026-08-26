import os
import json
import math
from google import genai
from ..config import settings

DB_PATH = "vector_db.json"

def cosine_similarity(v1: list, v2: list) -> float:
    """Calculates semantic similarity between two vectors."""
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0: return 0.0
    return dot / (mag1 * mag2)

def ingest_to_knowledge_base(filepath: str) -> str:
    """Reads a local text/markdown file, chunks it, generates embeddings, and saves it to the vector database.
    Use this when the user asks you to 'study', 'ingest', or 'memorize' a document.
    Args:
        filepath: Path to the file (e.g., 'docs/architecture.md').
    """
    if not os.path.exists(filepath):
        return f"Error: File '{filepath}' not found."
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
            
        # Basic chunking: split by double newlines or fallback to 1000 character blocks
        chunks = [c.strip() for c in text.split('\n\n') if len(c.strip()) > 50]
        if not chunks:
            chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
            
        client = genai.Client(api_key=settings.gemini_api_key)
        
        # Load existing DB
        db = []
        if os.path.exists(DB_PATH):
            with open(DB_PATH, "r", encoding="utf-8") as f:
                db = json.load(f)
                
        # Generate embeddings for new chunks
        added_count = 0
        for chunk in chunks:
            response = client.models.embed_content(model="text-embedding-004", contents=chunk)
            embedding = response.embeddings[0].values
            db.append({
                "source": filepath,
                "text": chunk,
                "embedding": embedding
            })
            added_count += 1
            
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(db, f)
            
        return f"Success. Ingested {added_count} chunks from {filepath} into the vector database."
    except Exception as e:
        return f"Failed to ingest document: {str(e)}"

def search_knowledge_base(query: str) -> str:
    """Searches the local knowledge base (RAG) for relevant document chunks based on semantic similarity.
    Use this when you need context about the user's specific projects, documents, or custom architecture.
    Args:
        query: The search query or question to find context for.
    """
    if not os.path.exists(DB_PATH):
        return "Knowledge base is empty. No documents ingested yet."
        
    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.embed_content(model="text-embedding-004", contents=query)
        query_embed = response.embeddings[0].values
        
        with open(DB_PATH, "r", encoding="utf-8") as f:
            db = json.load(f)
            
        # Calculate similarities
        results = []
        for item in db:
            sim = cosine_similarity(query_embed, item["embedding"])
            results.append((sim, item["text"], item["source"]))
            
        # Sort by highest similarity
        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:3] # Grab top 3 chunks
        
        if not top_results or top_results[0][0] < 0.4:
            return "No highly relevant information found in the knowledge base."
            
        context = "Found relevant context from vector search:\n"
        for sim, text, source in top_results:
            context += f"---\nSource: {source} (Relevance: {sim:.2f})\n{text}\n"
            
        return context
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"
