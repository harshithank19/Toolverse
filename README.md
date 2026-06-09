# ⚡ ToolVerse – AI-Powered Multi-Tool Web Platform

A full-stack web platform with 5 AI-powered media tools built with Python and Flask. Convert, transcribe, summarize, and listen — completely free, no sign-up needed.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?style=flat&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 🛠️ Tools

| Tool | Description |
|------|-------------|
| 📄 PDF to Audiobook | Converts PDF files to MP3 audio with live transcript highlighting |
| 🎥 Video to Transcript | Extracts text transcript from uploaded video files |
| 📝 PDF Summarizer | Generates AI-powered summaries of PDF documents |
| 🔊 Text to Speech | Converts typed text to natural-sounding audio |
| 🖼️ Image to Text | Extracts text from images using OCR (Tesseract) |
| 🤖 AI Chatbot | Built-in assistant powered by Groq (LLaMA 3) |

---

## 🚀 Tech Stack

- **Backend:** Python, Flask
- **AI/ML:** Groq API (LLaMA 3), gTTS, SpeechRecognition, Tesseract OCR, Sumy
- **Frontend:** HTML, CSS, JavaScript (dark/light mode)
- **Libraries:** PyMuPDF, MoviePy, Pillow, python-dotenv

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/harshithank19/toolverse.git
cd toolverse
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
```
Open `.env` and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Install Tesseract OCR (for Image to Text)
Download and install from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract)

### 6. Run the app
```bash
py app.py
```
Visit `http://127.0.0.1:5000` in your browser.

---

## 📁 Project Structure

```
toolverse/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore
├── static/
│   ├── style.css
│   ├── navbar.css
│   ├── theme.js
│   ├── loader.js
│   └── chatbot.js
└── templates/
    ├── index.html
    ├── audiobook.html
    ├── video.html
    ├── summarizer.html
    ├── tts.html
    └── imagetext.html
```

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key for the AI chatbot |

---

## 👤 Author

**Harshitha NK**  
[GitHub](https://github.com/harshithank19)
