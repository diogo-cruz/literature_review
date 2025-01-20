import tomli
from pathlib import Path

class Config:
    def __init__(self, config_path: str = "config.toml"):
        """Initialize configuration.
        
        Args:
            config_path: Path to the TOML config file
        """
        self.config_path = Path(config_path)
        self.load_config()
        
    def load_config(self):
        """Load configuration from TOML file."""
        if not self.config_path.exists():
            # Use default values
            self.config = {
                "claude": {
                    "model": "claude-3-5-haiku-latest",
                    "max_tokens": 4000,
                    "temperature": 0
                },
                "files": {
                    "project_doc": "project.docx",
                    "paper_list": "paper_list.txt",
                    "summaries_dir": "summaries",
                    "papers_dir": "papers"
                }
            }
        else:
            with open(self.config_path, "rb") as f:
                self.config = tomli.load(f)
                
    @property
    def claude_model(self) -> str:
        """Get the Claude model name."""
        return self.config["claude"]["model"]
    
    @property
    def claude_max_tokens(self) -> int:
        """Get the max tokens for Claude API."""
        return self.config["claude"]["max_tokens"]
    
    @property
    def claude_temperature(self) -> float:
        """Get the temperature for Claude API."""
        return self.config["claude"]["temperature"]
    
    @property
    def project_doc(self) -> str:
        """Get the project document path."""
        return self.config["files"]["project_doc"]
    
    @property
    def paper_list(self) -> str:
        """Get the paper list path."""
        return self.config["files"]["paper_list"]
    
    @property
    def summaries_dir(self) -> str:
        """Get the summaries directory path."""
        return self.config["files"]["summaries_dir"]
    
    @property
    def papers_dir(self) -> str:
        """Get the papers directory path."""
        return self.config["files"]["papers_dir"] 