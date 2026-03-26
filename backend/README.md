# ResumeLens - AI Resume Analyzer

ResumeLens is a modern AI-powered tool for analyzing resumes against job descriptions, identifying skills, and providing intelligent feedback.

## Features
- **Resume Parsing**: Extracts structured data (Education, Experience, Skills) from PDFs.
- **AI Analysis**: Uses Google Gemini to score and analyze resumes.
- **Modern UI**: sleek, dark-themed frontend for easy interaction.

## Prerequisites
- Python 3.10+
- Google Gemini API Key

## Setup & Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repo-url>
   cd ResumeAnalyzer
   ```

2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your API key:
   ```bash
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

## Running the Application

Start the backend server:

```bash
uvicorn main:app --reload
```

The application will be available at:
- **Frontend**: [http://localhost:8000](http://localhost:8000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
