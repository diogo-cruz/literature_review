import os
import arxiv
from pathlib import Path
import re

class ArxivDownloader:
    def __init__(self, papers_dir: str = "papers"):
        """Initialize the ArXiv downloader.
        
        Args:
            papers_dir: Directory to save downloaded papers
        """
        self.download_dir = Path(papers_dir)
        self.download_dir.mkdir(exist_ok=True)
        
    def _extract_arxiv_id(self, url: str) -> str:
        """Extract arXiv ID from URL.
        
        Args:
            url: arXiv paper URL
            
        Returns:
            arXiv paper ID
        """
        # Handle different URL formats
        patterns = [
            r"arxiv\.org/abs/(\d+\.\d+)",
            r"arxiv\.org/pdf/(\d+\.\d+)",
        ]
        
        for pattern in patterns:
            if match := re.search(pattern, url):
                return match.group(1)
        
        raise ValueError(f"Could not extract arXiv ID from URL: {url}")
        
    def download(self, url: str) -> Path:
        """Download a paper from arXiv.
        
        Args:
            url: arXiv paper URL
            
        Returns:
            Path to downloaded PDF file
        """
        paper_id = self._extract_arxiv_id(url)
        pdf_path = self.download_dir / f"{paper_id}.pdf"
        
        # Skip if already downloaded
        if pdf_path.exists():
            return pdf_path
            
        # Download paper
        search = arxiv.Search(id_list=[paper_id])
        paper = next(search.results())
        paper.download_pdf(filename=str(pdf_path))
        
        return pdf_path 