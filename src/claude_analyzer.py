import os
from pathlib import Path
import time
from typing import Optional
from anthropic import Anthropic, RateLimitError
from dotenv import load_dotenv
from .config import Config
from .cache import PromptCache

class ClaudeAnalyzer:
    def __init__(self, config: Config = None):
        """Initialize the Claude analyzer.
        
        Args:
            config: Configuration object. If None, uses default config.
        """
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.config = config or Config()
        self.cache = PromptCache()
        
        # Load analysis prompt template
        prompt_path = Path(__file__).parent.parent / "analysis_prompt.txt"
        with open(prompt_path) as f:
            self.prompt_template = f.read()
        
        # Rate limiting settings
        self.last_request_time = 0
        self.min_request_interval = 2  # seconds between requests
        self.max_retries = 5
        self.base_retry_delay = 60  # seconds
        
    def _call_claude_api(self, prompt: str, retry_count: int = 0) -> Optional[str]:
        """Call Claude API with rate limiting and retries.
        
        Args:
            prompt: The prompt to send to Claude
            retry_count: Current retry attempt number
            
        Returns:
            Analysis text if successful, None if all retries failed
        """
        # Ensure minimum time between requests
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
            
        try:
            response = self.client.messages.create(
                model=self.config.claude_model,
                max_tokens=self.config.claude_max_tokens,
                temperature=self.config.claude_temperature,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            self.last_request_time = time.time()
            return response.content[0].text if isinstance(response.content, list) else response.content
            
        except RateLimitError as e:
            if retry_count >= self.max_retries:
                print(f"\nError: Maximum retries ({self.max_retries}) exceeded.")
                print("Consider reducing batch size or increasing delay between requests.")
                return None
                
            retry_delay = self.base_retry_delay * (2 ** retry_count)  # Exponential backoff
            print(f"\nRate limit hit. Waiting {retry_delay} seconds before retry {retry_count + 1}/{self.max_retries}...")
            time.sleep(retry_delay)
            return self._call_claude_api(prompt, retry_count + 1)
        
    def analyze_paper(self, paper_text: str, project_context: str, paper_id: str) -> dict:
        """Analyze a paper using Claude API.
        
        Args:
            paper_text: Extracted text content from the paper
            project_context: Content from the project's document
            paper_id: arXiv paper ID for caching
            
        Returns:
            Dictionary containing the analysis results
        """
        # Prepare the prompt
        prompt = f"""Project Context:
{project_context}

Paper Content:
{paper_text}

{self.prompt_template}"""

        # Check cache first
        if cached_result := self.cache.get(paper_id, prompt):
            print(f"Using cached analysis for paper {paper_id}")
            return cached_result
            
        print(f"Analyzing paper {paper_id}...")
        
        # Get Claude's analysis with retries
        analysis_text = self._call_claude_api(prompt)
        if analysis_text is None:
            raise RuntimeError(f"Failed to analyze paper {paper_id} after maximum retries")
        
        result = {
            "analysis": analysis_text,
            "paper_text": paper_text,
            "project_context": project_context
        }
        
        # Cache the result
        self.cache.save(paper_id, prompt, result)
        
        return result 