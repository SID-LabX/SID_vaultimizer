@echo off
cd /d "%~dp0"
title Obsidian Vault Optimizer

echo ===================================================
echo   Starting Obsidian Vault Optimizer...
echo ===================================================

REM 1. Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    pause
    exit /b 1
)

REM 2. Create venv if missing (avoiding parenthesis echo trap)
if not exist ".venv\Scripts\activate.bat" (
    echo [*] Creating virtual environment .venv
    python -m venv .venv
)

REM 3. Activate venv
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo.
    echo [ERROR] Failed to activate .venv environment.
    echo.
    pause
    exit /b 1
)

REM 4. Install dependencies
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo [*] Installing dependencies from requirements.txt...
    pip install -r requirements.txt
)

REM 5. Run the optimizer
echo [*] Launching optimizer.py...
echo.
python optimizer.py

echo.
echo ===================================================
echo Process finished.
pause