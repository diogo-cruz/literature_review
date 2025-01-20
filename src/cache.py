import json
from pathlib import Path
import hashlib

class PromptCache:
    def __init__(self, cache_dir: str = ".cache"):
        """Initialize the prompt cache.
        
        Args:
            cache_dir: Directory to store cached results
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def _compute_hash(self, content: str) -> str:
        """Compute a hash of the content for cache key.
        
        Args:
            content: Content to hash
            
        Returns:
            Hash string
        """
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(self, paper_id: str, prompt: str) -> dict | None:
        """Get cached analysis result if it exists.
        
        Args:
            paper_id: arXiv paper ID
            prompt: Analysis prompt used
            
        Returns:
            Cached analysis result or None if not found
        """
        prompt_hash = self._compute_hash(prompt)
        cache_file = self.cache_dir / f"{paper_id}_{prompt_hash}.json"
        
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)
        return None
    
    def save(self, paper_id: str, prompt: str, result: dict) -> None:
        """Save analysis result to cache.
        
        Args:
            paper_id: arXiv paper ID
            prompt: Analysis prompt used
            result: Analysis result to cache
        """
        prompt_hash = self._compute_hash(prompt)
        cache_file = self.cache_dir / f"{paper_id}_{prompt_hash}.json"
        
        with open(cache_file, "w") as f:
            json.dump(result, f, indent=2) 