from sqlalchemy.orm import Session
from app.db.models import Booking, Document


def create_booking(db: Session, data: dict):
    booking = Booking(**data)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def create_document(
    db: Session,
    filename: str,
    chunks_count: int,
    namespace: str
):
    doc = Document(
        filename=filename,
        chunks_count=chunks_count,
        namespace=namespace
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc