# PDF to Markdown Converter

This project provides tools for converting PDF documents into Markdown format, specifically designed for educational content. It leverages powerful OCR and document conversion libraries to handle various input formats and languages.

## Features

- **Batch Conversion**: Convert multiple files (PDF, DOCX, PPTX, HTML, MD) to Markdown using `docling`.
- **OCR-based Extraction**: Extract text from PDFs using `PaddleOCR`, which is particularly effective for languages like Arabic and Persian.
- **Lesson Splitting**: Ability to process PDFs and save the output as Markdown files.

## Getting Started

### Prerequisites

- Python 3.9+

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   ```

2. **Create a virtual environment** (Recommended):
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install docling paddleocr paddlepaddle
   ```

*Note: For GPU acceleration with PaddleOCR, install `paddlepaddle-gpu` instead of `paddlepaddle`.*

## Usage

### General Conversion (`multiple.py`)

This script allows you to convert various document types to Markdown.

```bash
python multiple.py
```
*(Note: You may need to update the `input_files` list inside `multiple.py` to point to your local files.)*

### OCR-based Extraction (`pdf_to_lessons.py`)

This script is ideal for PDFs that require OCR, especially for non-Latin scripts.

```bash
python pdf_to_lessons.py --input "./books" --output "./outputs" --lang "fa"
```

**Arguments:**
- `--input`: Path to the folder containing PDF files.
- `--output`: Path to the folder where Markdown files will be saved.
- `--lang`: PaddleOCR language code (e.g., `ar` for Arabic, `fa` for Persian). Defaults to `ar`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
