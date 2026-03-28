"""
File I/O utilities.
"""
import os


def read_file(path: str, encoding: str = "utf-8") -> str:
    """Read a file."""
    with open(path, "r", encoding=encoding) as f:
        return f.read()


def write_file(path: str, content: str, encoding: str = "utf-8") -> None:
    """Write to a file, creating parent directories."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        f.write(content)


def ensure_dir(path: str) -> None:
    """Ensure a directory exists."""
    os.makedirs(os.path.dirname(path), exist_ok=True)


def main():
    print("File I/O utilities loaded")


if __name__ == "__main__":
    main()
