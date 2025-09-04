# AI Video Translator (with Summarizing AI Tool)

This Streamlit-based app lets users upload videos, extract and transcribe audio, translate the result into a chosen language, and generate a summary — all using powerful AI tools.

## 🔧 Features

- 🎧 Extract audio using ffmpeg
- 🗣 Transcribe speech to text via Google Cloud Speech-to-Text
- 🌍 Translate using Google Translate (via `googletrans`)
- 🧠 Summarize content using Hugging Face Transformers (BART model)
- 🖥 Intuitive web interface built with Streamlit

## 📁 Folder Structure

```
video_translator/
├── app.py                  # (Optional) Script-style processor
├── helpers.py              # Core logic: audio, transcription, translation, summarization
├── streamlit_app.py        # 🔵 Main Streamlit app UI
├── requirements.txt        # Python dependencies
├── packages.txt            # System packages (e.g. ffmpeg)
├── styles.css              # Custom UI styling
├── service_account_key.json (or use Streamlit secrets) 
```

## 📦 Installation & Running Locally

1. Install Python 3.9+ and [ffmpeg](https://ffmpeg.org/).
2. Clone the repo and install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run video_translator/streamlit_app.py
```

## 🚀 Deployment

For **Streamlit Cloud**, make sure you:
- Upload `service_account_key.json` contents into **Secrets > [gcp]** (formatted correctly)
- Include `ffmpeg` in `packages.txt`

---

## 👨‍🎓 Dissertation Use

This project demonstrates real-time multimedia AI integration:
- Speech-to-text processing
- Neural machine translation (NMT)
- Text summarization
- Web-based user experience
