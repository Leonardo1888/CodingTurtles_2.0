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
    echo Sto aprendo la pagina di download ufficiale di Python...
    start https://www.python.org/downloads/windows/
    echo Dopo l'installazione, seleziona "Add Python to PATH".
    pause
    exit /b
)

REM Mostra versione Python rilevata
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo Python versione rilevata: %PYTHON_VER%
echo.

REM ==============================
REM 2. Controllo pip
REM ==============================
python -m pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [!] pip non trovato. Tentativo di installazione...
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    del get-pip.py
)

REM ==============================
REM 3. Controllo Django
REM ==============================
python -m django --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [!] Django non trovato. Installazione in corso...
    python -m pip install --upgrade pip
    python -m pip install Django==5.2.7
) ELSE (
    for /f "tokens=*" %%i in ('python -m django --version') do set DJANGO_VER=%%i
    echo Django versione rilevata: %DJANGO_VER%
    if not "%DJANGO_VER%"=="5.2.7" (
        echo Aggiornamento Django alla versione 5.2.7...
        python -m pip install Django==5.2.7
    )
)

echo.
echo Tutto pronto!
echo.

REM ==============================
REM 4. Trova porta libera (da 8000 in poi)
REM ==============================
set PORT=8000
:check_port
netstat -ano | findstr ":%PORT%" >nul
IF %ERRORLEVEL%==0 (
    set /a PORT+=1
    goto check_port
)
echo Porta libera trovata: %PORT%
echo.

REM ==============================
REM 5. Avvio server Django
REM ==============================
echo Avvio del server locale nella stessa finestra...
echo -------------------------------------------------
echo Una volta avviato, apri il browser all'indirizzo:
echo http://localhost:%PORT%
echo -------------------------------------------------
echo.

start "" python manage.py runserver %PORT%
start http://localhost:%PORT%


REM ==============================
REM 6. Fine
REM ==============================
echo.
echo Server Django terminato.
pause
