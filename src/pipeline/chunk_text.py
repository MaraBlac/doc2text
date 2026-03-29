"""
Text chunking logic.
"""


def chunk_text(text: str, max_size: int = 500, overlap: int = 50) -> list:
    """
    Split text into chunks with overlap.

    Args:
        text: Text to chunk
        max_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + max_size
        chunks.append(text[start:end])

        if overlap > 0:
            start += max_size - overlap
        else:
            start += max_size

        if start + max_size > len(text):
            break

    return chunks
