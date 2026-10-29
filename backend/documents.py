from io import BytesIO
from pathlib import Path

from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def extract_text(filename: str, file_bytes: bytes) -> str:
    """Extract text from a PDF, TXT, or Markdown document."""

    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. Upload PDF, TXT, or Markdown."
        )

    if extension == ".pdf":
        reader = PdfReader(BytesIO(file_bytes))
        pages = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                pages.append(page_text)

        text = "\n".join(pages)

    else:
        text = file_bytes.decode("utf-8-sig")

    if not text.strip():
        raise ValueError(
            "No readable text found. The document may be empty or scanned."
        )

    return text.strip()


def split_into_chunks(
    text: str,
    chunk_size: int = 800,
    overlap: int = 100
) -> list[str]:
    """Split text into readable chunks while preserving sentence boundaries."""

    import re

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    text = text.strip()

    if not text:
        return []

    # Separate the text into sentences.
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    chunks = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        # Handle a sentence that is longer than the chunk limit.
        while len(sentence) > chunk_size:
            if current:
                chunks.append(current.strip())
                current = ""

            split_at = sentence.rfind(" ", 0, chunk_size + 1)

            if split_at <= 0:
                split_at = chunk_size

            chunks.append(sentence[:split_at].strip())
            sentence = sentence[split_at:].strip()

        # Add the sentence if it fits in the current chunk.
        if not current:
            current = sentence

        elif len(current) + 1 + len(sentence) <= chunk_size:
            current += " " + sentence

        else:
            chunks.append(current.strip())

            # Keep some text from the previous chunk as overlap.
            if overlap > 0:
                tail = current[-overlap:].strip()

                # Avoid starting the next chunk in the middle of a word.
                if " " in tail:
                    tail = tail.split(" ", 1)[1]

                current = (tail + " " + sentence).strip()
            else:
                current = sentence

    if current.strip():
        chunks.append(current.strip())

    return chunks