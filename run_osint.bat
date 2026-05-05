@echo off
setlocal

rem If a virtual environment exists, activate it.
if exist "%~dp0.venv\Scripts\activate.bat" (
    call "%~dp0.venv\Scripts\activate.bat"
)

rem Run the SafeStack OSINT CLI with forwarded arguments.
python -m cli.ss_osint %*

endlocal
