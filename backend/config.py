"""Configuration settings for the research agent"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Model Settings
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
PLANNER_MODEL = os.getenv("PLANNER_MODEL", DEFAULT_MODEL)
RESEARCHER_MODEL = os.getenv("RESEARCHER_MODEL", DEFAULT_MODEL)
ANALYST_MODEL = os.getenv("ANALYST_MODEL", DEFAULT_MODEL)
SYNTHESIZER_MODEL = os.getenv("SYNTHESIZER_MODEL", DEFAULT_MODEL)
CRITIC_MODEL = os.getenv("CRITIC_MODEL", DEFAULT_MODEL)

# Search Settings
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
MAX_ARXIV_RESULTS = int(os.getenv("MAX_ARXIV_RESULTS", "3"))
SEARCH_DEPTH = os.getenv("SEARCH_DEPTH", "advanced")  # "basic" or "advanced"

# Content Settings
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "5000"))
MIN_CREDIBILITY_SCORE = float(os.getenv("MIN_CREDIBILITY_SCORE", "0.3"))

# Research Settings
MIN_SUB_QUESTIONS = int(os.getenv("MIN_SUB_QUESTIONS", "3"))
MAX_SUB_QUESTIONS = int(os.getenv("MAX_SUB_QUESTIONS", "5"))
MIN_SOURCES_PER_QUESTION = int(os.getenv("MIN_SOURCES_PER_QUESTION", "3"))

# Temperature Settings
PLANNER_TEMPERATURE = float(os.getenv("PLANNER_TEMPERATURE", "0.7"))
RESEARCHER_TEMPERATURE = float(os.getenv("RESEARCHER_TEMPERATURE", "0.3"))
ANALYST_TEMPERATURE = float(os.getenv("ANALYST_TEMPERATURE", "0.3"))
SYNTHESIZER_TEMPERATURE = float(os.getenv("SYNTHESIZER_TEMPERATURE", "0.5"))
CRITIC_TEMPERATURE = float(os.getenv("CRITIC_TEMPERATURE", "0.3"))

# Credibility Weights
DOMAIN_AUTHORITY_WEIGHT = float(os.getenv("DOMAIN_AUTHORITY_WEIGHT", "0.3"))
CONTENT_QUALITY_WEIGHT = float(os.getenv("CONTENT_QUALITY_WEIGHT", "0.2"))
ACADEMIC_BONUS = float(os.getenv("ACADEMIC_BONUS", "0.9"))

# Trusted Domains
TRUSTED_DOMAINS = [
    ".edu", ".gov", ".org",
    "arxiv.org", "nature.com", "science.org",
    "ieee.org", "acm.org", "springer.com",
    "sciencedirect.com", "pubmed.gov"
]

# CORS Settings
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

def validate_config():
    """Validate required configuration"""
    errors = []
    
    if not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is required")
    if not TAVILY_API_KEY:
        errors.append("TAVILY_API_KEY is required")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    return True
