# streamlit_app.py

import streamlit as st
import helpers  # Import the helper functions you created in helpers.py
import os
import tempfile
import torch
import ffmpeg



with open("video_translator/styles.css") as f:  # Correct path to styles.css
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Initialize session state variables if not already initialized
    if 'target_lang' not in st.session_state:
        st.session_state.target_lang = "English"  # Default language or the language you want to initialize with

    # Sidebar navigation
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
        st.session_state.target_lang = target_lang  # Update session state with the selected target language

    elif page == "Upload Video":
        st.title("Upload Video")
        video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

        if video_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
                temp_video_file.write(video_file.read())
                temp_video_file.close()

            st.video(temp_video_file.name)

            st.write("Processing video...")  # You can add your actual video processing functions here

            # Example: Extract audio, transcribe, translate, and summarize
            audio_file = helpers.extract_audio(temp_video_file.name)
            if audio_file:
                transcript = helpers.transcribe_audio(audio_file)
                translated_text = helpers.translate_text(transcript, st.session_state.target_lang)  # Using session_state for target_lang
                summary = helpers.summarize_text(translated_text)

                st.subheader("Translated Subtitles:")
                st.write(translated_text)

                st.subheader("AI-generated Summary:")
                st.write(summary)

if __name__ == "__main__":
    main()
