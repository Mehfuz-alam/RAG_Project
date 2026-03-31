from pypdf import PdfReader
import io


def extract_pdf_text(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    return " ".join([page.extract_text() or "" for page in reader.pages])