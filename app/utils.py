"""Utility functions for the Voice Translation App."""

import os
from pathlib import Path
from typing import Union
import uuid
from pydub import AudioSegment
from .config import SUPPORTED_AUDIO_FORMATS, INPUT_DIR, OUTPUT_DIR

def generate_filename(prefix: str = "", extension: str = ".wav") -> str:
    """Generate a unique filename with the given prefix and extension."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}{extension}"

def convert_audio_to_wav(
    input_path: Union[str, Path], 
    output_path: Union[str, Path, None] = None
) -> str:
    """
    Convert any supported audio format to WAV format.
    
    Args:
        input_path: Path to input audio file
        output_path: Optional path for output WAV file
        
    Returns:
        str: Path to the converted WAV file
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
        
    if input_path.suffix.lower() not in SUPPORTED_AUDIO_FORMATS:
        raise ValueError(f"Unsupported audio format: {input_path.suffix}")
    
    # If no output path specified, create one in the input directory
    if output_path is None:
        output_path = INPUT_DIR / generate_filename(extension=".wav")
    else:
        output_path = Path(output_path)
        
    # Load audio using pydub
    audio = AudioSegment.from_file(input_path)
    
    # Export as WAV
    audio.export(output_path, format="wav")
    
    return str(output_path)

def save_audio_file(
    audio_data: bytes,
    filename: Union[str, None] = None,
    directory: Union[str, Path] = INPUT_DIR
) -> str:
    """
    Save audio data to a file in the specified directory.
    
    Args:
        audio_data: Raw audio data in bytes
        filename: Optional filename (will generate if not provided)
        directory: Directory to save the file in
        
    Returns:
        str: Path to the saved audio file
    """
    if filename is None:
        filename = generate_filename(extension=".wav")
        
    filepath = Path(directory) / filename
    
    with open(filepath, "wb") as f:
        f.write(audio_data)
        
    return str(filepath)

def cleanup_old_files(
    directory: Union[str, Path],
    max_files: int = 100,
    max_age_hours: int = 24
) -> None:
    """
    Remove old files from the specified directory.
    
    Args:
        directory: Directory to clean up
        max_files: Maximum number of files to keep
        max_age_hours: Maximum age of files in hours
    """
    directory = Path(directory)
    if not directory.exists():
        return
        
    # Get list of files sorted by modification time
    files = sorted(
        directory.glob("*"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    
    # Keep only max_files most recent files
    for file in files[max_files:]:
        try:
            file.unlink()
        except OSError:
            pass 