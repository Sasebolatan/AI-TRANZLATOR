# app.py - Legacy or alternative script (depending on your architecture)
# NOTE: This file appears to be a secondary entry point, possibly used before streamlit_app.py.
# It demonstrates direct use of the audio processing and summarization tools without UI.

import os
import tempfile
from helpers import extract_audio, transcribe_audio, translate_text, summarize_text

# ✅ This is a simple CLI-style flow, likely for testing or development.

def main(video_path, target_lang="es"):
    print("Processing video...")

    # Step 1: Extract audio from the video
    audio_path = extract_audio(video_path)
    if not audio_path:
        print("❌ Audio extraction failed")
        return

    print("✅ Audio extracted. Transcribing...")
    # Step 2: Transcribe audio to text
    transcript = transcribe_audio(audio_path)
    print("✅ Transcript:
", transcript[:200])

    # Step 3: Translate transcript
    translated = translate_text(transcript, target_lang)
    print("✅ Translated:
", translated[:200])

    # Step 4: Summarize translated text
    summary = summarize_text(translated)
    print("✅ Summary:
", summary)

if __name__ == "__main__":
    # Example test call (for development)
    test_video_path = "sample_video.mp4"  # Replace with your test file path
    if os.path.exists(test_video_path):
        main(test_video_path)
    else:
        print("⚠️ Please update 'test_video_path' to a real file to run this test.")
