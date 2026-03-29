"""
Pipeline orchestrator for coordinating processing steps.
"""


def run_pipeline(input_path: str, output_path: str, config: dict = None):
    """
    Run the complete document processing pipeline.

    Args:
        input_path: Path to input PDF file
        output_path: Path for output text file
        config: Optional config dict with keys:
            - use_ocr: bool, enable OCR for scanned PDFs
            - ocr_lang: str, language code for OCR (default: 'eng')
    """
    from .extract_pdf import extract_from_pdf
    from .clean_text import clean_text
    from .chunk_text import chunk_text
    from .export_txt import export_to_txt

    # Extract PDF (with OCR if configured)
    use_ocr = config.get('use_ocr', True)
    ocr_lang = config.get('ocr_lang', 'eng') if config else 'eng'
    text_content = extract_from_pdf(input_path, use_ocr=use_ocr)

    # Clean text
    cleaned_text = clean_text(text_content)

    # Chunk text
    chunks = chunk_text(cleaned_text)

    # Export
    export_to_txt(chunks, output_path)

    return {
        "input": input_path,
        "output": output_path,
        "chunks": len(chunks),
        "used_ocr": use_ocr
    }


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input PDF path")
    parser.add_argument("output", help="Output text path")
    args = parser.parse_args()

    result = run_pipeline(args.input, args.output)
    print(f"Processed: {result['input']} -> {result['output']}")
    print(f"Chunks created: {result['chunks']}")


if __name__ == "__main__":
    main()
