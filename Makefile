SHELL := /bin/bash

# Compiler
CC = icc

# Interpreters
PYPY = pypy3
PYPY_VENV = $(CURDIR)/venvs/pypy
PYPY_BIN = $(PYPY_VENV)/bin/python
PYPY_PIP = $(PYPY_VENV)/bin/pip
PYPY_REQUIREMENTS = $(CURDIR)/requirements_pypy.txt

PY = python3
PY_VENV = $(CURDIR)/venvs/python
PY_BIN = $(PY_VENV)/bin/python
PY_PIP = $(PY_VENV)/bin/pip
PY_REQUIREMENTS = $(CURDIR)/requirements_python.txt

# Paths
SRC = $(CURDIR)/src
VERSIONS_DIR = $(SRC)/versions/tesina
TESTS_DIR = $(SRC)/tests
CORE_ROOT = $(SRC)


.PHONY: benchmark install test clean

benchmark: install test cache-clean
	$(PY_BIN) -m benchmarker

test: install
	$(PY_BIN) -m unittest discover -v $(TESTS_DIR)

# Installers
install: python-install pypy-install cython-install

python-install: $(PY_VENV)

$(PY_VENV): requirements_python.txt
	virtualenv -p $(PY) $(PY_VENV)
	
	$(PY_PIP) install -r $(PY_REQUIREMENTS)
	$(PY_PIP) install -e $(CORE_ROOT)

pypy-install: $(PYPY_VENV)

$(PYPY_VENV): requirements_pypy.txt
	virtualenv -p $(PYPY) $(PYPY_VENV)

	wget --no-check-certificate -O get-pip.py https://bootstrap.pypa.io/get-pip.py
	$(PYPY_BIN) get-pip.py
	rm get-pip.py

	$(PYPY_PIP) install -r $(PYPY_REQUIREMENTS)
	$(PYPY_PIP) install -e $(CORE_ROOT)

cython-install: $(PY_VENV)
	./install.sh "cython" $(VERSIONS_DIR) $(PY_BIN) $(CC)

# Cleaners
clean: venv-clean cache-clean cython-clean

venv-clean:
	rm -rf $(PY_VENV)
	rm -rf $(PYPY_VENV)

cache-clean:
	find $(SRC) -type f  -regex '.*\.\(pyc\|nbi\|nbc\)' -delete
	find $(SRC) -type d -name "__pycache__" -delete

cython-clean:
	rm $(VERSIONS_DIR)/cython*/*.so
	rm -rf $(VERSIONS_DIR)/cython*/build
