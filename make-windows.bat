@echo off
setlocal EnableDelayedExpansion

REM ===============================
REM Clean build files if requested
REM ===============================
if /I "%1"=="clean" (
    echo Cleaning...
    rmdir /s /q venv build dist __pycache__ 2>nul
    del /q libcalc.dll libcalc.a Calculator.spec 2>nul
    echo Clean complete.
    goto :EOF
)

REM ===============================
REM Check prerequisites
REM ===============================
echo Checking prerequisites...
where python >nul 2>&1 || (echo Error: Python not found. && exit /b 1)
where gcc >nul 2>&1 || (echo Error: GCC not found. && exit /b 1)

REM ===============================
REM Setup virtual environment and dependencies
REM ===============================
echo Setting up environment...
if not exist "venv" python -m venv venv || (echo Error: Venv creation failed. && exit /b 1)
call venv\Scripts\activate.bat || (echo Error: Venv activation failed. && exit /b 1)

REM Use 'python -m pip' to ensure pip within the venv is targeted
python -m pip install --upgrade pip >nul || (echo Error: Pip upgrade failed. && exit /b 1)
if exist "requirements.txt" (
    python -m pip install -r requirements.txt >nul || (echo Error: Dependency install failed. && exit /b 1)
) else (
    echo Warning: requirements.txt not found.
)

REM ===============================
REM Build DLL
REM ===============================
echo Compiling DLL...
if not exist "calc.c" (echo Error: calc.c not found. && deactivate >nul 2>&1 && exit /b 1)
gcc -shared -o libcalc.dll -Wl,--out-implib,libcalc.a -Wl,--dll calc.c || (echo Error: DLL compile failed. && deactivate >nul 2>&1 && exit /b 1)

REM ===============================
REM Build executable with PyInstaller
REM ===============================
echo Building executable...
if not exist "calculator.py" (echo Error: calculator.py not found. && deactivate >nul 2>&1 && exit /b 1)

set "PYINSTALLER_CMD=pyinstaller --onefile --windowed --add-binary "libcalc.dll;." --name Calculator calculator.py"
if exist "icon.ico" (
    set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --icon=icon.ico"
) else (
    echo Warning: icon.ico not found. Building without icon.
)

%PYINSTALLER_CMD% || (echo Error: PyInstaller build failed. && deactivate >nul 2>&1 && exit /b 1)

REM ===============================
REM Finish
REM ===============================
echo Build complete.
deactivate >nul 2>&1
echo Executable in 'dist' folder.
pause
endlocal
