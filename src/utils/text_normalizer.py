"""
Text normalization utilities.
"""
import unicodedata


def normalize_text(text: str) -> str:
    """Normalize text to standard form."""
    # Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # Lowercase
    text = text.lower()

    return text


def remove_special_chars(text: str) -> str:
    """Remove special characters while keeping basic punctuation."""
    import string

    # Keep alphanumeric and basic punctuation
    keep = set(string.ascii_letters + string.digits + ".,!?;:'\"()[]{}")

    result = []
    for char in text:
        if char in keep or char.isspace():
            result.append(char)

    return "".join(result)


def main():
    sample = "Héllo Wörld! 你好世界"
    print(normalize_text(sample))
    print(remove_special_chars(sample))


if __name__ == "__main__":
    main()
