from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat

# Initialize converter
doc_converter = DocumentConverter(
    allowed_formats=[
        InputFormat.PDF,
        InputFormat.DOCX,
        InputFormat.PPTX,
        InputFormat.HTML,
        InputFormat.MD,
    ]
)

# List of input file paths
input_files = [
    Path("path/to/file1.pdf"),
    Path("path/to/file2.docx"),
    Path("path/to/file3.pptx"),
]

# Batch convert
conv_results = doc_converter.convert_all(input_files)

# Export results
output_dir = Path("./markdown_outputs")
output_dir.mkdir(exist_ok=True)

for res in conv_results:
    if res.status.name == "SUCCESS":
        # Export to Markdown
        md_content = res.document.export_to_markdown()
        output_path = output_dir / f"{res.input.file.stem}.md"
        output_path.write_text(md_content, encoding="utf-8")
        print(f"Converted {res.input.file.name} to {output_path}")   