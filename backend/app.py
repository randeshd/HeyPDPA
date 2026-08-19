from flask import Flask, request
from flask_cors import CORS
from pypdf import PdfReader
import docx
import os

app = Flask(__name__)
CORS(app)

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
    print(extracted_text[:500])  # print first 500 characters as a preview

    return f"Extracted {len(extracted_text)} characters from '{filename}'. Preview: {extracted_text[:200]}"

if __name__ == "__main__":
    app.run(debug=True, port=5000)