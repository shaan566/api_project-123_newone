<<<<<<< HEAD

@echo off
echo Starting SEO Research Pro...
echo.

echo Installing dependencies...
call npm install
cd backend
call pip install -r requirements.txt
cd ..

echo.
echo Creating environment file...
echo NEXT_PUBLIC_FASTAPI_URL=http://localhost:5000 > .env.local

echo.
echo Starting application...
echo Backend will run on: http://localhost:5000
echo Frontend will run on: http://localhost:3000
echo.

call npm run dev:full

pause
=======
@echo off
title SEO Research Pro
echo ============================================
echo        Starting SEO Research Pro...
echo ============================================
echo.

REM --------------------------------------------
REM Install Python dependencies
REM --------------------------------------------
echo.
echo 📦 Installing Python dependencies...
cd backend
pip install -r requirements.txt

cd ..

REM --------------------------------------------
REM Install Node.js dependencies
REM --------------------------------------------
echo.
echo 📦 Installing Node.js dependencies...
npm install


REM --------------------------------------------
REM Launch Servers
REM --------------------------------------------
echo.
echo ✅ Dependencies installed successfully!
echo 🚀 Starting servers...
echo --------------------------------------------
echo 🔄 Backend running at:  http://localhost:5000
echo 🌐 Frontend running at: http://localhost:3000
echo 📘 API Docs:           http://localhost:5000/docs
echo --------------------------------------------
echo.

REM Start backend server in new terminal
start "SEO Research Pro Backend" cmd /k "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend server in new terminal
start "SEO Research Pro Frontend" cmd /k "npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo API Documentation: http://localhost:5000/docs
echo.
echo Press any key to exit this window...
pause >nul
>>>>>>> 59c45857b34d2eb3ee7d5ebefcd93fa3cac60ba4
