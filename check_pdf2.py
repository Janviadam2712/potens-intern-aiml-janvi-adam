import fitz  # PyMuPDF

files = ["docs/2510.04618v3.pdf", "docs/2602.11988v2.pdf", "docs/2602.08316v3.pdf"]

for f in files:
    doc = fitz.open(f)
    text_found = 0
    for page in doc:
        text = page.get_text()
        if text and len(text.strip()) > 20:
            text_found += 1
    print(f"{f} — {len(doc)} pages, {text_found} with usable text")