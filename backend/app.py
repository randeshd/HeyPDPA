from flask import Flask, request
from flask_cors import CORS
from pypdf import PdfReader
import docx
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # reads .env and loads GEMINI_API_KEY into the environment

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    document = docx.Document(file)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file received", 400

    file = request.files["file"]
    filename = file.filename
    extension = os.path.splitext(filename)[1].lower()

    if extension == ".pdf":
        extracted_text = extract_text_from_pdf(file)
    elif extension == ".docx":
        extracted_text = extract_text_from_docx(file)
    else:
        return f"Unsupported file type: {extension}", 400

    print(f"Extracted {len(extracted_text)} characters from {filename}")

    # Send the extracted text to Gemini as a basic test
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"Summarize this document in one sentence:\n\n{extracted_text[:3000]}"
    )

    return response.text

if __name__ == "__main__":
    print("About to start Flask server...", flush=True)
    try:
        app.run(debug=True, port=5001)
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
    print("Flask server has stopped.", flush=True)