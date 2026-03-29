#!/usr/bin/env python3
"""
doc2text - Convert PDF documents to text files.

Usage:
    doc2text INPUT.pdf OUTPUT.txt
    doc2text INPUT_DIR/ OUTPUT_DIR/

Creates INPUT/ directory for PDF files and OUTPUT/ directory for text files.
"""
import sys
import os
from pathlib import Path
import argparse

from .pipeline.orchestrator import run_pipeline
from .pipeline.export_txt import export_to_html


def get_input_dir(input_path: str) -> str:
    """Get input directory from path."""
    return str(Path(input_path).parent)


def get_output_dir(output_path: str) -> str:
    """Get output directory from path."""
    return str(Path(output_path).parent)


def process_single_pdf(input_path: str, output_path: str, config: dict = None):
    """Process a single PDF file."""
    return run_pipeline(input_path, output_path, config)


def process_batch(input_dir: str, output_dir: str, config: dict = None):
    """Process all PDFs in input directory."""
    import glob

    results = {"processed": 0, "failed": 0}

    # Find all PDFs in input directory
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))

    for pdf_path in sorted(pdf_files):
        pdf_name = os.path.basename(pdf_path)
        txt_name = pdf_name.replace(".pdf", ".txt")
        txt_path = os.path.join(output_dir, txt_name)

        try:
            result = run_pipeline(pdf_path, txt_path, config)
            results["processed"] += 1
            print(f"✓ Processed: {pdf_name} -> {txt_path}")
        except Exception as e:
            results["failed"] += 1
            print(f"✗ Failed: {pdf_name} - {e}")

    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert PDF documents to text files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  doc2text input.pdf output.txt              # Single file
  doc2text docs/ output/                      # Batch process
  doc2text docs/ output/ --no-ocr             # Skip OCR
  doc2text docs/ output/ --ocr-lang spa       # Spanish OCR
  doc2text docs/ output/ --html output.html   # Export HTML too
        """
    )

    parser.add_argument(
        "input",
        help="Input PDF file or directory containing PDFs"
    )
    parser.add_argument(
        "output",
        help="Output text file or directory for text files"
    )
    parser.add_argument(
        "--no-ocr",
        action="store_true",
        help="Disable OCR for scanned PDFs (default: enabled)"
    )
    parser.add_argument(
        "--ocr-lang",
        default="eng",
        help="OCR language code (default: eng)"
    )
    parser.add_argument(
        "--html",
        help="Optional output HTML path"
    )
    parser.add_argument(
        "--force-html",
        action="store_true",
        help="Always export HTML (ignores --html flag)"
    )

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    # Create INPUT and OUTPUT directories if they don't exist
    input_dir = Path(input_path)
    output_dir = Path(output_path)

    if not input_dir.exists():
        print(f"Error: Input directory '{input_path}' does not exist")
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create input directory if it doesn't exist (for batch processing)
    if input_dir.is_dir():
        input_dir.mkdir(parents=True, exist_ok=True)

    # Determine mode: batch or single file
    if input_dir.is_dir() and list(input_dir.glob("*.pdf")):
        # Batch processing mode
        config = {
            "use_ocr": not args.no_ocr,
            "ocr_lang": args.ocr_lang
        }
        results = process_batch(str(input_dir), str(output_dir), config)

        # Export HTML if requested
        if args.html or args.force_html:
            pdf_files = list(input_dir.glob("*.pdf"))
            for pdf_path in pdf_files:
                txt_name = pdf_path.name.replace(".pdf", ".html")
                html_path = output_dir / txt_name
                extract_text(input_path, html_path, args.html, args.force_html)

        print(f"\nBatch complete: {results['processed']} processed, {results['failed']} failed")
    else:
        # Single file mode
        # Create INPUT directory if needed
        if not (Path(input_path).exists()):
            input_dir.mkdir(parents=True, exist_ok=True)

        config = {
            "use_ocr": not args.no_ocr,
            "ocr_lang": args.ocr_lang
        }

        result = process_single_pdf(input_path, output_path, config)

        # Export HTML if requested
        if args.html or args.force_html:
            extract_text(input_path, args.html)

        print(f"\nDone! Processed {result['chunks']} chunks")
        print(f"Output: {result['output']}")


def extract_text(input_path: str, output_path: str, force=False, existing_path: str = None):
    """Extract text and save as HTML."""
    from .pipeline.extract_pdf import extract_from_pdf
    from .pipeline.clean_text import clean_text
    from .pipeline.chunk_text import chunk_text

    text_content = extract_from_pdf(input_path)
    cleaned_text = clean_text(text_content)

    # Generate HTML
    html_content = _text_to_html(cleaned_text)

    # Determine output path
    if existing_path:
        html_path = Path(existing_path)
    else:
        html_path = Path(output_path)

    # Don't overwrite if file exists (unless force)
    if html_path.exists() and not force:
        print(f"Skipping HTML export: {html_path} already exists")
        return

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Exported HTML: {html_path}")


def _text_to_html(text: str) -> str:
    """Convert text to HTML."""
    html_content = text.replace("\n", "<br>")
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; }}
        h1 {{ color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        .chunk {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9; }}
        .chunk::before {{ content: "Chunk "; font-weight: bold; color: #666; }}
        .chunk-number {{ display: block; }}
    </style>
</head>
<body>
<h1>Document</h1>
""" + html_content + """
</body>
</html>"""


if __name__ == "__main__":
    main()
