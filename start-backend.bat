@echo off
echo Starting Backend...
cd backend
if not exist "venv\Scripts\activate" (
    echo Virtual environment not found in backend/venv.
    pause
    exit /b 1
)
call venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
