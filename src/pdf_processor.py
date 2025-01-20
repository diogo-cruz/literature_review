from pathlib import Path
from pypdf import PdfReader

class PDFProcessor:
    def extract_text(self, pdf_path: Path) -> str:
        """Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        reader = PdfReader(str(pdf_path))
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        return text.strip() 