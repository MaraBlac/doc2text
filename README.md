# doc2text

PDF to text extraction and processing pipeline with OCR support.

## Features

- **PDF extraction** - Extract text from regular PDF documents
- **OCR for scanned PDFs** - Automatic OCR using Tesseract for image-based PDFs
- **Text cleaning and normalization** - Remove artifacts, normalize whitespace
- **Text chunking strategies** - Fixed-size chunking with overlap
- **Export to multiple formats** - TXT and HTML

## Installation

```bash
pip install -r requirements.txt
```

**Note:** Ensure Tesseract OCR is installed on your system:
- Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`
- Windows: Download from [tesseract-ocr.org](https://tesseract-ocr.org)

## Usage

```bash
# Run the pipeline (with OCR enabled by default)
python -m src.main input.pdf output.txt

# Run without OCR (for text-only PDFs)
python -m src.main input.pdf output.txt --no-ocr

# Specify OCR language
python -m src.main input.pdf output.txt --ocr-lang spa

# Export to HTML as well
python -m src.main input.pdf output.txt --html output.html
```

**Batch processing:**
```bash
python scripts/batch_process.py
```

## Scripts

```bash
# Run pipeline via script
./scripts/run_pipeline.sh
```

## Project Structure

```
doc2text/
├── configs/
├── data/
├── icm/
├── src/
├── tests/
└── scripts/
```
