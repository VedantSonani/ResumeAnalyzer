# Project Knowledge: Resume Analyzer

## 1. Project Overview
**Resume Analyzer** is a Python-based backend application designed to automate the extraction of structured data from Resume PDFs and facilitate intelligent interactions using Large Language Models (LLMs). It uses **FastAPI** for the API layer and **Google Gemini** (via LangChain) for AI capabilities.

## 2. Technical Architecture

### Core Technologies
- **Language**: Python 3.12+
- **Framework**: FastAPI (High-performance async web framework)
- **AI/LLM**: Google Gemini (`gemini-3-flash-preview`)
- **Orchestration**: LangChain (Google GenAI integration)
- **PDF Processing**: `pdfplumber` (Text extraction)
- **Validation**: Pydantic (Data modeling)

### Directory Structure
- **`main.py`**: Application entry point, CORS configuration, and router inclusion.
- **`routers/`**: HTTP endpoints grouped by functionality.
    - `documents.py`: Handles file uploads and parsing triggers.
    - `chat.py`: Manages chat interactions with the LLM.
- **`services/`**: Business logic and external integrations.
    - `document_parser.py`: Core logic for reading PDFs and using Gemini to extract structured JSON.
    - `rag_pipeline.py`: Chat interface wrapper (currently direct LLM, planned for RAG).
- **`models/`**: Data definitions.
    - `schemas.py`: Defines the strictly typed `Resume` structure.

## 3. Key Features & Workflows

### A. Resume Parsing (Structured Data Extraction)
**Goal**: Convert a raw PDF resume into a structured JSON object.

**Workflow**:
1. **Upload**: User sends a PDF to `POST /documents/upload`.
2. **Text Extraction**: The `document_parser.py` service uses `pdfplumber` to iterate through pages and extract raw text.
3. **AI Extraction**:
    - The raw text is passed to Google Gemini.
    - Uses Gemini's **Structured Output** (Function Calling) mode.
    - The model maps the text to the `Resume` Pydantic schema.
4. **Result**: Returns a JSON object containing:
    - **Personal Details**: Name, Email, LinkedIn, GitHub.
    - **Education**: List of schools, degrees, grades, years.
    - **Experience**: Companies, roles, years, and responsibility bullet points.
    - **Projects**: Titles, descriptions, tech stacks.
    - **Skills**: List of extracted technical and soft skills.
    - **Summary**: Auto-generated professional summary.

### B. Chat Interface
**Goal**: Allow users to ask questions (currently general LLM chat).

**Workflow**:
1. User sends a message to `POST /chat/`.
2. `rag_pipeline.py` constructs a prompt (currently simple concatenation).
3. Sends request to Gemini (`gemini-3-flash-preview`).
4. Returns the AI's response.
*Note: The "RAG" (Retrieval Augmented Generation) part—searching through uploaded documents—is structured in the code but requires a vector database implementation to be active.*

## 4. detailed Data Models
The project works with a strict schema defined in `models/schemas.py`:

- **Resume**: The root object.
- **School**: `name`, `course`, `cgpa`, `start_year`, `end_year`.
- **Company**: `name`, `designation`, `responsibilities` (list), `years`.
- **Project**: `name`, `description`, `tech_stack` (list).
- **Certification**: `title`, `issuer`, `year`.

## 5. Current Development State
- **Implemented**: Full parsing pipeline, API structure, Data models, Direct Chat.
- **In Progress/Pending**:
    - Vector Database integration (ChromaDB) for storing parsed resumes.
    - Embedding Service implementation.
    - RAG logic to answer questions *specifically* based on the uploaded resumes.
