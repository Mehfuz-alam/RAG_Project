
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.ingest_service import IngestService

router = APIRouter()
ingest_service = IngestService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/ingest")
async def ingest(
    file: UploadFile,
    session_id: str,
    strategy: str = "fixed",
    db: Session = Depends(get_db)
):
    content = await file.read()
    result = ingest_service.process_file(
        db=db,
        file_bytes=content,
        filename=file.filename,
        strategy=strategy,
        session_id=session_id
    )
    return result