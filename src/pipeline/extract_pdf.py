"""
PDF extraction logic with OCR support for scanned documents.
"""
import fitz  # pymupdf
from PIL import Image
from io import BytesIO


def extract_from_pdf(pdf_path: str, use_ocr: bool = True) -> str:
    """
    Extract text content from a PDF file.
    Handles both text-based PDFs and scanned (image-based) PDFs.

    Args:
        pdf_path: Path to the PDF file
        use_ocr: If True, enable OCR for image-based PDFs

    Returns:
        Extracted text content with page breaks
    """
    # Try to extract text layer first (for text-based PDFs)
    text_content = _extract_text_layer(pdf_path)

    # If no text or OCR requested, extract images and OCR
    if not text_content or use_ocr:
        image_content = _extract_and_ocr(pdf_path)
        if image_content:
            if text_content:
                return f"{text_content}\n\n--- OCR Content ---\n\n{image_content}"
            return image_content

    return text_content


def _extract_text_layer(pdf_path: str) -> str:
    """
    Extract text layer from PDF using pymupdf.
    Returns empty string if no text layer found.
    """
    try:
        doc = fitz.open(pdf_path)
        text_parts = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            if text.strip():
                text_parts.append(text)

        doc.close()
        return "\n\n--- Page Break ---\n\n".join(text_parts)
    except Exception:
        return ""


def _extract_and_ocr(pdf_path: str) -> str:
    """
    Extract images from PDF and perform OCR on them.
    """
    doc = fitz.open(pdf_path)
    all_ocr_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        mat = fitz.Matrix(2.0)
        pix = page.get_pixmap(matrix=mat)

        img_data = pix.tobytes("png")
        img = Image.open(BytesIO(img_data))

        try:
            text = Image.open(BytesIO(pix.tobytes("png"))).convert("RGB")
            import pytesseract
            text = pytesseract.image_to_string(img, lang='eng')
            if text.strip():
                all_ocr_text.append(text)
        except Exception:
            pass

    doc.close()
    return "\n\n--- Page Break ---\n\n".join(all_ocr_text)
