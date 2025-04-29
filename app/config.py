"""Configuration settings and API keys for the Voice Translation App."""

import os
from pathlib import Path
import streamlit as st

# Project paths
BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / "assets" / "input"
OUTPUT_DIR = BASE_DIR / "assets" / "output"

# Create directories if they don't exist
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# API Keys - Try multiple methods to get the key
def get_openai_api_key():
    # Try environment variable first
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key
        
    # Try streamlit secrets
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        if api_key:
            return api_key
    except:
        pass
        
    # If we get here, no key was found
    raise ValueError(
        "OpenAI API key not found. Please set it in Streamlit secrets or as an environment variable."
    )

OPENAI_API_KEY = get_openai_api_key()

# Supported file formats
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".m4a"]

# Supported languages (ISO 639-1 codes)
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "nl": "Dutch",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
} 