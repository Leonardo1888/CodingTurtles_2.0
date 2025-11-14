@echo off
title Avvio progetto Django - CodingTurtles
echo =========================================
echo   AVVIO PROGETTO DJANGO - CodingTurtles
echo =========================================
echo.

REM --- Forza esecuzione nella cartella del BAT (dove c'è manage.py) ---
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
REM 2. Controllo pip
REM ==============================
python -m pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [!] pip non trovato. Installazione...
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py --user
    del get-pip.py
)

REM ==============================
REM 3. Controllo Django
REM ==============================
python -m django --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [!] Django non trovato. Installazione...
    python -m pip install "Django>=5.0,<6.0" --user
) ELSE (
    for /f "tokens=*" %%i in ('python -m django --version') do set DJANGO_VER=%%i
    echo Django versione rilevata: %DJANGO_VER%
)

echo.
echo Tutto pronto!
echo.

REM ==============================
REM 4. Trova porta libera
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
REM 5. Avvio server Django
REM ==============================
echo Avvio del server...
start "" python manage.py runserver %PORT%
start http://localhost:%PORT%
