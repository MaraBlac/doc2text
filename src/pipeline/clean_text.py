"""
Text cleaning logic.
"""
import unicodedata


def clean_text(text: str) -> str:
    """
    Clean extracted text.
    """
    # Normalize unicode
    text = unicodedata.normalize("NFKC", text)

    # Remove excessive whitespace
    text = " ".join(text.split())

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove short lines (page numbers, footers, etc.)
    lines = text.split("\n")
    cleaned_lines = [line for line in lines if len(line.strip()) > 30]

    return "\n".join(cleaned_lines)
