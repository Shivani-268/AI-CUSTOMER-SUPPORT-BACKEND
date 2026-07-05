import os
import faiss
import numpy as np
from google import genai
from app.config import settings

class VectorStoreManager:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.index = None
        self.documents = []

    async def initialize_store(self, faq_path: str):
        """Reads the text file and builds the FAISS index using the new Google GenAI SDK."""
        if not os.path.exists(faq_path):
            print(f"Error: {faq_path} not found.")
            return
        
        with open(faq_path, "r") as f:
            self.documents = [line.strip() for line in f if line.strip()]

        if not self.documents:
            print("Warning: faq.txt is empty.")
            return

        # Generate vectors using the new client and explicit model name
        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=self.documents
        )
        
        # Extract numerical vectors out of the modern structured response array
        embeddings = [item.values for item in response.embeddings]
        float32_embeddings = np.array(embeddings).astype("float32")
        
        # FIX: gemini-embedding-001 creates vectors with 3072 dimensions!
        dimension = 3072 
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(float32_embeddings)
        print("Vector store successfully initialized with Gemini for FREE!")

    async def search(self, query: str, k: int = 1):
        """Finds the 'k' most similar sentences from the handbook index."""
        if not self.index:
            return []

        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=query
        )
        
        query_vector = np.array([response.embeddings[0].values]).astype("float32")
        
        distances, indices = self.index.search(query_vector, k)
        return [self.documents[idx] for idx in indices[0] if idx != -1]

vector_store = VectorStoreManager()