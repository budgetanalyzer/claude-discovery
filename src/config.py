"""
Configuration management for claude-discovery.

Loads environment variables and provides configuration access.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration for claude-discovery."""
    
    # GitHub API
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    # Rate limiting
    MAX_REQUESTS_PER_HOUR = int(os.getenv('MAX_REQUESTS_PER_HOUR', 5000))
    
    # Result limits
    DEFAULT_MAX_RESULTS = int(os.getenv('DEFAULT_MAX_RESULTS', 100))
    
    # Quality thresholds
    QUALITY_THRESHOLD = int(os.getenv('QUALITY_THRESHOLD', 5))
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    CONFIG_DIR = PROJECT_ROOT / 'config'
    DOCS_DIR = PROJECT_ROOT / 'docs'
    
    # Output files
    DISCOVERIES_JSON = PROJECT_ROOT / 'discoveries.json'
    DISCOVERIES_MD = PROJECT_ROOT / 'DISCOVERIES.md'
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.GITHUB_TOKEN:
            raise ValueError(
                "GITHUB_TOKEN not found in environment. "
                "Copy .env.example to .env and add your GitHub token."
            )
        
        if cls.GITHUB_TOKEN == 'ghp_your_token_here':
            raise ValueError(
                "GITHUB_TOKEN is still set to placeholder value. "
                "Replace with your actual GitHub Personal Access Token."
            )
        
        return True


# Validate configuration on import
if __name__ != '__main__':
    # Skip validation during testing or when running module directly
    try:
        Config.validate()
    except ValueError as e:
        # Print warning but don't crash on import
        print(f"Warning: {e}")
