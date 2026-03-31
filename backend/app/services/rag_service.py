# from typing import List
# from app.llm.embeddings_provider import embed_text
# from app.vectorstore.pinecone_store import query_vectors
# from app.memory.redis_memory import get_memory, update_memory
# from app.llm.llm_provider import generate_response


# class RAGService:
#     def __init__(self, namespace: str = "default", top_k: int = 3):
#         self.namespace = namespace
#         self.top_k = top_k

#     def get_context(self, query: str) -> List[str]:
#         """
#         Retrieve relevant chunks from vector store for the query
#         """
#         vector = embed_text(query)
#         results = query_vectors(vector, top_k=self.top_k, namespace=self.namespace)
#         return [match["metadata"]["text"] for match in results.get("matches", [])]

#     def answer_query(self, query: str, session_id: str) -> str:
#         """
#         Handles a user query with context and session memory
#         """
#         # 1. Retrieve relevant context
#         context = self.get_context(query)
#         context_str = "\n".join(context) if context else "No relevant context found."

#         # 2. Get previous memory
#         history = get_memory(session_id)
#         history_str = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history]) if history else "No previous conversation."

#         # 3. Build prompt for LLM
#         prompt = f"""
# You are a helpful AI assistant.

# Context:
# {context_str}

# Conversation History:
# {history_str}

# User Question:
# {query}

# Answer clearly.
# """

#         # 4. Generate LLM response safely
#         try:
#             response = generate_response(prompt)
#         except Exception as e:
#             response = "Sorry, I cannot answer this right now."
#             print(f"LLM Error: {e}")

#         # 5. Update Redis memory as structured JSON
#         update_memory(session_id, role="user", text=query)
#         update_memory(session_id, role="assistant", text=response)

#         return response



from typing import List
from app.llm.embeddings_provider import embed_text
from app.vectorstore.pinecone_store import query_vectors
from app.memory.redis_memory import get_memory, update_memory
from app.llm.llm_provider import generate_response


class RAGService:
    def __init__(self, top_k: int = 3):
        self.top_k = top_k

    def get_context(self, query: str, session_id: str) -> List[str]:
        """
        Retrieve relevant chunks from vector store for the query
        """
        vector = embed_text(query)
        results = query_vectors(vector, top_k=self.top_k, namespace=session_id)
        return [match["metadata"]["text"] for match in results.get("matches", [])]

    def answer_query(self, query: str, session_id: str) -> str:
        """
        Handles a user query with context and session memory
        """

        # 1. Retrieve relevant context (from session namespace)
        context = self.get_context(query, session_id)
        context_str = "\n".join(context) if context else "No relevant context found."

        # 2. Get previous memory (Redis)
        history = get_memory(session_id)
        history_str = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in history]
        ) if history else "No previous conversation."

        # 3. Build prompt for LLM
        prompt = f"""
You are a helpful AI assistant.

Context:
{context_str}

Conversation History:
{history_str}

User Question:
{query}

Answer clearly.
"""

        # 4. Generate LLM response
        try:
            response = generate_response(prompt)
        except Exception as e:
            response = "Sorry, I cannot answer this right now."
            print(f"LLM Error: {e}")

        # 5. Update Redis memory
        update_memory(session_id, role="user", text=query)
        update_memory(session_id, role="assistant", text=response)

        return response