# Literature Review Assistant

A Python package that automates the process of analyzing research papers for literature reviews. It downloads papers from arXiv, analyzes them using Claude API, and generates summaries while considering the context of your project document.

## Features

- Downloads papers from arXiv links
- Analyzes papers using Claude API with context from your project document
- Generates individual paper summaries and a comprehensive meta-summary
- Caches analysis results to avoid redundant API calls
- Handles API rate limits automatically

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

The package will:
- Download PDFs to the `papers/` directory
- Cache analysis results in `.cache/` to avoid reprocessing
- Handle API rate limits with automatic retries
- Generate both individual summaries and a meta-summary

## Requirements

- Python 3.8+ (tested with 3.12)
- Claude API key
- Word document with project context 