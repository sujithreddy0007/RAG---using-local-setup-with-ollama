from pypdf import PdfReader
from io import BytesIO
from app.core.logging import logger

def load_text_from_file(file_bytes: bytes, filename: str) -> str:
    logger.info(f"Loading file: {filename}")

    if filename.lower().endswith(".pdf"):
        pdf_stream = BytesIO(file_bytes)
        reader = PdfReader(pdf_stream)

        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text

    # Plain text files
    return file_bytes.decode("utf-8", errors="ignore")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks
