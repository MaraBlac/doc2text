"""
Export processed text to files.
"""


def export_to_txt(chunks: list, output_path: str) -> None:
    """
    Export chunks to a text file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"## Chunk {i + 1}\n")
            f.write(chunk)
            f.write("\n\n")


def main():
    chunks = ["Chunk 1", "Chunk 2"]
    export_to_txt(chunks, "output.txt")
    print("Exported to output.txt")


if __name__ == "__main__":
    main()
