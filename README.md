# Wiki Quiz - AI-Powered Wikipedia Quiz Generator

A full-stack application that generates quizzes from Wikipedia articles using AI (LLM). Built with FastAPI, React, and PostgreSQL.

![Wiki Quiz Banner](https://img.shields.io/badge/Wiki_Quiz-AI_Powered-6366f1?style=for-the-badge)

## 🚀 Features

- **Quiz Generation**: Enter any Wikipedia URL and get an AI-generated quiz
- **Smart Extraction**: Automatically extracts title, summary, sections, and key entities
- **Diverse Questions**: 5-10 questions with varying difficulty levels (easy, medium, hard)
- **Take Quiz Mode**: Interactive quiz mode with scoring
- **History**: View and revisit all previously generated quizzes
- **Caching**: Prevents duplicate scraping of the same URL
- **Related Topics**: Suggests related Wikipedia articles for further reading

## 📋 Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI (Python) |
| Frontend | React + Vite |
| Database | PostgreSQL |
| LLM | Groq (LangChain) |
| Scraping | BeautifulSoup4 |

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 13+

### 1. Clone the Repository

```bash
git clone <repository-url>
cd DeepKlarity
```

### 2. Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE wiki_quiz;
```

Or using psql:

```bash
psql -U postgres -c "CREATE DATABASE wiki_quiz;"
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit .env file with your database URL and Groq API key
# The .env file is already configured with the provided Groq API key

# Start the backend server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📡 API Endpoints

### Generate Quiz
```
POST /api/quiz/generate
Content-Type: application/json

{
  "url": "https://en.wikipedia.org/wiki/Alan_Turing"
}
```

### Get Quiz History
```
GET /api/quiz/history?skip=0&limit=50
```

### Get Quiz Details
```
GET /api/quiz/{quiz_id}
```

### Delete Quiz
```
DELETE /api/quiz/{quiz_id}
```

## 📁 Project Structure

```
DeepKlarity/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Configuration settings
│   │   ├── database.py          # PostgreSQL connection
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── routers/
│   │   │   └── quiz.py          # Quiz API endpoints
│   │   └── services/
│   │       ├── scraper.py       # Wikipedia scraping
│   │       └── llm_service.py   # LangChain + Groq
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   ├── api/
│   │   │   └── quizApi.js
│   │   └── components/
│   │       ├── GenerateQuiz.jsx
│   │       ├── QuizDisplay.jsx
│   │       ├── QuizHistory.jsx
│   │       └── QuizModal.jsx
│   ├── package.json
│   └── vite.config.js
├── sample_data/
│   ├── alan_turing_output.json
│   ├── albert_einstein_output.json
│   └── test_urls.md
└── README.md
```

## 🧪 Testing

### Test the Backend API

```bash
# Health check
curl http://localhost:8000/health

# Generate a quiz
curl -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Alan_Turing"}'

# Get quiz history
curl http://localhost:8000/api/quiz/history
```

### Sample URLs for Testing

See `sample_data/test_urls.md` for a curated list of Wikipedia URLs to test with.

## 🤖 LangChain Prompt Templates

The application uses carefully designed prompts to ensure high-quality quiz generation. See `PROMPTS.md` for detailed documentation of the prompt templates.

### Quiz Generation Prompt (Summary)
- Generates 5-10 questions based strictly on article content
- Ensures mix of difficulty levels (easy, medium, hard)
- Includes explanations referencing article sections
- Prevents hallucination by grounding in source text

### Related Topics Prompt (Summary)
- Suggests 5-7 related Wikipedia topics
- Based on article sections and key entities
- Helps users explore related concepts

## 🎮 Using the Application

### Tab 1: Generate Quiz
1. Enter a Wikipedia article URL in the input field
2. Click "Generate Quiz" button
3. Wait for the AI to scrape and generate questions
4. View the quiz with questions, options, and explanations
5. Toggle to "Take Quiz" mode to answer questions and get scored

### Tab 2: Past Quizzes
1. View a table of all previously generated quizzes
2. Click "Details" to open the full quiz in a modal
3. Use "Take Quiz" mode in the modal to retake any quiz

## 🎯 Evaluation Criteria Met

| Criteria | Implementation |
|----------|----------------|
| Prompt Design | Carefully crafted prompts with grounding and anti-hallucination measures |
| Quiz Quality | Diverse questions with proper difficulty distribution |
| Extraction Quality | Clean scraping with BeautifulSoup, entity extraction |
| Functionality | Full end-to-end flow with database persistence |
| Code Quality | Modular structure with services, routers, and components |
| Error Handling | Graceful handling of invalid URLs and network errors |
| UI Design | Modern dark theme with glassmorphism and animations |
| Database Accuracy | PostgreSQL with proper schema and caching |
| Testing Evidence | Sample data folder with example outputs |

## 🌟 Bonus Features Implemented

- ✅ **Take Quiz Mode**: Interactive quiz with user scoring
- ✅ **URL Validation**: Validates Wikipedia URLs before processing
- ✅ **Caching**: Prevents duplicate scraping of same URLs
- ✅ **Raw HTML Storage**: Stores scraped HTML for reference

## 📄 License

MIT License
