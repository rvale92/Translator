"""Speech-to-Text module using OpenAI's Whisper model."""

import os
from pathlib import Path
from typing import Optional
import whisper
from .utils import convert_audio_to_wav
from .config import INPUT_DIR

class SpeechToText:
    """Speech-to-Text processor using Whisper."""
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize the STT processor.
        
        Args:
            model_name: Whisper model to use ("tiny", "base", "small", "medium", "large")
        """
        self.model = whisper.load_model(model_name)
    
    def transcribe_audio(
        self,
        audio_path: str,
        language: Optional[str] = None,
        save_transcript: bool = True
    ) -> str:
        """
        Convert spoken audio to text using Whisper.
        
        Args:
            audio_path: Path to the input audio file
            language: Optional ISO language code (e.g., "en", "es")
            save_transcript: Whether to save the transcript to a file
            
        Returns:
            str: Transcribed text
        """
        # Convert audio to WAV format if needed
        wav_path = convert_audio_to_wav(audio_path)
        
        # Transcribe audio
        result = self.model.transcribe(
            wav_path,
            language=language,
            fp16=False  # Use float32 for better compatibility
        )
        
        transcript = result["text"].strip()
        
        # Save transcript if requested
        if save_transcript:
            transcript_path = Path(wav_path).with_suffix(".txt")
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(transcript)
        
        return transcript

# Create a default instance with the base model
default_stt = SpeechToText() 