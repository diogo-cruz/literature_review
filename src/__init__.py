from .arxiv_downloader import ArxivDownloader
from .claude_analyzer import ClaudeAnalyzer
from .docx_handler import DocxHandler
from .pdf_processor import PDFProcessor
from .summary_generator import SummaryGenerator
from .config import Config

class LiteratureReview:
    def __init__(self, config: Config = None):
        """Initialize the Literature Review system.
        
        Args:
            config: Configuration object. If None, uses default config.
        """
        self.config = config or Config()
        self.doc_handler = DocxHandler(self.config.project_doc)
        self.downloader = ArxivDownloader(papers_dir=self.config.papers_dir)
        self.pdf_processor = PDFProcessor()
        self.analyzer = ClaudeAnalyzer(config=self.config)
        self.summary_generator = SummaryGenerator(output_dir=self.config.summaries_dir)
        
    def analyze_papers(self, arxiv_links: list[str]) -> None:
        """Analyze a list of papers from arXiv.
        
        Args:
            arxiv_links: List of arXiv paper URLs to analyze
        """
        # Get project context
        project_context = self.doc_handler.get_document_content()
        
        summaries = []
        for link in arxiv_links:
            # Download paper
            pdf_path = self.downloader.download(link)
            
            # Process PDF
            paper_text = self.pdf_processor.extract_text(pdf_path)
            
            # Analyze with Claude
            summary = self.analyzer.analyze_paper(
                paper_text=paper_text,
                project_context=project_context
            )
            summaries.append(summary)
        
        # Generate final summaries
        self.summary_generator.generate_individual_summaries(summaries)
        self.summary_generator.generate_meta_summary(summaries) 