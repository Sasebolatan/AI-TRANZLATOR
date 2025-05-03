import streamlit as st
import helpers  # Your helper functions from helpers.py
import os
import tempfile
import torch
import ffmpeg

# ✅ Set Google Cloud credentials environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account_key.json"

# Load the custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Initialize session state if not already set
    if 'target_lang' not in st.session_state:
        st.session_state.target_lang = "English"

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Welcome", "Language Selection", "Upload Video"])

    if page == "Welcome":
        st.title("AI Video Translator with Summarization")
        st.write("Welcome to the AI Video Translator. This app allows you to upload a video, transcribe it to text, translate it to another language, and generate a summary.")
        
        language = st.selectbox("Select your language", ["English", "Spanish", "French", "German", "Italian", "Japanese", "Korean"])
        st.session_state.language = language

    elif page == "Language Selection":
        st.title("Select Target Language")
        target_lang = st.selectbox("Select target language for translation", ["English", "Spanish", "French", "German", "Italian", "Japanese", "Korean"])
        st.session_state.target_lang = target_lang

    elif page == "Upload Video":
        st.title("Upload Video")
        video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

        if video_file:
            try:
                with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
                    temp_video_file.write(video_file.read())
                    temp_video_file.close()

                st.video(temp_video_file.name)
                st.write("Processing video...")
