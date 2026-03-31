
from fastapi import APIRouter, Depends
from app.services.rag_service import RAGService
from app.services.booking_service import BookingService
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

router = APIRouter()
rag_service = RAGService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/chat")
def chat(query: str, session_id: str, db: Session = Depends(get_db)):
    # 1. Extract booking info
    booking_data = BookingService.extract_booking(query)

    # 2. Only save if at least name or email exists
    if booking_data and (booking_data.get("name") or booking_data.get("email")):
        BookingService.save_booking(db, booking_data)
        return {"response": "Booking confirmed", "booking": booking_data}

    # 3. Otherwise normal RAG chat
    response = rag_service.answer_query(query, session_id)
    return {"response": response}