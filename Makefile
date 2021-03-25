PYTHON?=python3
PIP?=pip3
VENV?=venv

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
	source ${VENV}/bin/activate && cd docs && ${MAKE} html

test: venv
	@${VENV}/bin/tox

lint: venv
	@${VENV}/bin/tox -p -e lint

clean-build:
	rm -rf build/ dist/ pip-wheel-metadata/ *.egg-info

clean-py:
	find . -name '__pycache__' -exec rm --force --recursive {} +
	rm -rf .pytest_cache/ .mypy_cache/

clean-test:
	rm -rf .tox/

clean-venv:
	rm -rf $(VENV)

clean: clean-build clean-py clean-test clean-venv
