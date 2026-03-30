# doc2text

A parallel PDF to text converter that extracts text from PDFs using two approaches:
- **PyMuPDF**: For text-based PDFs (fast, preserves formatting)
- **Tesseract OCR**: For scanned/image-based PDFs

## Features

- ✅ Multi-threaded processing (uses all but 1 CPU core)
- ✅ Automatic fallback: tries PyMuPDF first, falls back to OCR if needed
- ✅ Image preprocessing with adaptive thresholding for better OCR
- ✅ GUI and CLI support
- ✅ Skips already-processed files

## Installation

```bash
# Install dependencies
pip install fitz pytesseract pdf2image opencv-python numpy
```

> **Note**: Install Tesseract OCR on your system first:
> - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
> - macOS: `brew install tesseract`
> - Windows: Download from [tesseract-ocr.org](https://tesseract-ocr.org)

## Usage

### Command Line

```bash
# Run the script
python pdf_to_text_parallel.py
```

Place your PDFs in the `INPUT_DIR` folder (relative to project root) and extracted text files will appear in `OUTPUT_DIR`.

### GUI

```bash
python gui_runner.py
```

Click "Start Processing" to begin conversion.

## Project Structure

```
doc2text/
├── INPUT_DIR/          # Place PDFs here
├── OUTPUT_DIR/         # Extracted text appears here
├── pdf_to_text_parallel.py  # Main conversion script
├── gui_runner.py        # GUI launcher
└── README.md
```

## How It Works

1. **Text Extraction**: Uses PyMuPDF to extract text from PDFs
2. **OCR Fallback**: If text extraction fails or returns short content, switches to OCR
3. **Preprocessing**: Converts images to grayscale and applies adaptive thresholding
4. **OCR**: Uses Tesseract to read text from images
5. **Output**: Saves extracted text to `.txt` files in `OUTPUT_DIR`

## License

MIT
