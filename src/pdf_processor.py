from pathlib import Path
from pypdf import PdfReader
import logging
from typing import Optional

class PDFProcessor:
    def extract_text(self, pdf_path: Path) -> str:
        """Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content. Returns error message if extraction fails.
        """
        try:
            reader = PdfReader(str(pdf_path))
            text = ""
            failed_pages = 0
            total_pages = len(reader.pages)
            
            for page_num, page in enumerate(reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    else:
                        failed_pages += 1
                except (TypeError, AttributeError, KeyError) as e:
                    failed_pages += 1
                    continue
            
            if failed_pages > 0:
                print(f"\nWarning: Failed to extract text from {failed_pages}/{total_pages} pages in {pdf_path.name}")
                
            text = text.strip()
            if not text:
                print(f"\nWarning: No text could be extracted from {pdf_path.name}")
                return f"[Error: Could not extract text from PDF file {pdf_path.name}]"
                
            if failed_pages == total_pages:
                return f"[Error: Failed to extract text from any page in {pdf_path.name}]"
                
            return text
            
        except Exception as e:
            print(f"\nError processing PDF {pdf_path.name}: {str(e)}")
            return f"[Error: Failed to process PDF file {pdf_path.name}: {str(e)}]" 