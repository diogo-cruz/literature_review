# Literature Review Assistant

A Python package that automates the process of analyzing research papers for literature reviews. It downloads papers from arXiv, analyzes them using Claude API, and generates summaries while considering the context of your project document.

## Features

- Downloads papers from arXiv links
- Analyzes papers using Claude API with context from your project document
- Generates individual paper summaries and a comprehensive meta-summary
- Caches analysis results to avoid redundant API calls
- Handles API rate limits automatically
- Exports paper summaries to CSV for easy analysis

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd literature-review
```

2. Install the package:
```bash
pip install -e .
```

## Configuration

1. Create a `.env` file with your Claude API key:
```
ANTHROPIC_API_KEY=your_claude_api_key
```

2. Create `project.docx` in the project root directory:
   - This Word document should contain your project context
   - The context will be used to guide the analysis of each paper

3. List your papers in `paper_list.txt`:
   - One arXiv URL per line
   - Example:
   ```
   https://arxiv.org/abs/2402.17764
   https://arxiv.org/abs/2402.17765
   ```

4. (Optional) Configure settings in `config.toml`:
   ```toml
   [claude]
   model = "claude-3-5-sonnet-20241022"  # Choose Claude model
   max_tokens = 4000
   temperature = 0

   [files]
   project_doc = "project.docx"
   paper_list = "paper_list.txt"
   summaries_dir = "summaries"
   papers_dir = "papers"
   ```

## Usage

1. Run the analysis:
```bash
python run.py
```

2. Check the results in the `summaries` directory:
   - `paper_*_[timestamp].md`: Individual paper summaries
   - `meta_summary_[timestamp].md`: Comprehensive analysis across all papers
   - `paper_*_[timestamp]_raw.json`: Raw analysis data including paper text

3. Generate a CSV summary:
```bash
python gather_summaries.py
```
This will create `paper_summaries.csv` containing:
- Index: Paper's position in paper_list.txt
- Arxiv ID: Paper's arxiv identifier
- Title: Paper title
- Authors: Paper authors
- Summary: Brief summary of the paper
- Relation to project: How the paper relates to your project
- Potential Extensions: Possible future work or extensions
- Relevance: Numerical relevance score (0-100)

The package will:
- Download PDFs to the `papers/` directory
- Cache analysis results in `.cache/` to avoid reprocessing
- Handle API rate limits with automatic retries
- Generate both individual summaries and a meta-summary
- Export structured data to CSV for further analysis

## Requirements

- Python 3.8+ (tested with 3.12)
- Claude API key
- Word document with project context 

## Utility Scripts

### gather_summaries.py

A script that collects and organizes all paper summaries into a single CSV file. It:
- Extracts metadata from arXiv for each paper
- Parses the markdown summaries to extract key sections
- Combines all information into a structured CSV with fields:
  - Index
  - Arxiv ID
  - Title
  - Authors
  - Summary
  - Relation to project
  - Potential Extensions
  - Relevance score
  - Reasoning for the score

Usage:
```bash
python gather_summaries.py
```

### collect_recent_papers.py

A script that collects recent Machine Learning papers from arXiv's cs.LG category. Features:
- Collects papers from a specified time range (default: last 180 days)
- Uses date chunking to handle API limits gracefully
- Saves papers to CSV with metadata including:
  - Title
  - Authors
  - Abstract
  - Publication date
  - arXiv ID
  - URL

Usage:
```bash
python collect_recent_papers.py
```

The output is saved to `recent_ml_papers.csv`. 