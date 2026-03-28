"""
Text cleaning logic.
"""
import unicodedata


def clean_text(text: str) -> str:
    """
    Clean extracted text.
    """
    # Normalize unicode
    text = unicodedata.normalize("NFKC", text)

    # Remove excessive whitespace
    text = " ".join(text.split())

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove page numbers (basic heuristic)
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if len(line) < 50:  # Skip short lines that might be page numbers
            continue
        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    return text


def main():
    sample = "  Hello   World  \n\n   Page 1   "
    print(clean_text(sample))


if __name__ == "__main__":
    main()
