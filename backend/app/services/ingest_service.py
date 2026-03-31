
from typing import List
import uuid
from sqlalchemy.orm import Session

from app.llm.embeddings_provider import embed_text
from app.vectorstore.pinecone_store import upsert_vectors
from app.rag.chunking import fixed_chunk, semantic_chunk
from app.utils.pdf_utils import extract_pdf_text
from app.utils.text_utils import clean_text
from app.db.repositories import create_document


class IngestService:
    def process_file(
        self,
        db: Session,
        file_bytes: bytes,
        filename: str,
        strategy: str = "fixed",
        session_id: str = "default"
    ) -> dict:

        # 1. Extract text
        if filename.endswith(".pdf"):
            text = extract_pdf_text(file_bytes)
        else:
            text = file_bytes.decode("utf-8")

        text = clean_text(text)

        # 2. Chunking
        chunks = fixed_chunk(text) if strategy == "fixed" else semantic_chunk(text)

        # 3. Prepare vectors
        vectors = []
        for chunk in chunks:
            vector = embed_text(chunk)
            vectors.append({
                "id": str(uuid.uuid4()),
                "values": vector,
                "metadata": {
                    "text": chunk,
                    "source": filename
                }
            })

        # 4. Store in Pinecone (namespace = session_id)
        upsert_vectors(vectors, namespace=session_id)

        # 5. Save document metadata in Postgres
        create_document(
            db=db,
            filename=filename,
            chunks_count=len(chunks),
            namespace=session_id
        )

        print("Document saved in DB:", filename)

        return {
            "chunks_ingested": len(chunks),
            "filename": filename,
            "session_id": session_id
        }