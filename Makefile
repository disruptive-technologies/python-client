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
	${VENV}/bin/python -m pip install -e .[dev]

build: venv
	${VENV}/bin/python setup.py sdist bdist_wheel

docs: venv
	source ${VENV}/bin/activate && cd docs && ${MAKE} clean html

test: venv
	source ${VENV}/bin/activate && pytest

coverage: venv
	source ${VENV}/bin/activate && pytest --cov=./ --cov-report=xml

lint: venv
	source ${VENV}/bin/activate && mypy disruptive/ && flake8 disruptive/

clean:
	rm -rf build/ dist/ pip-wheel-metadata/ *.egg-info
	find . -name '__pycache__' -exec rm --force --recursive {} +
	rm -rf .pytest_cache/ .mypy_cache/
	rm -rf $(VENV)
	rm -f coverage.xml
