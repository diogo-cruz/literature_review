# Literature Review Assistant

A Python package that automates the process of analyzing research papers for literature reviews. It downloads papers from arXiv, analyzes them using Claude API, and generates summaries while considering the context of your project document.

## Features

- Downloads papers from arXiv links
- Analyzes papers using Claude API with context from your project document
- Generates individual paper summaries
- Creates a comprehensive summary of all analyzed papers
- Integrates with Google Docs for project context

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

3. Set up environment variables:
Create a `.env` file with:
```
ANTHROPIC_API_KEY=your_claude_api_key
GOOGLE_CREDENTIALS_PATH=path_to_your_google_credentials.json
```

## Usage

```python
from literature_review import LiteratureReview

# Initialize with your Google Doc ID
review = LiteratureReview(google_doc_id="your_doc_id")

# Add arXiv papers to analyze
papers = [
    "https://arxiv.org/abs/2402.17764",
    "https://arxiv.org/abs/2402.17765"
]

# Run the analysis
review.analyze_papers(papers)
```

The summaries will be generated in the `summaries/` directory.

## Requirements

- Python 3.8+
- Claude API key
- Google Cloud credentials with Google Docs API access 