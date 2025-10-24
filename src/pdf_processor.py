import os
import pymupdf
import logging

class PDFprocessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_text(self, pdf_path):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError('')
        try:
            text = ""
            with pymupdf.open(pdf_path, filetype='text') as file:
                for page in file:
                    text += page.get_text() + '\n'
            return text.strip()
        except:
            self.logger.error('Failed to extract text from file')
            return
        
    def get_info(self, pdf_path):
        try:
            with pymupdf.open(pdf_path, filetype='text') as file:
                return {
                    'num_pages': file.get_page_numbers(),
                    'file_size': os.path.getsize(pdf_path)
                }
        except:
            pass