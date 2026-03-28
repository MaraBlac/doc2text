#!/bin/bash
# Run the doc2text pipeline

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <input_pdf> <output_txt>"
    echo "Example: $0 input.pdf output.txt"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"

echo "Running pipeline: $INPUT -> $OUTPUT"

# Run the pipeline
python -m src.main "$INPUT" "$OUTPUT" "output.html"

echo "Done!"
