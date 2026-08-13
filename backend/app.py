from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file received", 400

    file = request.files["file"]
    print(f"Received file: {file.filename}")

    return f"File '{file.filename}' received successfully!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)