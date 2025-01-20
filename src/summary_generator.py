from pathlib import Path
import json
from datetime import datetime
from anthropic import Anthropic
import os
from dotenv import load_dotenv
from .config import Config

class SummaryGenerator:
    def __init__(self, output_dir: str = "summaries", config: Config = None):
        """Initialize the summary generator.
        
        Args:
            output_dir: Directory to save generated summaries
            config: Configuration object. If None, uses default config
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Claude client for meta-summary
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.config = config or Config()
        
    def generate_individual_summaries(self, analyses: list[dict]) -> None:
        """Generate individual markdown files for each paper analysis.
        
        Args:
            analyses: List of paper analysis results
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, analysis in enumerate(analyses, 1):
            output_path = self.output_dir / f"paper_{i}_{timestamp}.md"
            
            with open(output_path, "w") as f:
                f.write(analysis["analysis"])
                
            # Save raw data for reference
            raw_path = self.output_dir / f"paper_{i}_{timestamp}_raw.json"
            with open(raw_path, "w") as f:
                json.dump(analysis, f, indent=2)
                
    def generate_meta_summary(self, analyses: list[dict]) -> None:
        """Generate a meta-summary of all paper analyses.
        
        Args:
            analyses: List of paper analysis results
        """
        # Prepare prompt for meta-summary
        summaries = [analysis["analysis"] for analysis in analyses]
        prompt = f"""I have analyzed {len(summaries)} papers for my literature review. Below are the individual analyses. Please provide a comprehensive meta-summary that:
1. Identifies common themes and patterns
2. Highlights key differences and contradictions
3. Suggests potential research directions based on gaps in the literature
4. Provides a structured overview of the current state of research in this area

Individual Paper Analyses:

{chr(10).join(f"Paper {i+1}:\n{summary}\n" for i, summary in enumerate(summaries))}"""

        # Get meta-summary from Claude
        response = self.client.messages.create(
            model=self.config.claude_model,
            max_tokens=self.config.claude_max_tokens,
            temperature=self.config.claude_temperature,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extract the text content from the response
        meta_summary = response.content[0].text if isinstance(response.content, list) else response.content
        
        # Save meta-summary
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"meta_summary_{timestamp}.md"
        
        with open(output_path, "w") as f:
            f.write(meta_summary) 