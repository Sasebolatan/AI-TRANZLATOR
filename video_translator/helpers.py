import ffmpeg  # Used for audio extraction from video
from google.cloud import speech  # Google Cloud Speech-to-Text API
from googletrans import Translator  # Google Translate API (unofficial)
from transformers import pipeline  # Hugging Face transformers for summarization
from google.oauth2 import service_account  # For GCP credentials
import tempfile
import time
import streamlit as st
import logging

# Set up logging to debug issues more easily
logging.basicConfig(level=logging.INFO)

#  Load GCP credentials securely from Streamlit secrets
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp"])
client = speech.SpeechClient(credentials=credentials)

#  Initialize translation and summarization models
translator = Translator()
summarizer = pipeline("summarization")

def extract_audio(video_file):
    """Extracts audio from the uploaded video using ffmpeg."""
    try:
        timestamp = int(time.time())
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'_{timestamp}.wav') as audio_file:
            output_audio_path = audio_file.name

        # Run ffmpeg to convert video to mono WAV at 16kHz
        ffmpeg.input(video_file).output(
            output_audio_path, acodec='pcm_s16le', ac=1, ar='16000'
        ).run(overwrite_output=True, capture_stdout=True, capture_stderr=True)

        logging.info(f"Extracted audio file path: {output_audio_path}")
        return output_audio_path
    except Exception as e:
        logging.error(f"Error in extracting audio: {e}")
        return None

def transcribe_audio(audio_file):
    """Transcribes audio using Google Cloud Speech-to-Text API."""
    with open(audio_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    # Combine all transcript segments into one text
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript

def translate_text(text, target_lang="es"):
    """Translates text into the selected language using Google Translate."""
    translated = translator.translate(text, dest=target_lang)
    return translated.text

def summarize_text(text):
    """Summarizes the text using a Hugging Face model (BART by default)."""
    summary = summarizer(text, max_length=200, min_length=50, do_sample=False)
    return summary[0]['summary_text']
