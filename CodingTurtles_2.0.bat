@echo off
REM Attiva il virtual environment
call Scripts\activate.bat

REM Avvia il server di sviluppo Django in background
start "" python manage.py runserver

REM Apri il browser all'indirizzo localhost:8000
start http://localhost:8000


