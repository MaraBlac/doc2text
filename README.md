# doc2text

Convert PDF documents to text files. Processes entire directories recursively while preserving the directory structure.

## Usage

```bash
# Batch processing - recursively processes all PDFs in input directory
doc2text INPUT_DIR/ OUTPUT_DIR/

# Example with your specific file:
doc2text /home/book/ /home/book/output/

# This will:
# - Scan /home/book/ and all subdirectories for .pdf files
# - Process each PDF with OCR (default)
# - Preserve directory structure in output
# - Save /home/book/mechanical engineering handbook II.pdf
#   as /home/book/output/mechanical engineering handbook II.txt
```

## Options

| Flag | Description |
|------|-------------|
| `--no-ocr` | Disable OCR for scanned PDFs |
| `--ocr-lang LANG` | Set OCR language (default: `eng`) |
| `--html PATH` | Generate HTML report at PATH |
| `--force-html` | Always generate HTML report |
| `--verbose` | Show detailed progress |

## Examples

### Basic batch processing
```bash
doc2text /home/book/ /home/book/output/
```

### Skip OCR (digital PDFs only)
```bash
doc2text /home/book/ /home/book/output/ --no-ocr
```

### Spanish OCR
```bash
doc2text /home/book/ /home/book/output/ --ocr-lang spa
```

### Generate HTML report
```bash
doc2text /home/book/ /home/book/output/ --html /home/book/report.html
```

### Verbose mode
```bash
doc2text /home/book/ /home/book/output/ --verbose
```

## Directory Structure

The tool preserves your directory structure:

```
/home/book/
├── mechanical engineering handbook II.pdf
└── chapter1/
    ├── intro.pdf
    └── sections/
        └── 1a.pdf

/home/book/output/
├── mechanical engineering handbook II.txt
└── chapter1/
    ├── intro.txt
    └── sections/
        └── 1a.txt
```

## Installation

```bash
pip install -r requirements.txt
# Then add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

## Prerequisites

- [tesseract](https://github.com/UB-Mannheim/tesseract/wiki) for OCR
- [poppler-utils](https://github.com/poppler/poppler-utils) (pdftotext, pdfimages)

## License

MIT
