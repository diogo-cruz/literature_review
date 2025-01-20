import os
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv
from .config import Config

class ClaudeAnalyzer:
    def __init__(self, config: Config = None):
        """Initialize the Claude analyzer.
        
        Args:
            config: Configuration object. If None, uses default config.
        """
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.config = config or Config()
        
        # Load analysis prompt template
        prompt_path = Path(__file__).parent.parent / "analysis_prompt.txt"
        with open(prompt_path) as f:
            self.prompt_template = f.read()
        
    def analyze_paper(self, paper_text: str, project_context: str) -> dict:
        """Analyze a paper using Claude API.
        
        Args:
            paper_text: Extracted text content from the paper
            project_context: Content from the project's document
            
        Returns:
            Dictionary containing the analysis results
        """
        # Prepare the prompt
        prompt = f"""Project Context:
{project_context}

Paper Content:
{paper_text}

{self.prompt_template}"""
        
        # Get Claude's analysis
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
        analysis_text = response.content[0].text if isinstance(response.content, list) else response.content
        
        return {
            "analysis": analysis_text,
            "paper_text": paper_text,
            "project_context": project_context
        } 