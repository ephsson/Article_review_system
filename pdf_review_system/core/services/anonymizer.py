import fitz  # PyMuPDF
from transformers import pipeline
import os

ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

def anonymize_pdf(input_path, output_path):
    doc = fitz.open(input_path)
    page = doc[0]
    words = page.get_text("words")
    
    lines = {}
    for w in words:
        key = (w[5], w[6])
        lines.setdefault(key, []).append(w)
    
    target_lines = list(lines.items())[:15]

    keywords = ["university", "institute", "department", "faculty", "college", "school", "center", "technology"]

    for _, line_words in target_lines:
        line_text = " ".join(w[4] for w in line_words)
        entities = ner(line_text)

        redact_line = any(ent["entity_group"] in ["PER", "ORG"] and ent["score"] >= 0.80 for ent in entities)
        if any(kw in line_text.lower() for kw in keywords):
            redact_line = True

        if redact_line:
            for w in line_words:
                rect = fitz.Rect(w[0], w[1], w[2], w[3])
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))

    doc.save(output_path)
    doc.close()
