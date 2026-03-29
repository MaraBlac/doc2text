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


def export_to_html(text: str, output_path: str) -> None:
    """
    Export text content to HTML file.
    """
    # Replace newlines with <br> and wrap in basic HTML structure
    html_content = text.replace("\n", "<br>")
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        h1 {{ color: #333; }}
        .chunk {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
    </style>
</head>
<body>
<h1>Document</h1>
""" + html_content + """
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def main():
    chunks = ["Chunk 1", "Chunk 2"]
    export_to_txt(chunks, "output.txt")
    print("Exported to output.txt")


if __name__ == "__main__":
    main()
