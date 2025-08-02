@echo off
setlocal EnableDelayedExpansion

REM ===============================
REM Configuration
REM ===============================
set VENV_DIR=venv
set C_SRC=core\calc_functions.c
set DLL_NAME=calc_functions.dll
set PY_ENTRY=main.py
set EXE_NAME=Calculator

REM ===============================
REM Clean Target
REM ===============================
if /I "%1"=="clean" (
    echo >>> Cleaning...
    if exist !VENV_DIR! rmdir /s /q !VENV_DIR!
    if exist build rmdir /s /q build
    if exist dist rmdir /s /q dist
    if exist __pycache__ rmdir /s /q __pycache__
    if exist core\__pycache__ rmdir /s /q core\__pycache__
    if exist ui\__pycache__ rmdir /s /q ui\__pycache__
    del /q !DLL_NAME! *.spec >nul 2>&1
    echo Clean complete.
    goto :EOF
)

REM ===============================
REM Setup Environment
REM ===============================
echo >>> Setting up environment...
if not exist "!VENV_DIR!\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv !VENV_DIR! || (echo [ERROR] Venv creation failed. && exit /b 1)
)
call !VENV_DIR!\Scripts\activate.bat || (echo [ERROR] Venv activation failed. && exit /b 1)
echo Installing dependencies...
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt >nul || (echo [ERROR] Dependency install failed. && exit /b 1)

REM ===============================
REM Build DLL from core directory
REM ===============================
echo >>> Compiling DLL...
if not exist "!C_SRC!" (echo [ERROR] !C_SRC! not found. && exit /b 1)
gcc -shared -o !DLL_NAME! !C_SRC! || (echo [ERROR] DLL compile failed. && exit /b 1)

REM ===============================
REM Build Executable
REM ===============================
echo >>> Building executable...
if not exist "!PY_ENTRY!" (echo [ERROR] !PY_ENTRY! not found. && exit /b 1)
pyinstaller --onefile --windowed --name !EXE_NAME! --add-binary "!DLL_NAME!;core" !PY_ENTRY! || (echo [ERROR] PyInstaller build failed. && exit /b 1)

echo.
echo Build complete. Executable is in the 'dist' folder.
pause
endlocal