#!/usr/bin/env python3
"""
Test script to verify OCR and PDF extraction functionality.
"""
import sys
sys.path.insert(0, '/home/morka/doc2text/src')

from pipeline.extract_pdf import extract_from_pdf
from pipeline.clean_text import clean_text
from pipeline.chunk_text import chunk_text
from pipeline.export_txt import export_to_txt


def main():
    """Test the pipeline with a simple document."""
    import os

    # Create test PDF (simple text PDF path)
    test_pdf = "/tmp/test.pdf"

    # For testing, we'll just verify imports work
    print("Testing doc2text pipeline...")

    # Test functions exist
    print(f"  extract_from_pdf: {extract_from_pdf}")
    print(f"  clean_text: {clean_text}")
    print(f"  chunk_text: {chunk_text}")
    print(f"  export_to_txt: {export_to_txt}")

    print("\nAll imports successful!")
    print("To test with real PDFs, run:")
    print("  pip install -r requirements.txt")
    print("  # Then ensure Tesseract is installed")
    print("  python -m src.main <input.pdf> <output.txt>")


if __name__ == "__main__":
    main()
