import os
from pdfminer.high_level import extract_text
import docx

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        return extract_text(pdf_path)
    except Exception as e:
        return ""

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(docx_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        return ""

def resume_parser(file_path):
    """Parses resume file and returns text content."""
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        return ""
