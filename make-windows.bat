@echo off
setlocal

REM Check if first argument is clean
if /I "%1"=="clean" (
    echo Cleaning build files...
    rmdir /s /q venv
    del /q libcalc.dll
    rmdir /s /q build dist __pycache__
    del /q Calculator.spec
    goto :EOF
)

REM Check for Python
where python >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python and add it to your system PATH.
    exit /b 1
)

REM Check for gcc (mingw)
where gcc >nul 2>&1
if errorlevel 1 (
    echo GCC (mingw) not found.
    echo Please install mingw and add gcc to your PATH.
    exit /b 1
)

REM Create virtual environment if not exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install requirements
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

REM Build DLL with mingw gcc
echo Compiling DLL...
gcc -shared -o libcalc.dll -Wl,--out-implib,libcalc.a -Wl,--dll calc.c

REM Build executable with PyInstaller including DLL
echo Building executable...
pyinstaller --onefile --windowed --icon=icon.ico --add-binary "libcalc.dll;." --name Calculator calculator.py

echo Build complete.
pause
