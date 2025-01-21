import json
from pathlib import Path
import hashlib
import re

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
        # Clean the content of problematic Unicode characters
        cleaned_content = content.encode('ascii', 'ignore').decode()
        return hashlib.sha256(cleaned_content.encode()).hexdigest()
    
    def _legacy_hash(self, content: str) -> str:
        """Compute hash using the old method for backward compatibility.
        
        Args:
            content: Content to hash
            
        Returns:
            Hash string
        """
        try:
            return hashlib.sha256(content.encode()).hexdigest()
        except UnicodeEncodeError:
            return None
    
    def get(self, paper_id: str, prompt: str) -> dict | None:
        """Get cached analysis result if it exists.
        
        Args:
            paper_id: arXiv paper ID
            prompt: Analysis prompt used
            
        Returns:
            Cached analysis result or None if not found
        """
        # Try new hash first
        prompt_hash = self._compute_hash(prompt)
        cache_file = self.cache_dir / f"{paper_id}_{prompt_hash}.json"
        
        # If not found, try legacy hash
        if not cache_file.exists():
            legacy_hash = self._legacy_hash(prompt)
            if legacy_hash:
                legacy_file = self.cache_dir / f"{paper_id}_{legacy_hash}.json"
                if legacy_file.exists():
                    cache_file = legacy_file
        
        if cache_file.exists():
            try:
                with open(cache_file) as f:
                    return json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError):
                print(f"\nWarning: Corrupted cache file for paper {paper_id}, will reanalyze")
                return None
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
        
        try:
            with open(cache_file, "w", encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"\nWarning: Failed to cache results for paper {paper_id}: {str(e)}") 