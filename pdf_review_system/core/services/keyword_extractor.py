import fitz  # PyMuPDF
from transformers import pipeline
import spacy 


# HuggingFace NER pipeline'ını başlat
ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")


def extract_entities_from_pdf(pdf_path):
    """
    PDF'ten yazar (PER) ve kurum (ORG) bilgilerini çıkarır.
    Dönüş: (authors, organizations)
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    entities = ner(text)

    authors = set()
    organizations = set()

    for ent in entities:
        if ent["score"] < 0.80:
            continue
        if ent["entity_group"] == "PER":
            authors.add(ent["word"].strip())
        elif ent["entity_group"] == "ORG":
            organizations.add(ent["word"].strip())

    return list(authors), list(organizations)


nlp = spacy.load("en_core_web_sm")

def extract_keywords_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    print("[DEBUG] Extracted PDF text (first 300 chars):", text[:300])

    # Spacy ile POS analizi
    spacy_doc = nlp(text)

    keywords = set()
    for token in spacy_doc:
        if token.pos_ in ["NOUN", "PROPN", "ADJ"] and not token.is_stop and token.is_alpha and len(token.text) > 2:
            keywords.add(token.text.lower())

    print(f"[DEBUG] Extracted {len(keywords)} keywords:", list(keywords)[:10])  # sadece ilk 10 kelimeyi göster

    return list(keywords)