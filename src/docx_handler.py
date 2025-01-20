from pathlib import Path
from docx import Document

class DocxHandler:
    def __init__(self, docx_path: str = "project.docx"):
        """Initialize the Word document handler.
        
        Args:
            docx_path: Path to the Word document containing project context
        """
        self.docx_path = Path(docx_path)
        
    def get_document_content(self) -> str:
        """Get the content of the Word document.
        
        Returns:
            The text content of the document
        """
        if not self.docx_path.exists():
            raise FileNotFoundError(
                f"Project document not found at {self.docx_path}. "
                "Please make sure 'project.docx' exists in the project root."
            )
            
        doc = Document(self.docx_path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs) 