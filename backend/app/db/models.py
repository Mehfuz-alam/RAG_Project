from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from datetime import datetime
from app.db.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    date = Column(Date, nullable=True)
    time = Column(Time, nullable=True)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    chunks_count = Column(Integer, default=0)
    namespace = Column(String, default="default")
    ingested_at = Column(DateTime, default=datetime.utcnow)