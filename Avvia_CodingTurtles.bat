@echo off
title Avvio progetto Django - CodingTurtles
echo =========================================
echo   AVVIO PROGETTO DJANGO - CodingTurtles
echo =========================================
echo.

REM --- Vai nella cartella del BAT (dove c'è manage.py) ---
cd /d %~dp0

REM ==============================
REM 1. Controllo presenza Python
REM ==============================
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [!] Python non e' installato o non e' nel PATH.
    start https://www.python.org/downloads/windows/
    pause
    exit /b
)
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo Python versione rilevata: %PYTHON_VER%
echo.

REM ==============================
REM 2. Crea/Attiva venv
REM ==============================
IF NOT EXIST venv (
    echo Creo ambiente virtuale...
    python -m venv venv
)
if not exist venv\Scripts\activate.bat (
    echo [!] Errore: manca activate.bat in venv\Scripts
    pause
    exit /b
)
call venv\Scripts\activate.bat
echo Ambiente virtuale attivato.
echo.

REM ==============================
REM 3. Aggiorna pip e installa requirements
REM ==============================
python -m pip install --upgrade pip
IF EXIST requirements.txt (
    echo Installazione dipendenze dal requirements.txt...
    python -m pip install -r requirements.txt
)

REM ==============================
REM 4. Controllo Django
REM ==============================
python -m django --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [!] Django non trovato nel venv. Installazione...
    python -m pip install "Django>=5.0,<6.0"
) ELSE (
    for /f "tokens=*" %%i in ('python -m django --version') do set DJANGO_VER=%%i
    echo Django versione rilevata nel venv: %DJANGO_VER%
)
echo.

REM ==============================
REM 5. Trova porta libera
REM ==============================
set PORT=8000
:check_port
netstat -ano | findstr ":%PORT%" >nul
IF %ERRORLEVEL%==0 (
    set /a PORT+=1
    goto check_port
)
echo Porta libera: %PORT%
echo.

REM ==============================
REM 6. Avvia server Django
REM ==============================
echo Avvio del server...
start "" python manage.py runserver %PORT%
start http://localhost:%PORT%
pause
