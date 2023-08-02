PYTHON?=python3
PIP?=pip3
VENV?=venv

SHELL := /bin/bash

.PHONY: docs build venv VENV

venv: $(VENV)/bin/activate

$(VENV)/bin/activate: setup.py
	$(PIP) install --upgrade pip virtualenv
	@test -d $(VENV) || $(PYTHON) -m virtualenv --clear $(VENV)
	${VENV}/bin/python -m pip install --upgrade pip
	${VENV}/bin/python -m pip install -e .[dev,extra]

build: venv
	${VENV}/bin/python setup.py sdist bdist_wheel

test: venv
	source ${VENV}/bin/activate && pytest tests/

coverage: venv
	source ${VENV}/bin/activate && pytest --cov=disruptive tests/

lint: venv
	source ${VENV}/bin/activate && mypy --config-file ./mypy.ini disruptive/ && flake8 disruptive/

clean:
	rm -rf build/ dist/ pip-wheel-metadata/ *.egg-info .pytest_cache/ .mypy_cache/ $(VENV) coverage.xml
