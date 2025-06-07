import pytesseract
from PIL import Image
import fitz  
from langchain.tools import tool
import logging

@tool
def extract_structured_text_from_pdf(file_path: str) -> str:
    """Extracts text from image-based PDFs using OCR, preserving basic structure."""
    try:
        pdf_document = fitz.open(file_path)
        extracted_text = ""

        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap(dpi=300) 
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            ocr_text = pytesseract.image_to_string(img, config='--psm 6')

            extracted_text += f"\n--- Page {page_number + 1} ---\n" + ocr_text.strip() + "\n"

        return extracted_text

    except Exception as e:
        logging.error(f"[extract_structured_text_from_pdf] Error extracting text: {e}")
        return "Sorry, there was an error processing your PDF. Please try again with a valid file."
