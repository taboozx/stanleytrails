@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo Starting server...
python -m uvicorn main:app --reload

pause
