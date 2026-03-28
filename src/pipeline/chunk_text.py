"""
Text chunking logic.
"""


def chunk_text(text: str, max_size: int = 500, overlap: int = 50) -> list:
    """
    Split text into chunks with overlap.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_size
        chunks.append(text[start:end])

        # If overlap > 0, advance past overlap
        if overlap > 0:
            start += max_size - overlap
        else:
            start += max_size

        # Ensure we don't exceed remaining text
        if start + max_size > len(text):
            chunks.append(text[start:])
            break

    return chunks


def main():
    text = "This is a sample text for chunking demonstration."
    print(chunk_text(text, max_size=10, overlap=2))


if __name__ == "__main__":
    main()
