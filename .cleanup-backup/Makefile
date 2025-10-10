.PHONY: setup lint format type test precommit build

ifeq ($(OS),Windows_NT)
PY        = py -3.11
VENV_BIN  = .venv/Scripts
PIP       = $(VENV_BIN)/pip.exe
PYTHON    = $(VENV_BIN)/python.exe
PRECOMMIT = $(VENV_BIN)/pre-commit.exe
RUFF      = $(VENV_BIN)/ruff.exe
MYPY      = $(VENV_BIN)/mypy.exe
PYTEST    = $(VENV_BIN)/pytest.exe
else
PY        = python3.11
VENV_BIN  = .venv/bin
PIP       = $(VENV_BIN)/pip
PYTHON    = $(VENV_BIN)/python
PRECOMMIT = $(VENV_BIN)/pre-commit
RUFF      = $(VENV_BIN)/ruff
MYPY      = $(VENV_BIN)/mypy
PYTEST    = $(VENV_BIN)/pytest
endif

setup:
	$(PY) -m venv .venv
	$(PIP) install -U pip
	$(PIP) install -e .[dev]
	$(PRECOMMIT) install

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

type:
	$(MYPY) src

test:
	$(PYTEST)

precommit:
	$(PRECOMMIT) run --all-files

build:
	$(PYTHON) -m build
