from pypdf import PdfReader

files = ["docs/2510.04618v3.pdf", "docs/2602.11988v2.pdf", "docs/2602.08316v3.pdf"]

for f in files:
    reader = PdfReader(f)
    print(f"\n{f} — {len(reader.pages)} pages")
    text_found = 0
    for page in reader.pages:
        try:
            t = page.extract_text()
            if t and len(t.strip()) > 20:
                text_found += 1
        except Exception:
            pass
    print(f"  Pages with usable text: {text_found}")