@echo off
echo Starting Restaurant Query Assistant with React Frontend...

echo.
echo [1/3] Starting Database...
cd query_assistant
docker-compose up -d

echo.
echo [2/3] Loading Data...
python load_data.py

echo.
echo [3/3] Installing Frontend Dependencies...
cd ..\frontend
call npm install

echo.
echo Starting Backend Server (FastAPI)...
cd ..\query_assistant
start /B python -m uvicorn backend:app --reload --host 0.0.0.0 --port 8000

echo.
echo Starting Frontend Server (React)...
cd ..\frontend
start /B npm run dev

echo.
echo ================================
echo Restaurant Query Assistant Ready!
echo ================================
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop all services...
pause >nul

echo.
echo Stopping services...
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul
cd query_assistant
docker-compose down
echo Services stopped.
pause