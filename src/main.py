#!/usr/bin/env python3
"""
doc2text - Convert PDF documents to text files.

Usage:
    doc2text INPUT_DIR/ OUTPUT_DIR/   # Batch process all PDFs recursively, preserving directory structure
    doc2text input.pdf output.txt     # Single file
"""
import sys
import os
from pathlib import Path
import argparse

from .pipeline.orchestrator import run_pipeline


def process_recursive(input_dir: str, output_dir: str, config: dict = None):
    """
    Process all PDFs recursively, preserving directory structure.

    For each PDF at INPUT_DIR/path/to/file.pdf, creates:
    OUTPUT_DIR/path/to/file.txt
    """
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    results = {"processed": 0, "failed": 0}

    # Walk through all subdirectories
    for root, dirs, files in os.walk(input_dir):
        # Sort for consistent ordering
        dirs.sort()
        files.sort()

        for filename in files:
            if filename.endswith(".pdf"):
                input_pdf = Path(root) / filename
                # Get relative path from input directory
                rel_path = input_pdf.relative_to(input_path)
                # Create corresponding output path preserving structure
                output_txt = output_path / rel_path.with_suffix(".txt")

                # Create parent directories
                output_txt.parent.mkdir(parents=True, exist_ok=True)

                try:
                    result = run_pipeline(str(input_pdf), str(output_txt), config)
                    results["processed"] += 1
                    rel_str = str(rel_path).replace(".pdf", ".txt")
                    print(f"✓ Processed: {rel_str}")
                except Exception as e:
                    results["failed"] += 1
                    rel_str = str(rel_path)
                    print(f"✗ Failed: {rel_str} - {e}")

    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert PDF documents to text files (batch mode with recursive processing)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  doc2text /home/book/ /home/book/output/   # Process all PDFs in /home/book/ recursively
  doc2text docs/ output/                     # Batch process docs/ directory
  doc2text docs/ output/ --no-ocr            # Skip OCR
  doc2text docs/ output/ --ocr-lang spa      # Spanish OCR
        """
    )

    parser.add_argument(
        "input",
        help="Input directory containing PDF files"
    )
    parser.add_argument(
        "output",
        help="Output directory for text files"
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
        help="Optional output HTML path (flat structure)"
    )
    parser.add_argument(
        "--force-html",
        action="store_true",
        help="Always export HTML (ignores --html flag)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed progress"
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    # Verify input directory exists
    if not input_path.exists():
        print(f"Error: Input directory '{args.input}' does not exist")
        sys.exit(1)

    if not input_path.is_dir():
        print(f"Error: '{args.input}' is not a directory. Use doc2text input.pdf output.txt for single files.")
        sys.exit(1)

    # Prepare config
    config = {
        "use_ocr": not args.no_ocr,
        "ocr_lang": args.ocr_lang
    }

    if args.verbose:
        print(f"Scanning directory: {input_path}")
        pdf_count = sum(1 for _ in input_path.rglob("*.pdf"))
        print(f"Found {pdf_count} PDF file(s)")

    print(f"Processing PDFs from {input_path} to {output_path}...")
    print("-" * 60)

    results = process_recursive(str(input_path), str(output_path), config)

    print("-" * 60)
    print(f"\nBatch complete: {results['processed']} processed, {results['failed']} failed")

    if args.html or args.force_html:
        html_output = args.html or str(output_path / "index.html")
        html_path = Path(html_output)
        html_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"\nGenerating HTML report: {html_path}")
        _generate_html_report(output_path, html_path)


def _generate_html_report(output_dir: Path, html_path: Path):
    """Generate HTML report from all text files."""
    from .pipeline.export_txt import export_to_html

    text_files = list(output_dir.glob("**/*.txt"))

    if not text_files:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write("<html><body><p>No text files found.</p></body></html>")
        return

    # Collect all content
    chunks = []
    for i, txt_file in enumerate(sorted(text_files)):
        try:
            with open(txt_file, "r", encoding="utf-8") as f:
                content = f.read()
                chunks.append(f"<div class='doc'><h2>{txt_file.name}</h2>{content}</div>")
        except Exception as e:
            print(f"Warning: Could not read {txt_file}: {e}")

    if not chunks:
        html_content = "<html><body><p>No content found.</p></body></html>"
    else:
        html_content = "<html><head><style>body{font-family:sans-serif;margin:20px;}.doc{margin:20px 0;border:1px solid #ddd;padding:15px;border-radius:5px;}</style></head><body>"
        html_content += "<h1>Processed Documents</h1>"
        html_content += "".join(chunks)
        html_content += "</body></html>"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML report generated: {html_path}")


if __name__ == "__main__":
    main()
