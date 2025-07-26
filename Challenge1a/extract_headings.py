import fitz  # PyMuPDF
import json
import re
import os

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                text = " ".join(span["text"] for span in line["spans"]).strip()
                if not text:
                    continue

                if re.match(r'^\d+\.\s+', text):
                    level = "H1"
                elif re.match(r'^\d+\.\d+\.\s+', text):
                    level = "H2"
                elif re.match(r'^\d+\.\d+\.\d+\.\s+', text):
                    level = "H3"
                else:
                    continue

                outline.append({
                    "level": level,
                    "text": text,
                    "page": page_num + 1
                })

    result = {
        "title": os.path.basename(pdf_path).replace(".pdf", ""),
        "outline": outline
    }

    return result

if __name__ == "__main__":
    input_path = "input/sample.pdf"
    output_path = "output/sample.json"
    os.makedirs("output", exist_ok=True)

    data = extract_headings(input_path)

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
