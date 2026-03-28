"""
PDF extraction logic.
"""
import fitz  # pymupdf


def extract_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.
    """
    doc = fitz.open(pdf_path)
    text_parts = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        text_parts.append(text)

    doc.close()

    return "\n\n--- Page Break ---\n\n".join(text_parts)


def main():
    import sys
    if len(sys.argv) > 1:
        print(f"Extracting: {sys.argv[1]}")


if __name__ == "__main__":
    main()
