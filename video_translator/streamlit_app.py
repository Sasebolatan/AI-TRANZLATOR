import streamlit as st  # Streamlit for building the web interface
import helpers  # Custom helper functions for audio extraction, transcription, translation, and summarization
import os
import tempfile  # For saving uploaded video files temporarily
import torch  # Required for the summarization model
import ffmpeg  # For handling audio extraction from video

#  Load custom CSS to style the Streamlit app
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Initialize session state for language persistence
    if 'target_lang' not in st.session_state:
        st.session_state.target_lang = "English"

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Welcome", "Language Selection", "Upload Video"])

    # Welcome Page
    if page == "Welcome":
        st.title("AI Video Translator with Summarization")
        st.write("This app allows you to upload a video, transcribe its speech to text, translate the text into a different language, and generate a summary.")
        language = st.selectbox("Select your language", ["English", "Spanish", "French", "German", "Italian", "Japanese", "Korean"])
        st.session_state.language = language

    # Language selection page
    elif page == "Language Selection":
        st.title("Select Target Language")
        target_lang = st.selectbox("Select target language for translation", ["English", "Spanish", "French", "German", "Italian", "Japanese", "Korean"])
        st.session_state.target_lang = target_lang

    # Video upload and processing page
    elif page == "Upload Video":
        st.title("Upload Video")
        video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

        if video_file:
            try:
                # Save the uploaded video to a temporary file
                with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
                    temp_video_file.write(video_file.read())
                    temp_video_file.close()

                st.video(temp_video_file.name)  # Display the uploaded video
                st.write("Processing video...")

                # Step 1: Extract audio using ffmpeg
                st.write(" Extracting audio...")
                audio_file = helpers.extract_audio(temp_video_file.name)
                if not audio_file:
                    st.error(" Failed to extract audio.")
                    return
                st.success(" Audio extracted!")

                # Step 2: Transcribe audio to text using Google Speech-to-Text
                st.write(" Transcribing audio...")
                transcript = helpers.transcribe_audio(audio_file)
                if not transcript:
                    st.error(" Failed to transcribe audio.")
                    return
                st.success(" Transcript created!")
                st.write(f" Transcript Preview:\n{transcript[:300]}...")

                # Step 3: Translate text into the selected language
                st.write(" Translating transcript...")
                translated_text = helpers.translate_text(transcript, st.session_state.target_lang)
                st.success(" Translation complete!")
                st.write(f" Translation Preview:\n{translated_text[:300]}...")

                # Step 4: Summarize the translated text
                st.write(" Generating summary...")
                summary = helpers.summarize_text(translated_text)
                st.success(" Summary generated!")
                st.write(f" Summary Preview:\n{summary}")

            except Exception as e:
                # Catch-all for debugging errors
                st.error(f" An error occurred: {e}")
                st.warning("Please ensure the video file is supported and all services are correctly configured.")
        else:
            st.info(" Please upload a video file.")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
