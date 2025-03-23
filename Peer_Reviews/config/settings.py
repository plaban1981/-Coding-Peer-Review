from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class ReviewConfig:
    MIN_CONFIDENCE_SCORE: float = 0.8
    MAX_REVIEW_TIME: int = 300  # seconds
    
    # Use field with default_factory for mutable defaults
    SEVERITY_LEVELS: Dict[str, int] = field(default_factory=lambda: {
        "CRITICAL": 1,
        "HIGH": 2,
        "MEDIUM": 3,
        "LOW": 4
    })
    
    # Review categories
    REVIEW_CATEGORIES: List[str] = field(default_factory=lambda: [
        "code_quality",
        "security",
        "performance",
        "maintainability",
        "testing"
    ])
    
    # LLM configuration
    LLM_CONFIG: Dict[str, any] = field(default_factory=lambda: {
        "temperature": 0.3,
        "max_tokens": 2000,
        "model": "mixtral-8x7b-32768"
    }) 