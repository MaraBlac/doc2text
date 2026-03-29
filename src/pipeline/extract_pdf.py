"""
PDF extraction logic with OCR support for scanned documents.
"""
import fitz  # pymupdf
from PIL import Image
import pytesseract
from io import BytesIO


def extract_from_pdf(pdf_path: str, use_ocr: bool = True) -> str:
    """
    Extract text content from a PDF file.
    Handles both text-based PDFs and scanned (image-based) PDFs.

    Args:
        pdf_path: Path to the PDF file
        use_ocr: If True, enable OCR for image/text on images.
                  If False, extract only text layers from text-based PDFs.

    Returns:
        Extracted text content with page breaks
    """
    # First, try to extract text layer (for text-based PDFs)
    text_content = _extract_text_layer(pdf_path)

    # If no text was extracted, or if OCR is requested, extract images and OCR
    if not text_content or use_ocr:
        image_content = _extract_and_ocr(pdf_path)
        if image_content:
            # Combine text and OCR results
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
            # Check if page has actual text (not empty)
            if text.strip():
                text_parts.append(text)

        doc.close()

        if text_parts:
            return "\n\n--- Page Break ---\n\n".join(text_parts)
        return ""
    except Exception as e:
        return ""


def _extract_and_ocr(pdf_path: str) -> str:
    """
    Extract images from PDF and perform OCR on them.
    """
    doc = fitz.open(pdf_path)
    all_ocr_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Get page as high-quality pixmap
        mat = fitz.Matrix(2.0)  # 2x zoom for better OCR quality
        pix = page.get_pixmap(matrix=mat)

        # Convert to PIL Image
        img_data = pix.tobytes("png")
        img = Image.open(BytesIO(img_data))

        # Perform OCR
        try:
            text = pytesseract.image_to_string(img, lang='eng')
            if text.strip():
                all_ocr_text.append(text)
        except Exception as e:
            print(f"OCR error on page {page_num + 1}: {e}")

    doc.close()

    if all_ocr_text:
        return "\n\n--- Page Break ---\n\n".join(all_ocr_text)
    return ""


def main():
    import sys
    if len(sys.argv) > 1:
        print(f"Extracting: {sys.argv[1]}")


if __name__ == "__main__":
    main()
