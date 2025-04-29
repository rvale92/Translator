"""Main Streamlit application for the Voice Translation App."""

import os
import tempfile
from pathlib import Path
import streamlit as st
from pydub import AudioSegment
import soundfile as sf

from .config import SUPPORTED_LANGUAGES, INPUT_DIR, OUTPUT_DIR
from .stt import default_stt
from .translator import default_translator
from .tts import default_tts
from .utils import cleanup_old_files

# Set page config
st.set_page_config(
    page_title="Voice Translation App",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for better mobile responsiveness
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
    }
    .uploadedFile {
        margin: 1rem 0;
    }
    @media (max-width: 768px) {
        .stApp {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Add GitHub deployment info
st.sidebar.markdown("""
### About
Voice Translation App powered by OpenAI Whisper
* [View Source Code](https://github.com/rvale92/Translator)
* [Report Issues](https://github.com/rvale92/Translator/issues)
""")

def init_session_state():
    """Initialize session state variables."""
    if "audio_path" not in st.session_state:
        st.session_state.audio_path = None
    if "transcript" not in st.session_state:
        st.session_state.transcript = None
    if "translation" not in st.session_state:
        st.session_state.translation = None
    if "output_audio" not in st.session_state:
        st.session_state.output_audio = None

def save_uploaded_file(uploaded_file) -> str:
    """Save uploaded audio file and return its path."""
    # Create a temporary file with the same extension
    suffix = Path(uploaded_file.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name

def main():
    """Main application function."""
    # Initialize session state
    init_session_state()
    
    # Display header
    st.title("🎙️ Voice Translation App")
    st.markdown("""
    Transform voice messages between languages instantly! Upload an audio file 
    or record directly in your browser.
    """)
    
    # Create two columns for source and target languages
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Source Language")
        source_lang = st.selectbox(
            "Select input language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]} ({x})",
            key="source_lang"
        )
        
    with col2:
        st.subheader("Target Language")
        target_lang = st.selectbox(
            "Select output language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]} ({x})",
            key="target_lang"
        )
    
    # Audio input section
    st.subheader("Input Audio")
    input_method = st.radio(
        "Choose input method:",
        options=["Upload Audio", "Record Audio"]
    )
    
    if input_method == "Upload Audio":
        uploaded_file = st.file_uploader(
            "Upload an audio file",
            type=["mp3", "wav", "m4a"],
            help="Supported formats: MP3, WAV, M4A"
        )
        
        if uploaded_file:
            st.audio(uploaded_file, format=f"audio/{uploaded_file.type.split('/')[1]}")
            st.session_state.audio_path = save_uploaded_file(uploaded_file)
            
    else:  # Record Audio
        st.warning("Note: Audio recording requires microphone access")
        audio_bytes = st.audio_recorder(
            text="Click to record",
            recording_color="#e87070"
        )
        
        if audio_bytes:
            # Save recorded audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_bytes)
                st.session_state.audio_path = tmp_file.name
                
            # Display recorded audio
            st.audio(audio_bytes, format="audio/wav")
    
    # Process button
    if st.button("Translate Audio", type="primary", disabled=not st.session_state.audio_path):
        with st.spinner("Processing..."):
            try:
                # Step 1: Speech to Text
                st.session_state.transcript = default_stt.transcribe_audio(
                    st.session_state.audio_path,
                    language=source_lang
                )
                
                # Display transcript
                st.subheader("Transcript")
                st.text_area(
                    "Original Text",
                    value=st.session_state.transcript,
                    height=100,
                    disabled=True
                )
                
                # Step 2: Translation
                st.session_state.translation = default_translator.translate_text(
                    st.session_state.transcript,
                    source_lang=source_lang,
                    target_lang=target_lang
                )
                
                # Display translation
                st.subheader("Translation")
                st.text_area(
                    "Translated Text",
                    value=st.session_state.translation,
                    height=100,
                    disabled=True
                )
                
                # Step 3: Text to Speech
                st.session_state.output_audio = default_tts.synthesize_speech(
                    st.session_state.translation,
                    lang_code=target_lang
                )
                
                # Display output audio
                st.subheader("Output Audio")
                with open(st.session_state.output_audio, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    
                # Add download button
                st.download_button(
                    label="Download Translated Audio",
                    data=audio_bytes,
                    file_name=f"translated_audio_{target_lang}.mp3",
                    mime="audio/mp3"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                
    # Cleanup old files periodically
    cleanup_old_files(INPUT_DIR)
    cleanup_old_files(OUTPUT_DIR)

if __name__ == "__main__":
    main() 