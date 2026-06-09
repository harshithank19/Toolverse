from flask import Flask, render_template, request, jsonify, send_from_directory, make_response
import fitz
from gtts import gTTS
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

# =====================
# HOME PAGE
# =====================
@app.route("/")
def home():
    response = make_response(render_template("index.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# =====================
# PDF TO AUDIOBOOK
# =====================
@app.route("/audiobook")
def audiobook():
    response = make_response(render_template("audiobook.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/convert", methods=["POST"])
def convert():
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["pdf"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pdf_path)
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    if not text.strip():
        return jsonify({"error": "No readable text found in PDF"}), 400
    tts = gTTS(text=text, lang="en")
    audio_filename = str(uuid.uuid4()) + ".mp3"
    audio_path = os.path.join(OUTPUT_FOLDER, audio_filename)
    tts.save(audio_path)
    return jsonify({"audio_file": audio_filename, "transcript": text})

@app.route("/output/<filename>")
def get_audio(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

# =====================
# VIDEO TO TRANSCRIPT
# =====================
@app.route("/video")
def video():
    response = make_response(render_template("video.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/video/convert", methods=["POST"])
def video_convert():
    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400
    file = request.files["video"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    video_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    video_path = os.path.join(UPLOAD_FOLDER, video_filename)
    file.save(video_path)

    try:
        from moviepy import VideoFileClip
        import speech_recognition as sr

        audio_path = os.path.join(UPLOAD_FOLDER, str(uuid.uuid4()) + ".wav")
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(
            audio_path,
            fps=16000,
            nbytes=2,
            codec='pcm_s16le',
            logger=None
        )
        clip.close()

        recognizer = sr.Recognizer()
        transcript = ""

        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                transcript = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                transcript = "Could not understand audio clearly."
            except sr.RequestError as e:
                return jsonify({"error": "Speech recognition failed: " + str(e)}), 500

        os.remove(audio_path)
        os.remove(video_path)

        return jsonify({"transcript": transcript})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================
# PDF SUMMARIZER
# =====================
@app.route("/summarizer")
def summarizer():
    response = make_response(render_template("summarizer.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/summarizer/convert", methods=["POST"])
def summarizer_convert():
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["pdf"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pdf_path)
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    if not text.strip():
        return jsonify({"error": "No readable text found in PDF"}), 400

    try:
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lsa import LsaSummarizer

        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary_sentences = summarizer(parser.document, 10)
        summary = " ".join(str(sentence) for sentence in summary_sentences)

        if not summary.strip():
            return jsonify({"error": "Could not generate summary from this PDF"}), 400

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================
# TEXT TO SPEECH
# =====================
@app.route("/tts")
def tts():
    response = make_response(render_template("tts.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/tts/convert", methods=["POST"])
def tts_convert():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400
    if len(text) > 5000:
        return jsonify({"error": "Text too long! Max 5000 characters"}), 400
    tts = gTTS(text=text, lang="en")
    audio_filename = str(uuid.uuid4()) + ".mp3"
    audio_path = os.path.join(OUTPUT_FOLDER, audio_filename)
    tts.save(audio_path)
    return jsonify({"audio_file": audio_filename})

# =====================
# IMAGE TO TEXT
# =====================
@app.route("/imagetext")
def imagetext():
    response = make_response(render_template("imagetext.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/imagetext/convert", methods=["POST"])
def imagetext_convert():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        import pytesseract
        from PIL import Image

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

        img_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        img_path = os.path.join(UPLOAD_FOLDER, img_filename)
        file.save(img_path)

        img = Image.open(img_path)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        width, height = img.size
        if width < 1000:
            scale = 1000 / width
            img = img.resize((int(width * scale), int(height * scale)), Image.LANCZOS)

        img = img.convert('L')

        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(img, config=custom_config)

        os.remove(img_path)

        if not text.strip():
            return jsonify({"error": "No text found in this image"}), 400

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =====================
# AI CHATBOT
# =====================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        from groq import Groq
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful AI assistant for ToolVerse — a free AI-powered media tools platform.
                    ToolVerse has these tools:
                    1. PDF to Audiobook — converts PDFs to MP3 audio with live transcript highlighting
                    2. Video to Transcript — extracts text transcript from video files
                    3. PDF Summarizer — generates AI-powered summaries of PDFs
                    4. Text to Speech — converts typed text to natural sounding audio
                    5. Image to Text — extracts text from images using OCR technology

                    You can answer questions about how to use these tools AND general questions.
                    Keep responses concise, friendly and helpful.
                    If asked about ToolVerse features, be specific and accurate.
                    Format responses clearly — use bullet points when listing multiple items."""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=512,
            temperature=0.7
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)