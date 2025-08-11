
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
