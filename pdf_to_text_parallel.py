import os
from multiprocessing import Pool, cpu_count
import fitz
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np

# --- CONFIG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = os.path.join(BASE_DIR, "INPUT_DIR")
OUTPUT_DIR = os.path.join(BASE_DIR, "OUTPUT_DIR")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Suppress MuPDF spam
fitz.TOOLS.mupdf_display_errors(False)


# --- TEXT EXTRACTION ---
def extract_text(pdf_path):
    try:
        doc = fitz.open(pdf_path, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        print(f"[PyMuPDF ERROR] {pdf_path} -> {e}")
        return ""


# --- IMAGE PREPROCESSING ---
def preprocess(img):
    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Better for bad scans
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )

    return thresh


# --- OCR ---
def ocr(pdf_path):
    try:
        images = convert_from_path(pdf_path, dpi=300)
        text = ""

        for img in images:
            processed = preprocess(img)
            text += pytesseract.image_to_string(processed)

        return text
    except Exception as e:
        print(f"[OCR ERROR] {pdf_path} -> {e}")
        return ""


# --- MAIN PROCESSING ---
def process_file(args):
    pdf_path, rel_path = args

    output_path = os.path.join(
        OUTPUT_DIR,
        os.path.splitext(rel_path)[0] + ".txt"
    )

    # Skip already processed files
    if os.path.exists(output_path):
        print(f"[SKIP] {rel_path}")
        return rel_path

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"[PROCESSING] {rel_path}")

    text = extract_text(pdf_path)

    # Smarter fallback
    if not text or len(text) < 200:
        print(f"[OCR] {rel_path}")
        text = ocr(pdf_path)

    if not text:
        print(f"[FAILED] {rel_path}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return rel_path


# --- FILE COLLECTION ---
def collect_files():
    tasks = []

    for root, _, files in os.walk(INPUT_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, INPUT_DIR)
                tasks.append((full_path, rel_path))

    return tasks


# --- MAIN ---
def main():
    tasks = collect_files()

    cores = max(1, cpu_count() - 1)

    print(f"Found {len(tasks)} PDFs")
    print(f"Using {cores} cores")

    with Pool(cores) as pool:
        pool.map(process_file, tasks)


if __name__ == "__main__":
    main()