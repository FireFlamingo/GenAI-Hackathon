@echo off
echo 🚀 Starting Parent Portal...

REM Check and setup backend
if not exist "backend\venv" (
    echo 📦 Setting up backend virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
)

REM Check and setup frontend  
if not exist "frontend\frontend-venv" (
    echo 📦 Setting up frontend virtual environment...
    cd frontend
    python -m venv frontend-venv
    call frontend-venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
)

REM Start backend
echo 🖥️ Starting MCP Server...
cd backend
call venv\Scripts\activate
start /B python parent_mcp_server.py
cd ..

REM Wait and start frontend
timeout /t 2 /nobreak > nul
echo 🌐 Starting Web Client...
cd frontend
call frontend-venv\Scripts\activate
python parent_portal_client.py

echo ✅ Parent Portal is running!
echo 📱 Open: http://localhost:8001
pause
