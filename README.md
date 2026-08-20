# PDPA Compliance Checker

An MVP tool that analyzes a company's governance/security documents and assesses compliance against Sri Lanka's Personal Data Protection Act (PDPA). Built for an AI innovation hackathon.

## What it does
- Upload a governance document (PDF or DOCX)
- The system extracts the text and sends it to Google Gemini
- Gemini analyzes the document against PDPA requirements and returns a summary/gap analysis

## Tech stack
- **Backend:** Python (Flask)
- **Frontend:** HTML/JavaScript
- **AI:** Google Gemini API
- **Text extraction:** pypdf (PDF), python-docx (Word)

## Setup

### Prerequisites
- Python 3
- A Gemini API key from [Google AI Studio](https://aistudio.google.com)

### Installation

1. Clone the repo:
   \`\`\`
   git clone https://github.com/randeshd/Project1.git
   cd Project1
   \`\`\`

2. Create and activate a virtual environment:
   \`\`\`
   python3 -m venv venv
   source venv/bin/activate
   \`\`\`

3. Install dependencies:
   \`\`\`
   pip install flask flask-cors pypdf python-docx python-dotenv google-genai
   \`\`\`

4. Set up your API key:
   - Copy \`backend/.env.example\` to \`backend/.env\`
   - Add your actual Gemini API key inside

### Running the app

1. Start the backend:
   \`\`\`
   cd backend
   python3 app.py
   \`\`\`
   Runs on \`http://127.0.0.1:5001\`

2. Open \`frontend/index.html\` (recommended: use VS Code's Live Server extension)

## Status
🚧 Work in progress — MVP for hackathon submission.