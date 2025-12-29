@echo off
echo ================================
echo Starting Session-Based RAG App
echo ================================

REM Activate virtual environment
call venv\Scripts\activate

echo Starting Ollama...
start cmd /k "ollama run llama3"
timeout /t 5

echo Starting FastAPI backend...
start cmd /k "call venv\Scripts\activate && uvicorn app.main:app --host 127.0.0.1 --port 8000"
timeout /t 5

echo Starting Streamlit UI...
start cmd /k "call venv\Scripts\activate && streamlit run ui/app.py"

echo ================================
echo App started!
echo Open http://localhost:8501
echo ================================
