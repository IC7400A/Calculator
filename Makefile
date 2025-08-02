# Makefile for building Calculator app on Linux/macOS

# --- Variables ---
VENV        = venv
PYTHON      = $(VENV)/bin/python3
PIP         = $(VENV)/bin/pip
PYINSTALLER = $(VENV)/bin/pyinstaller
CC          = gcc

# --- Source and Target Names ---
C_SRC       = core/calc_functions.c
LIB_NAME    = libcalc_functions.so
PY_ENTRY    = main.py
EXE_NAME    = Calculator

.PHONY: all clean run build_exe

# --- Main Targets ---
all: build

build: $(VENV)/bin/activate $(LIB_NAME) build_exe

run: $(VENV)/bin/activate
	@echo ">>> Running the application..."
	@$(PYTHON) $(PY_ENTRY)

# --- Build Steps ---
$(VENV)/bin/activate: requirements.txt
	@echo ">>> Setting up virtual environment..."
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip > /dev/null
	@$(PIP) install -r requirements.txt > /dev/null

$(LIB_NAME): $(C_SRC)
	@echo ">>> Compiling C shared library..."
	$(CC) -fPIC -shared -o $(LIB_NAME) $(C_SRC)

build_exe:
	@echo ">>> Building standalone executable with PyInstaller..."
	@$(PYINSTALLER) --onefile --windowed \
		--name=$(EXE_NAME) \
		--add-binary "$(LIB_NAME):core" \
		$(PY_ENTRY)

# --- Housekeeping ---
clean:
	@echo ">>> Cleaning build files..."
	@rm -f $(LIB_NAME)
	@rm -rf __pycache__ build dist *.spec $(VENV) core/__pycache__ ui/__pycache__