# Makefile for building Calculator app on Linux

# Source and target names
C_SRC       = calc.c
SO_FILE     = libcalc.so
PY_SRC      = calculator.py
ICON        = icon.ico
PY_REQ      = requirements.txt
VENV        = venv
EXE_NAME    = Calculator
PYINSTALLER = $(VENV)/bin/pyinstaller
CC          = gcc

.PHONY: all clean

# Main target: builds everything
all: $(VENV)/bin/activate $(SO_FILE) build_exe

# Set up virtual environment and install Python requirements
$(VENV)/bin/activate:
	@echo "Creating virtual environment (if not exists)..."
	@test -d $(VENV) || python3 -m venv $(VENV)
	@echo "Installing Python dependencies..."
	@$(VENV)/bin/pip install --upgrade pip
	@$(VENV)/bin/pip install -r $(PY_REQ)

# Compile the C code into a shared object for ctypes
$(SO_FILE): $(C_SRC)
	@echo "Compiling C shared library..."
	$(CC) -fPIC -shared -o $(SO_FILE) $(C_SRC)

# Build the final standalone binary using PyInstaller
build_exe:
	@echo "Building standalone executable with PyInstaller..."
	@$(PYINSTALLER) --onefile --windowed \
		--icon=$(ICON) \
		--add-binary "$(SO_FILE):." \
		--name=$(EXE_NAME) \
		$(PY_SRC)

# Clean all generated files
clean:
	@echo "Cleaning build files..."
	@rm -f $(SO_FILE)
	@rm -rf __pycache__ build dist *.spec $(VENV)
