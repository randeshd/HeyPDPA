from flask import Flask, request
from flask_cors import CORS
from pypdf import PdfReader
import docx
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = [".pdf", ".docx"]

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    document = docx.Document(file)
    text = ""

    # Extract normal paragraphs
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    # Extract tables (previously silently skipped)
    for table in document.tables:
        for row in table.rows:
            row_text = " | ".join(cell.text.strip() for cell in row.cells)
            text += row_text + "\n"

    return text

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/upload", methods=["POST"])
def upload_file():
    # Check file exists in the request
    if "file" not in request.files:
        return "No file received", 400

    file = request.files["file"]

    # Check a file was actually selected
    if file.filename == "":
        return "No file selected", 400

    filename = file.filename
    extension = os.path.splitext(filename)[1].lower()

    # Check file type
    if extension not in ALLOWED_EXTENSIONS:
        return f"Unsupported file type: {extension}. Please upload a PDF or DOCX file.", 400

    # Check file size
    file.seek(0, os.SEEK_END)
    file_size_mb = file.tell() / (1024 * 1024)
    file.seek(0)  # reset pointer back to start after checking size

    if file_size_mb > MAX_FILE_SIZE_MB:
        return f"File too large ({file_size_mb:.1f}MB). Max size is {MAX_FILE_SIZE_MB}MB.", 400

    # Try extraction, catch corrupted/unreadable files
    try:
        if extension == ".pdf":
            extracted_text = extract_text_from_pdf(file)
        elif extension == ".docx":
            extracted_text = extract_text_from_docx(file)
    except Exception as e:
        return f"Could not read this file. It may be corrupted or in an unsupported format. Error: {e}", 400

    # Check something was actually extracted
    if not extracted_text.strip():
        return "No readable text found in this document. It may be a scanned/image-based file, which isn't supported yet.", 400

    print(f"Extracted {len(extracted_text)} characters from {filename}")

    # Try calling Gemini, catch API errors separately
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"Summarize this document in one sentence:\n\n{extracted_text[:3000]}"
        )
    except Exception as e:
        return f"AI analysis failed: {e}", 500

    return response.text

if __name__ == "__main__":
    print("About to start Flask server...", flush=True)
    try:
        app.run(debug=True, port=5001)
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
    print("Flask server has stopped.", flush=True)