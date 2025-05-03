import streamlit as st
import helpers  # Your helper functions from helpers.py
import os
import tempfile
import torch
import ffmpeg

# ✅ Set Google Cloud credentials (for local dev only)
# Comment this out if you're using Streamlit secrets instead
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account_key.json"

# ✅ Load your custom CSS
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    # Initialize session state
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

                # Step 1: Extract Audio
                st.write("🎧 Extracting audio...")
                audio_file = helpers.extract_audio(temp_video_file.name)
                if not audio_file:
                    st.error("❌ Failed to extract audio.")
                    return
                st.success("✅ Audio extracted!")

                # Step 2: Transcribe
                st.write("🔊 Transcribing audio...")
                transcript = helpers.transcribe_audio(audio_file)
                if not transcript:
                    st.error("❌ Failed to transcribe audio.")
                    return
                st.success("✅ Transcript created!")
                st.write(f"📝 Transcript Preview:\n{transcript[:300]}...")

                # Step 3: Translate
                st.write("🌍 Translating transcript...")
                translated_text = helpers.translate_text(transcript, st.session_state.target_lang)
                st.success("✅ Translation complete!")
                st.write(f"🈂️ Translation Preview:\n{translated_text[:300]}...")

                # Step 4: Summarize
                st.write("🧠 Generating summary...")
                summary = helpers.summarize_text(translated_text)
                st.success("✅ Summary generated!")
                st.write(f"📋 Summary Preview:\n{summary}")

            except Exception as e:
                st.error(f"🚨 An error occurred: {e}")
                st.warning("Please ensure the video file is supported and all services are correctly configured.")
        else:
            st.info("📁 Please upload a video file.")

if __name__ == "__main__":
    main()
