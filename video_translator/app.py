import streamlit as st
import tempfile  # Import tempfile to avoid the NameError
import helpers  # Import the helper functions
import os

# Add the custom CSS to the app
with open("styles.css") as f:  # Open your CSS file
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Welcome", "Language Selection", "Upload Video"])

    if page == "Welcome":
        st.title("AI TRANZLATOR with video Summarization")
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
            with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:  # Fix the tempfile issue
                temp_video_file.write(video_file.read())
                temp_video_file.close()

            st.video(temp_video_file.name)  # Display video

            st.write("Processing video...")  # You can add your actual video processing functions here

            # Extract audio from the video file
            audio_file = helpers.extract_audio(temp_video_file.name)

            if audio_file:
                # Transcribe audio to text
                transcript = helpers.transcribe_audio(audio_file)

                # Translate the transcript to the target language
                translated_text = helpers.translate_text(transcript, st.session_state.target_lang)

                # Summarize the translated text
                summary = helpers.summarize_text(translated_text)

                # Display the translated subtitles and summary
                st.subheader("Translated Subtitles:")
                st.write(translated_text)

                st.subheader("AI-generated Summary:")
                st.write(summary)

if __name__ == "__main__":
    main()
