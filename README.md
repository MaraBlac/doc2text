# doc2text

PDF to text extraction and processing pipeline.

## Features

- PDF extraction
- Text cleaning and normalization
- Text chunking strategies
- Export to multiple formats

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Run the pipeline
python -m src.main

# Run the batch processor
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
