from docling.document_converter import DocumentConverter
from pathlib import Path as p

source = p("./books/G1-Dr-Dari.pdf")
converter = DocumentConverter()
result = converter.convert(source)
with open("output.md", "w", encoding="utf-8") as f:
    f.write(result.document.export_to_markdown())
print("Conversion successful! Output saved to output.md")