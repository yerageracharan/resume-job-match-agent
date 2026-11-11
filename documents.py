"""Local extraction for PDF, DOCX, and TXT resumes."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path

MAX_FILE_BYTES = 10 * 1024 * 1024
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def extract_text_from_bytes(data: bytes, filename: str) -> str:
    if not data:
        raise ValueError("The uploaded file is empty.")
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("File exceeds the 10 MB limit.")
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError("Upload a PDF, DOCX, or TXT file.")
    if suffix == ".txt":
        text = data.decode("utf-8-sig", errors="replace")
    elif suffix == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(BytesIO(data))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            raise ValueError(f"Could not read this PDF: {exc}") from exc
        if not text.strip():
            raise ValueError("This PDF contains no selectable text. It may be scanned; use OCR first or paste the resume text.")
    else:
        try:
            from docx import Document
            document = Document(BytesIO(data))
            blocks = [p.text for p in document.paragraphs if p.text.strip()]
            for table in document.tables:
                for row in table.rows:
                    cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if cells:
                        blocks.append(" | ".join(cells))
            text = "\n".join(blocks)
        except Exception as exc:
            raise ValueError(f"Could not read this DOCX: {exc}") from exc
    if not text.strip():
        raise ValueError("No text could be extracted from this file.")
    return text.strip()


def extract_text_from_path(file_path: str) -> str:
    path = Path(file_path).expanduser().resolve()
    if not path.exists() or not path.is_file():
        raise ValueError("The supplied resume path does not point to an existing file.")
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError("Resume file must be PDF, DOCX, or TXT.")
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("File exceeds the 10 MB limit.")
    return extract_text_from_bytes(path.read_bytes(), path.name)
