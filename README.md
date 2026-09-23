# Expert Call AI

AI-powered expert interview analysis application built for the Hasamex AI Engineer technical case study.

The application analyzes three expert-call transcripts from the European robotic surgery market and uses retrieval-augmented generation (RAG) to answer interview-guide questions, provide exact supporting quotes with timestamps, compare expert perspectives, and answer custom questions across all transcripts.

---

## 1. Case Study Requirements

The Hasamex case study asked for an application that can:

- Analyze three sample expert-call transcripts.
- Answer the provided interview-guide questions for each expert/market.
- Extract exact useful quotes from the transcripts.
- Show the source timestamp for supporting evidence.
- Identify common themes and disagreements across the calls.
- Allow users to ask questions across all transcripts.
- Avoid inventing information or unsupported quotes.
- Provide a simple and usable interface.
- Explain the architecture, model choice, grounding/citation approach, hallucination reduction, and how the solution could scale.

This project implements these requirements through a React frontend, FastAPI backend, ChromaDB vector retrieval, and Gemini for embeddings and answer generation.

---

# 2. What I Built

## Main Features

### 2.1 Interview Guide Analysis

The application contains the six interview-guide questions from the case study:

1. How would you describe current adoption of robotic surgery in your market?
2. What are the main barriers to adoption?
3. How important are hospital budgets and ROI in purchasing decisions?
4. How important are surgeon training and clinical outcomes?
5. What adoption trend do you expect over the next 3–5 years?
6. What is the typical hospital decision-making timeline for purchasing a new robotic system?

Users can:

- Select a market:
  - All Markets
  - France
  - Germany
  - United Kingdom
- Select an interview question.
- Generate an AI-supported answer.
- View the transcript evidence used to support the answer.

Each evidence item contains:

- Expert name
- Expert role
- Market
- Timestamp
- Speaker
- Exact transcript quote

---

### 2.2 Exact Quotes and Timestamped Evidence

The system is designed so that quotes are retrieved directly from the source transcripts.

The AI prompt explicitly instructs the model:

- Never invent facts.
- Never invent quotes.
- Never modify quoted text.
- Use only the supplied transcript evidence.
- Include expert, market, and timestamp for supporting evidence.
- State clearly when the evidence is insufficient.

This makes the generated analysis traceable back to the original transcript.

---

### 2.3 Compare Experts

The "Compare Experts" section analyzes all three expert interviews together.

The application identifies:

- Common themes
- Areas of agreement
- Meaningful differences
- Market-specific observations
- Key takeaways

The application does not rank the experts or decide which expert is correct.

The three source interviews are:

| Market | Expert | Role |
|---|---|---|
| France | Dr. Jean Martin | Head of Urology |
| Germany | Anna Keller | Former Hospital Procurement Director |
| United Kingdom | Dr. Emily Carter | Consultant Urologist |

---

### 2.4 Ask AI

The "Ask AI" section allows the user to ask a custom question across all three transcripts.

Example:

> What are the biggest barriers to robotic surgery adoption?

The system:

1. Converts the question into an embedding.
2. Searches the ChromaDB vector store for relevant transcript chunks.
3. Provides the retrieved evidence to Gemini.
4. Generates a grounded response.
5. Displays the supporting transcript evidence.

This allows users to perform cross-transcript research without manually reading all three calls.

---

# 3. Architecture

```text
                         User
                           |
                           v
                  React + TypeScript
                    Vite + Tailwind
                           |
                           | HTTP / JSON
                           v
                    FastAPI Backend
                           |
             +-------------+-------------+
             |                           |
             v                           v
        ChromaDB                     Gemini API
      Vector Retrieval          Embeddings + Generation
             |
             v
       Transcript Evidence
             |
             v
      Grounded AI Response
```

---

# 4. Technology Stack

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS v3
- Lucide React

## Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

## AI / RAG

- Google Gemini API
- Gemini text generation model
- Gemini Embeddings
- ChromaDB
- Retrieval-Augmented Generation (RAG)

## DevOps

- Docker
- Docker Compose
- GitHub
- GitHub Actions

---

# 5. Project Structure

