# parser.py
import docx2txt
from pypdf import PdfReader

def extract_text_from_pdf(file_buffer):
    """Extracts raw text from an uploaded PDF file buffer."""
    try:
        reader = PdfReader(file_buffer)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file_buffer):
    """Extracts raw text from an uploaded DOCX file buffer."""
    try:
        text = docx2txt.process(file_buffer)
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

# CRITICAL: Make sure this name matches perfectly!
def get_document_text(uploaded_file):
    """Determines file type and routes it to the correct parser."""
    if uploaded_file is None:
        return ""
        
    file_name = uploaded_file.name.lower()
    
    if file_name.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file)
    elif file_name.endswith('.docx'):
        return extract_text_from_docx(uploaded_file)
    else:
        return "Unsupported file format."