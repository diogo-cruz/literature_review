import os
import re
import csv
import glob
import arxiv
import pandas as pd
from typing import Dict, List, Optional

def extract_arxiv_id(url: str) -> str:
    """Extract arxiv ID from URL."""
    return url.split('/')[-1]

def get_paper_metadata(arxiv_id: str) -> Dict:
    """Fetch paper metadata from arxiv API."""
    try:
        client = arxiv.Client()
        search = arxiv.Search(id_list=[arxiv_id])
        paper = next(client.results(search))
        return {
            'Arxiv ID': arxiv_id,
            'Title': paper.title,
            'Authors': ', '.join(author.name for author in paper.authors)
        }
    except Exception as e:
        print(f"Error fetching metadata for {arxiv_id}: {e}")
        return {
            'Arxiv ID': arxiv_id,
            'Title': 'N/A',
            'Authors': 'N/A'
        }

def parse_summary_file(file_path: str) -> Dict:
    """Parse a markdown summary file to extract relevant sections."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Initialize default values
        summary = relevance = relation = extensions = reasoning = "N/A"

        # Extract sections using regex patterns
        # Handle various summary header formats:
        # - Summary:
        # - Summary of the paper:
        # - Summary of [paper name]:
        # - Summary of the Paper:
        if summary_match := re.search(r'(?:\*\*)?(?:Summary|Summary of (?:the )?(?:[Pp]aper|.*?)):.*?(?:\*\*)?\s*(.*?)(?=\n\n(?:\*\*)?[A-Z][a-zA-Z ]*(?:of (?:the )?(?:[Pp]aper|.*?))?:|\Z)', content, re.DOTALL):
            summary = summary_match.group(1).strip()
        
        # Handle variations of the relation section:
        # - Relation to your project:
        # - Key findings relevant to your project:
        # - Relevance to your project:
        if relation_match := re.search(r'(?:\*\*)?(?:Relation to|Key findings relevant to|Relevance to) .*?:.*?(?:\*\*)?\s*(.*?)(?=\n\n(?:\*\*)?[A-Z][a-zA-Z ]*(?:of (?:the )?(?:[Pp]aper|.*?))?:|\Z)', content, re.DOTALL):
            relation = relation_match.group(1).strip()
        
        # Handle "Potential Extensions" and variations (topics, extensions/topics)
        if extensions_match := re.search(r'(?:\*\*)?Potential (?:[Ee]xtensions|[Ee]xtensions/[Tt]opics|[Tt]opics|[Ee]xtensions.*?):.*?(?:\*\*)?\s*(.*?)(?=\n\n(?:\*\*)?[A-Z][a-zA-Z ]*(?:of (?:the )?(?:[Pp]aper|.*?))?:|\Z)', content, re.DOTALL):
            extensions = extensions_match.group(1).strip()
        
        # Find score and everything after it, handling trailing bold markers
        score_and_text = re.search(r'(?:\*\*)?(?:Relevance|Score).*?:.*?(?:\*\*)?\s*(\d+)/100\s*(?:\*\*)?(.*)', content, re.DOTALL)
        
        if score_and_text:
            relevance = score_and_text.group(1)
            full_text = score_and_text.group(2).strip()
            
            # Split into sentences and remove the last one if it ends with a question mark
            sentences = full_text.split('\n\n')
            if sentences and sentences[-1].strip().endswith('?'):
                full_text = '\n\n'.join(sentences[:-1])
            
            reasoning = full_text.strip()

        return {
            'Summary': summary,
            'Relation to project': relation,
            'Potential Extensions': extensions,
            'Relevance': relevance,
            'Reasoning': reasoning
        }
    except Exception as e:
        print(f"Error parsing summary file {file_path}: {e}")
        return {
            'Summary': 'N/A',
            'Relation to project': 'N/A',
            'Potential Extensions': 'N/A',
            'Relevance': 'N/A',
            'Reasoning': 'N/A'
        }

def main():
    # Read paper list
    with open('paper_list.txt', 'r') as f:
        paper_urls = [line.strip() for line in f if line.strip()]
    
    # Create a list to store all paper data
    papers_data = []
    
    # Process each paper
    for index, url in enumerate(paper_urls, 1):
        arxiv_id = extract_arxiv_id(url)
        
        # Get paper metadata
        metadata = get_paper_metadata(arxiv_id)
        
        # Find corresponding summary file
        summary_files = glob.glob(f'summaries/paper_{index}_*.md')
        summary_data = {}
        
        if summary_files:
            # Use the most recent summary if multiple exist
            latest_summary = max(summary_files)
            if not latest_summary.endswith('raw.json'):  # Ignore raw json files
                summary_data = parse_summary_file(latest_summary)
        
        # Combine all data
        paper_data = {
            'Index': index,
            **metadata,
            **summary_data
        }
        
        papers_data.append(paper_data)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(papers_data)
    df = df[[
        'Index', 'Arxiv ID', 'Title', 'Authors', 'Summary',
        'Relation to project', 'Potential Extensions', 'Relevance', 'Reasoning'
    ]]
    
    # Count N/A entries for each column
    na_counts = {col: df[col].eq('N/A').sum() for col in df.columns}
    
    # Save to CSV
    df.to_csv('paper_summaries.csv', index=False)
    
    # Print summary
    print(f"\nSuccessfully processed {len(papers_data)} papers. Results saved to paper_summaries.csv")
    print("\nN/A entries per column:")
    for col, count in na_counts.items():
        if count > 0:  # Only show columns with N/A entries
            print(f"- {col}: {count}")

if __name__ == "__main__":
    main() 