```text
expert_call_ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── analysis.py
│   │   │       ├── chat.py
│   │   │       └── transcripts.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── prompts.py
│   │   │
│   │   ├── data/
│   │   │   ├── transcripts/
│   │   │   │   ├── france.txt
│   │   │   │   ├── germany.txt
│   │   │   │   └── uk.txt
│   │   │   └── interview_guide.json
│   │   │
│   │   ├── models/
│   │   │   ├── schemas.py
│   │   │   └── transcript.py
│   │   │
│   │   ├── services/
│   │   │   ├── analysis_service.py
│   │   │   ├── ingestion_service.py
│   │   │   ├── llm_service.py
│   │   │   └── rag_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── vectorstore/
│   │   └── .gitkeep
│   │
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.example
│   ├── requirements.txt
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AskAI.tsx
│   │   │   ├── Comparison.tsx
│   │   │   ├── EvidenceCard.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── InterviewGuide.tsx
│   │   │   └── Sidebar.tsx
│   │   │
│   │   ├── types/
│   │   │   └── index.ts
│   │   │
│   │   ├── api.ts
│   │   ├── App.tsx
│   │   ├── index.css
│   │   └── main.tsx
│   │
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.example
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.ts
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# 6. Backend API

The backend exposes the following endpoints.

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

## List Transcripts

```http
GET /api/transcripts/
```

Returns the available expert transcripts.

---

## Get Transcript

```http
GET /api/transcripts/{market}
```

Examples:

```text
/api/transcripts/france
/api/transcripts/germany
/api/transcripts/uk
```

---

## Analyze Interview Question

```http
POST /api/analysis/question
```

Example request:

```json
{
  "market": "France",
  "question": "What are the main barriers to adoption?"
}
```

The market can also be omitted/null to search across all markets.

---

## Compare Experts

```http
GET /api/analysis/compare
```

Returns a cross-transcript comparison of the three experts.

---

## Ask AI

```http
POST /api/chat/
```

Example request:

```json
{
  "question": "What are the biggest barriers to robotic surgery adoption?"
}
```

---

# 7. RAG and Grounding Approach

The source transcripts are treated as the ground truth.

The RAG pipeline works as follows:

```text
Transcript Files
      |
      v
Transcript Parser
      |
      v
Timestamped Transcript Chunks
      |
      v
Gemini Embeddings
      |
      v
ChromaDB Vector Store
      |
      v
User Question
      |
      v
Question Embedding
      |
      v
Semantic Retrieval
      |
      v
Relevant Transcript Chunks
      |
      v
Gemini
      |
      v
Grounded Answer + Evidence
```

Each transcript chunk stores metadata such as:

- Expert
- Role
- Market
- Timestamp
- Speaker
- Original transcript text

This metadata is returned with the retrieved evidence so the UI can show the source of each answer.

---

# 8. Hallucination Reduction

Several measures were implemented to reduce hallucination:

### Source-grounded prompting

The system prompt explicitly tells Gemini to use only the supplied transcript evidence.

### Exact quote requirement

The model is instructed not to create or modify quotes.

### Timestamp metadata

Each transcript chunk retains its original timestamp.

### Retrieval before generation

The model receives relevant transcript evidence instead of being asked to answer from general knowledge.

### Insufficient-evidence behavior

The model is instructed to clearly state when the transcripts do not contain enough evidence.

### Separation of experts

Expert, market, role, timestamp, and speaker metadata are retained throughout the retrieval process.

---

# 9. Why ChromaDB?

A vector database is useful because users may ask questions using wording that does not exactly match the transcript.

For example:

```text
User:
What prevents hospitals from adopting robotic surgery?

Transcript:
The biggest issue is getting capital budget approval.
```

Keyword matching may not identify this as strongly as semantic search.

Embeddings allow the system to retrieve semantically related transcript chunks.

ChromaDB was chosen because it is lightweight, easy to run locally, and sufficient for the size of this case study.

---

# 10. Why Gemini?

Gemini is used for two primary tasks:

1. Embedding transcript chunks and questions.
2. Generating grounded answers from retrieved evidence.

The application does not send a question to the model and ask it to answer from general knowledge.

Instead:

```text
Question
   ↓
Retrieve relevant evidence
   ↓
Give evidence + question to Gemini
   ↓
Generate answer
```

This makes the model part of a retrieval-grounded workflow rather than the sole source of information.

---

# 11. Local Setup

## Prerequisites

Install:

- Python 3.12+
- Node.js 20+
- npm
- Docker Desktop (optional if running without Docker)
- Git

A Google Gemini API key is also required.

---

# 12. Run Without Docker

## Step 1 — Clone the repository

```bash
git clone https://github.com/Soumojit-007/expert_call_ai.git
cd expert_call_ai
```

---

## Step 2 — Configure the backend

Go to the backend:

```bash
cd backend
```

Create:

```text
.env
```

Add:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Do not commit this file to GitHub.

The repository contains `.env.example` as a template.

---

## Step 3 — Create Python virtual environment

From the `backend` directory:

### Windows PowerShell

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation is blocked by PowerShell policy, use:

```powershell
.\.venv\Scripts\activate.bat
```

---

## Step 4 — Install backend dependencies

```powershell
pip install -r requirements.txt
```

---

## Step 5 — Start FastAPI

From:

```text
expert_call_ai/backend
```

run:

```powershell
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

# 13. Run the Frontend

Open a second terminal.

Go to the project:

```powershell
cd E:\expert-call-ai\frontend
```

Install dependencies:

```powershell
npm install
```

Create:

```text
frontend/.env
```

Add:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Then start Vite:

```powershell
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 14. Running with Docker Compose

Docker Compose can run the backend and frontend together.

Make sure Docker Desktop is running.

From the project root:

```powershell
cd E:\expert-call-ai
```

If the Compose configuration uses the backend `.env` for the Gemini secret, run:

```powershell
docker compose --env-file backend/.env up --build
```

If the Compose file is already configured with the required environment variable through your shell/environment, this can also be used:

```powershell
docker compose up --build
```

Frontend:

```text
http://localhost:5173
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

To stop the containers:

```powershell
docker compose down
```

To rebuild after code changes:

