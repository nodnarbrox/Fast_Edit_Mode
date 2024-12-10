@echo off
REM Deployment script for Fast Edit Mode Web Interface

REM Create virtual environment
python -m venv .venv

REM Activate virtual environment
call .venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Set environment variables (ensure .env is properly configured)
for /f "tokens=1,2 delims==" %%a in (.env) do set %%a=%%b

REM Start the application
flask run --host=0.0.0.0 --port=5000
