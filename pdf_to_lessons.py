import json
import os
import re
import argparse
from pathlib import Path

# Avoid a PaddlePaddle oneDNN execution error on this CPU/runtime combination.
os.environ.setdefault("PADDLE_PDX_ENABLE_MKLDNN_BYDEFAULT", "false")
os.environ.setdefault("PADDLE_PDX_DISABLE_MKLDNN_MODEL_BL", "true")

try:
    from paddleocr import PaddleOCR
except ImportError as exc:
    raise SystemExit(
        "PaddleOCR is not installed. Run: "
        "python -m pip install paddleocr paddlepaddle"
    ) from exc

# Lesson detection is disabled because each PDF is now saved as one Markdown file.
# LESSON_MARKER_REGEX = re.compile(
#     r"(درس|فصل)\s*(\d+|اول|دوم|سوم|چهارم|پنجم|ششم|هفتم|هشتم|نهم|دهم)",
#     re.IGNORECASE | re.UNICODE
# )

def sanitize_filename(name: str) -> str:
    """Removes characters that are invalid for filenames."""
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def save_content(folder: Path, filename: str, content: str):
    """Saves the content to a markdown file in the specified folder."""
    if not content.strip():
        return

    file_path = folder / f"{sanitize_filename(filename)}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved: {file_path.name}")

def result_to_text(result) -> str:
    """Extract recognized lines from a PaddleOCR result."""
    data = result.json
    if callable(data):
        data = data()
    if isinstance(data, str):
        data = json.loads(data)

    if not isinstance(data, dict):
        return ""

    page_data = data.get("res", data)
    texts = page_data.get("rec_texts", [])
    return "\n".join(text.strip() for text in texts if text.strip())


def extract_pdf_text(pdf_path: Path, ocr: PaddleOCR) -> str:
    """OCR a PDF and return its recognized text in page order."""
    pages = []
    for page_number, result in enumerate(ocr.predict(input=str(pdf_path)), start=1):
        page_text = result_to_text(result)
        if page_text:
            pages.append(page_text)
        print(f"OCR page {page_number}: {len(page_text)} characters")
    return "\n\n".join(pages)


def process_pdf(pdf_path: Path, output_folder: Path, ocr: PaddleOCR):
    """OCR a PDF and split the recognized text into lessons."""
    print(f"Processing {pdf_path.name}...")

    try:
        text = extract_pdf_text(pdf_path, ocr)
        pdf_stem = pdf_path.stem

        #  matches = list(LESSON_MARKER_REGEX.finditer(text))
        # if not matches:
        #     save_content(output_folder, f"{pdf_stem}_introduction", text)
        #     print("No lesson headings detected; saved all OCR text as introduction.")
        #     return

        # if matches[0].start() > 0:
        #     save_content(
        #         output_folder,
        #         f"{pdf_stem}_introduction",
        #         text[:matches[0].start()],
        #     )

        # for index, match in enumerate(matches):
        #     end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        #     lesson_name = sanitize_filename(match.group(0))
        #     save_content(
        #         output_folder,
        #         f"{pdf_stem}_{lesson_name}",
        #         text[match.start():end],
        #     )


        # Lesson separation is disabled. Save the complete PDF as one Markdown file.
        save_content(output_folder, pdf_stem, text)
        print(f"Saved complete PDF as {pdf_stem}.md")

    except Exception as e:
        print(f"Error processing {pdf_path.name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Split PDF lessons into Markdown using Docling")
    parser.add_argument("--input", type=str, required=True, help="Path to input folder containing PDFs")
    parser.add_argument("--output", type=str, required=True, help="Path to output folder for Markdown files")
    parser.add_argument("--lang", default="ar", help="PaddleOCR language code (default: ar for Arabic)")

    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.is_dir():
        print(f"Error: Input path {input_dir} is not a directory.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Initializing PaddleOCR with language: {args.lang}...")
    ocr = PaddleOCR(
        lang=args.lang,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )

    # Process all PDFs
    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in input directory.")
        return

    print(f"Found {len(pdf_files)} PDF files.")
    for pdf_file in pdf_files:
        process_pdf(pdf_file, output_dir, ocr)

    print("Processing complete.")

if __name__ == "__main__":
    main()


# python pdf_to_lessons.py --input "./books" --output "./outputs" --lang "fa"