```powershell
docker compose up --build
```

---

# 15. Environment Variables

## Backend

`backend/.env`

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

## Frontend

`frontend/.env`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

The real `.env` files are intentionally excluded from Git.

Only `.env.example` files should be committed.

---

# 16. Security

API keys are not stored in the React frontend.

The Gemini API key is only used by the FastAPI backend.

The following files should never be committed:

```text
backend/.env
frontend/.env
```

For CI/CD, the Gemini key can be supplied through GitHub Actions Secrets:

```text
GEMINI_API_KEY
```

---

# 17. CI/CD

GitHub Actions is included for basic continuous integration.

The workflow performs checks such as:

- Checkout repository
- Set up Python
- Install backend dependencies
- Verify backend imports
- Build the backend Docker image

The Gemini API key is supplied through GitHub Secrets rather than committed source code.

The workflow can be extended with frontend tests, Docker Compose builds, and deployment stages.

---

# 18. Scaling From 3 to 30+ Transcripts

The current application is intentionally simple for the case study, but the architecture can scale.

For a larger implementation:

### Current

```text
Transcript files
      ↓
ChromaDB
      ↓
Gemini
```

### Larger production architecture

```text
Transcript Storage
       ↓
Document Processing Pipeline
       ↓
Chunking + Metadata Extraction
       ↓
Embedding Service
       ↓
Scalable Vector Database
       ↓
Retrieval / Reranking
       ↓
LLM
       ↓
Grounded Response
```

Possible production improvements include:

- Object storage for transcripts.
- Batch embedding instead of one-at-a-time processing.
- PostgreSQL for application metadata.
- A managed vector database.
- Background ingestion jobs.
- Retrieval filtering by market, expert, date, or project.
- Reranking retrieved chunks.
- Caching frequent questions.
- Evaluation datasets for quote accuracy and retrieval quality.
- Authentication and user/project isolation.
- Observability and structured logging.

The current separation between ingestion, retrieval, LLM generation, API routes, and frontend components makes these upgrades easier to introduce.

---

# 19. Design Decisions

## Why FastAPI?

FastAPI provides:

- Simple Python API development.
- Automatic OpenAPI/Swagger documentation.
- Good integration with Python AI/ML libraries.
- Clear separation between API routes and services.

## Why React + TypeScript?

React provides a simple interactive interface while TypeScript provides type safety for API responses and frontend state.

## Why ChromaDB?

It is lightweight and easy to run locally while providing semantic vector retrieval for this small case study.

## Why separate services?

The project separates:

```text
API routes
Services
Models
Prompts
Configuration
Data
```

This keeps the codebase maintainable and allows individual components to evolve independently.

---

# 20. Key API-to-Frontend Flow

The frontend communicates with FastAPI through `src/api.ts`.

```text
InterviewGuide.tsx
        ↓
analyzeQuestion()
        ↓
src/api.ts
        ↓
POST /api/analysis/question
        ↓
FastAPI
        ↓
RAG retrieval
        ↓
Gemini
        ↓
Answer + evidence
        ↓
React UI
```

The same approach is used for:

```text
Compare Experts
       ↓
GET /api/analysis/compare

Ask AI
       ↓
POST /api/chat/
```

---

# 21. Demo Flow

For the technical demo, the application can be demonstrated in this order:

### 1. Interview Guide

- Select France.
- Select an interview question.
- Run analysis.
- Show the generated answer.
- Show the exact supporting quote.
- Point out the timestamp and expert metadata.

### 2. Compare Experts

- Open Compare Experts.
- Run the comparison.
- Show common themes and meaningful differences across France, Germany, and the UK.

### 3. Ask AI

Ask a cross-transcript question such as:

```text
What are the biggest barriers to robotic surgery adoption across these markets?
```

Show the generated answer and supporting evidence.

### 4. Architecture

Briefly explain:

```text
React
  ↓
FastAPI
  ↓
ChromaDB retrieval
  ↓
Gemini
  ↓
Grounded response
```

### 5. Hallucination Reduction

Explain that the model receives retrieved transcript evidence and is explicitly instructed not to invent or modify quotes.

---

# 22. Limitations

This is a focused technical case-study implementation rather than a production enterprise platform.

Current limitations include:

- The three case-study transcripts are bundled with the application.
- ChromaDB is local.
- Authentication is not implemented.
- There is no persistent user/project management database.
- Large-scale ingestion would require a background processing pipeline.
- Production deployment would require stronger observability, access control, and infrastructure management.

These can be added as the application scales beyond the case-study requirements.

---

# 23. Conclusion

Expert Call AI demonstrates a practical RAG-based approach to expert interview analysis.

The application focuses on the core requirements of the Hasamex case study:

- Interview-guide analysis
- Exact transcript quotes
- Timestamped evidence
- Cross-expert comparison
- Common themes and disagreements
- Natural-language Q&A across transcripts
- Source-grounded generation
- Hallucination reduction
- Clean frontend/backend separation
- Dockerized execution
- CI/CD-ready repository structure

The design intentionally keeps the implementation simple while maintaining a clear path toward scaling the same architecture to a larger expert-research workflow.
