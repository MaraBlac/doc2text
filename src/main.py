#!/usr/bin/env python3
"""
Main entry point for doc2text pipeline.
"""
import sys
from .pipeline.orchestrator import run_pipeline


def main():
    """Main entry point."""
    if len(sys.argv) < 4:
        print("Usage: doc2text <input_pdf> <output_txt> <output_html>")
        print("\nExample:")
        print("  doc2text input.pdf output.txt output.html")
        return

    input_pdf = sys.argv[1]
    output_txt = sys.argv[2]
    output_html = sys.argv[3]

    # Run pipeline
    result = run_pipeline(input_pdf, output_txt)

    # Export HTML (placeholder)
    # This would be implemented in a separate module

    print(f"Done! Processed {result['chunks']} chunks")
    print(f"Output: {result['output']}")


if __name__ == "__main__":
    main()
