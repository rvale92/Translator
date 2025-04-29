"""Text-to-Speech module using Google Text-to-Speech (gTTS)."""

import os
from pathlib import Path
from typing import Optional
from gtts import gTTS
from pydub import AudioSegment
from .config import OUTPUT_DIR, SUPPORTED_LANGUAGES
from .utils import generate_filename

class TextToSpeech:
    """Text-to-Speech processor using Google TTS."""
    
    def __init__(self):
        """Initialize the TTS processor."""
        # Ensure output directory exists
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    def synthesize_speech(
        self,
        text: str,
        lang_code: str,
        output_path: Optional[str] = None,
        slow: bool = False,
        output_format: str = "mp3"
    ) -> str:
        """
        Convert text to speech using Google TTS.
        
        Args:
            text: Text to convert to speech
            lang_code: Language code (e.g., "en", "es")
            output_path: Optional path for output audio file
            slow: Whether to speak slowly
            output_format: Output audio format ("mp3" or "wav")
            
        Returns:
            str: Path to the generated audio file
        """
        # Validate language code
        if lang_code not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language code: {lang_code}")
            
        # Generate output path if not provided
        if output_path is None:
            output_path = OUTPUT_DIR / generate_filename(
                prefix=f"tts_{lang_code}",
                extension=f".{output_format}"
            )
        else:
            output_path = Path(output_path)
            
        # Create gTTS object and generate speech
        tts = gTTS(text=text, lang=lang_code, slow=slow)
        
        # Save as MP3 first (gTTS only supports MP3)
        temp_mp3 = output_path.with_suffix('.mp3')
        tts.save(str(temp_mp3))
        
        # Convert to desired format if not MP3
        if output_format.lower() != "mp3":
            audio = AudioSegment.from_mp3(temp_mp3)
            audio.export(output_path, format=output_format)
            temp_mp3.unlink()  # Remove temporary MP3
            
        return str(output_path)
    
    def create_audio_segments(
        self,
        text: str,
        lang_code: str,
        max_chars: int = 500,
        **kwargs
    ) -> list[str]:
        """
        Split long text into segments and convert each to speech.
        
        Args:
            text: Long text to convert to speech
            lang_code: Language code
            max_chars: Maximum characters per segment
            **kwargs: Additional arguments for synthesize_speech
            
        Returns:
            list[str]: List of paths to audio segment files
        """
        # Split text into segments (try to split at sentence boundaries)
        segments = []
        current_segment = ""
        
        sentences = text.replace("。", ".").replace("！", "!").replace("？", "?").split(".")
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # If adding this sentence would exceed max_chars, save current segment
            if len(current_segment) + len(sentence) > max_chars:
                if current_segment:
                    segments.append(current_segment)
                current_segment = sentence
            else:
                current_segment += " " + sentence if current_segment else sentence
                
        # Add the last segment if it exists
        if current_segment:
            segments.append(current_segment)
            
        # Convert each segment to speech
        audio_paths = []
        for i, segment in enumerate(segments):
            output_path = OUTPUT_DIR / generate_filename(
                prefix=f"tts_{lang_code}_part{i+1}",
                extension=".mp3"
            )
            audio_path = self.synthesize_speech(
                text=segment,
                lang_code=lang_code,
                output_path=output_path,
                **kwargs
            )
            audio_paths.append(audio_path)
            
        return audio_paths
    
    def combine_audio_files(
        self,
        audio_paths: list[str],
        output_path: Optional[str] = None,
        output_format: str = "mp3"
    ) -> str:
        """
        Combine multiple audio files into one.
        
        Args:
            audio_paths: List of paths to audio files
            output_path: Optional path for combined audio file
            output_format: Output audio format
            
        Returns:
            str: Path to the combined audio file
        """
        if not audio_paths:
            raise ValueError("No audio files provided")
            
        # Generate output path if not provided
        if output_path is None:
            output_path = OUTPUT_DIR / generate_filename(
                prefix="tts_combined",
                extension=f".{output_format}"
            )
        else:
            output_path = Path(output_path)
            
        # Combine audio segments
        combined = AudioSegment.empty()
        for path in audio_paths:
            segment = AudioSegment.from_file(path)
            combined += segment
            
        # Export combined audio
        combined.export(output_path, format=output_format)
        
        return str(output_path)

# Create a default instance
default_tts = TextToSpeech() 