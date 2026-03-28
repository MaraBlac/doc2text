#!/usr/bin/env python3
"""
Batch processing for multiple PDF files.
"""
import os
import glob
from pathlib import Path
from src.pipeline.orchestrator import run_pipeline


def batch_process(input_dir: str, output_dir: str) -> dict:
    """
    Process all PDFs in input directory.
    """
    results = {"processed": 0, "failed": 0}

    # Find all PDFs
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))

    for pdf_path in pdf_files:
        pdf_name = os.path.basename(pdf_path)
        txt_name = pdf_name.replace(".pdf", ".txt")
        txt_path = os.path.join(output_dir, txt_name)

        try:
            run_pipeline(pdf_path, txt_path)
            results["processed"] += 1
            print(f"Processed: {pdf_name}")
        except Exception as e:
            results["failed"] += 1
            print(f"Failed: {pdf_name} - {e}")

    return results


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input directory with PDFs")
    parser.add_argument("output", help="Output directory for text files")
    args = parser.parse_args()

    results = batch_process(args.input, args.output)

    print(f"\nBatch complete:")
    print(f"  Processed: {results['processed']}")
    print(f"  Failed: {results['failed']}")


if __name__ == "__main__":
    main()
