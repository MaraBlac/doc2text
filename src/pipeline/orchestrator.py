"""
Pipeline orchestrator for coordinating processing steps.
"""


def run_pipeline(input_path: str, output_path: str):
    """
    Run the complete document processing pipeline.
    """
    from .extract_pdf import extract_from_pdf
    from .clean_text import clean_text
    from .chunk_text import chunk_text
    from .export_txt import export_to_txt

    # Extract PDF
    text_content = extract_from_pdf(input_path)

    # Clean text
    cleaned_text = clean_text(text_content)

    # Chunk text
    chunks = chunk_text(cleaned_text)

    # Export
    export_to_txt(chunks, output_path)

    return {
        "input": input_path,
        "output": output_path,
        "chunks": len(chunks)
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
