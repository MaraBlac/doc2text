#!/usr/bin/env python3
"""
Main entry point for doc2text pipeline.
"""
import sys
import argparse
from .pipeline.orchestrator import run_pipeline
from .pipeline.export_txt import export_to_html


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Convert PDF to text files")
    parser.add_argument("input", help="Input PDF path")
    parser.add_argument("output", help="Output text path")
    parser.add_argument("--html", help="Optional output HTML path", default=None)
    parser.add_argument("--no-ocr", action="store_true", help="Disable OCR for scanned PDFs")
    parser.add_argument("--ocr-lang", default="eng", help="OCR language code (default: eng)")

    args = parser.parse_args()

    # Build config
    config = {
        "use_ocr": not args.no_ocr,
        "ocr_lang": args.ocr_lang
    }

    # Run pipeline
    result = run_pipeline(args.input, args.output, config)

    # Export HTML if requested
    if args.html:
        # Get full text content for HTML export
        from .extract_pdf import extract_from_pdf
        from .clean_text import clean_text
        text_content = extract_from_pdf(args.input, use_ocr=config["use_ocr"])
        cleaned_text = clean_text(text_content)
        export_to_html(cleaned_text, args.html)

    print(f"Done! Processed {result['chunks']} chunks")
    print(f"Output: {result['output']}")
