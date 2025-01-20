#!/usr/bin/env python3
"""
Example script demonstrating how to use the literature review package.
Before running:
1. Install the package: pip install -e .
2. Create a .env file with your Claude API key:
   ANTHROPIC_API_KEY=your_claude_api_key
3. Place your project description in 'project.docx' in this directory
4. List your arXiv paper URLs in 'paper_list.txt' (one URL per line)
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from literature_review import LiteratureReview

def check_environment():
    """Check if all required files and environment variables are set."""
    load_dotenv()
    
    # Check for Claude API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\nError: ANTHROPIC_API_KEY not found in .env file")
        print("Please add your Claude API key to the .env file.")
        return False
    
    # Check for project document
    if not Path("project.docx").exists():
        print("\nError: project.docx not found")
        print("Please create a Word document named 'project.docx' with your project description.")
        return False
    
    # Check for paper list
    if not Path("paper_list.txt").exists():
        print("\nError: paper_list.txt not found")
        print("Please create paper_list.txt with your arXiv URLs (one per line).")
        print("Example format:")
        print("https://arxiv.org/abs/2402.17764")
        print("https://arxiv.org/abs/2402.17765")
        return False
        
    return True

def read_paper_list():
    """Read and validate arXiv URLs from paper_list.txt."""
    with open("paper_list.txt") as f:
        urls = [line.strip() for line in f if line.strip()]
    
    # Basic validation
    for url in urls:
        if not url.startswith("https://arxiv.org/"):
            raise ValueError(
                f"Invalid arXiv URL: {url}\n"
                "URLs should start with 'https://arxiv.org/'"
            )
    
    return urls

def main():
    if not check_environment():
        return
    
    try:
        papers = read_paper_list()
    except Exception as e:
        print(f"\nError reading paper_list.txt: {e}")
        return
    
    if not papers:
        print("\nError: No paper URLs found in paper_list.txt")
        return
    
    # Initialize the literature review system
    review = LiteratureReview()
    
    print(f"Starting analysis of {len(papers)} papers...")
    print("This may take a while depending on the number and size of papers.")
    
    # Run the analysis
    review.analyze_papers(papers)
    
    print("\nAnalysis complete! Check the 'summaries' directory for results:")
    print("- Individual paper summaries: paper_*.md")
    print("- Raw analysis data: paper_*_raw.json")
    print("- Meta-summary across all papers: meta_summary_*.md")

if __name__ == "__main__":
    main() 