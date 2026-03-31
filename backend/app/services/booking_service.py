
import json
import re
from sqlalchemy.orm import Session
from app.db.repositories import create_booking
from app.llm.llm_provider import generate_response
import datetime
import re
from dateutil import parser as date_parser

class BookingService:
    @staticmethod
    def extract_booking(query: str) -> dict | None:
        """
        Extract booking info from the query.
        First, try LLM JSON parsing. If it fails or fields are empty, use regex fallback.
        """
        prompt = f"""
Extract name, email, date, and time from this message.

Message:
{query}

Return ONLY JSON in this EXACT format:
{{
  "name": "string",
  "email": "string",
  "date": "YYYY-MM-DD",
  "time": "HH:MM"
}}

Do not include any text outside JSON.
If a field is missing, return an empty string for that field.
"""
        response = generate_response(prompt)

        booking_data = None
        try:
            booking_data = json.loads(response)
        except json.JSONDecodeError:
            booking_data = None

        # If LLM failed or fields are empty, use regex fallback
        if not booking_data or not any(booking_data.values()):
            booking_data = BookingService._parse_booking_fallback(query)

        return booking_data

    @staticmethod
    def save_booking(db: Session, booking_data: dict):
        # Convert date/time strings to datetime objects
        if booking_data.get("date"):
            booking_data["date"] = datetime.datetime.strptime(
                booking_data["date"], "%Y-%m-%d"
            ).date()
        if booking_data.get("time"):
            booking_data["time"] = datetime.datetime.strptime(
                booking_data["time"], "%H:%M"
            ).time()

        return create_booking(db, booking_data)


    @staticmethod
    def _parse_booking_fallback(query: str) -> dict:
        data = {"name": "", "email": "", "date": "", "time": ""}

        # Email
        email_match = re.search(r"[\w\.-]+@[\w\.-]+", query)
        if email_match:
            data["email"] = email_match.group(0)

        # Date (YYYY-MM-DD)
        date_match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", query)
        if date_match:
            data["date"] = date_match.group(0)

        # Time (HH:MM)
        time_match = re.search(r"\b\d{1,2}:\d{2}\b", query)
        if time_match:
            data["time"] = time_match.group(0)

        # Name (look for "for <name>" or "I am <name>")
        name_match = re.search(r"(?:for|I am|I'm|My name is) ([A-Z][a-z]+(?: [A-Z][a-z]+)*)", query)
        if name_match:
            data["name"] = name_match.group(1)

        return data