"""Text translation module using deep-translator."""

from typing import Optional
from deep_translator import GoogleTranslator
from .config import SUPPORTED_LANGUAGES

class Translator:
    """Text translator using Google Translate API."""
    
    def __init__(self):
        """Initialize the translator."""
        self.translator = GoogleTranslator()
        
    def translate_text(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        preserve_formatting: bool = True
    ) -> str:
        """
        Translate text from source language to target language.
        
        Args:
            text: Text to translate
            source_lang: Source language code (e.g., "en", "es")
            target_lang: Target language code
            preserve_formatting: Whether to preserve text formatting
            
        Returns:
            str: Translated text
        """
        # Validate language codes
        if source_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported source language: {source_lang}")
        if target_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported target language: {target_lang}")
            
        # Create translator for the specific language pair
        translator = GoogleTranslator(
            source=source_lang,
            target=target_lang
        )
        
        # Translate the text
        translated_text = translator.translate(text)
        
        return translated_text
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of the input text.
        
        Args:
            text: Text to analyze
            
        Returns:
            str: ISO language code or None if detection failed
        """
        try:
            detected = self.translator.detect_language(text)
            if detected in SUPPORTED_LANGUAGES:
                return detected
        except Exception:
            pass
        return None

# Create a default instance
default_translator = Translator() 