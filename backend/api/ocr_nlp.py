import pytesseract
from pdf2image import convert_from_path
from transformers import pipeline

nlp_pipeline = pipeline("ner", model="dslim/bert-base-NER")

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def extract_legal_clauses(text):
    results = nlp_pipeline(text)
    clauses = [res["word"] for res in results if res["entity"] in ["B-ORG", "B-MISC"]]
    return clauses
