PYTHON?=python3
PIP?=pip3

help:
	@echo Usage:
	@echo - make dev
	@echo - make build
	@echo - make test
	@echo - make mypy
	@echo - make lint
	@echo - make all

env:
	${PIP} install -r requirements.txt

build: env
	${PYTHON} setup.py sdist bdist_wheel
	${PIP} install -e .

sphinx:
	cd docs && ${MAKE} html

test:
	pytest

mypy:
	mypy disruptive/
	mypy examples/

lint:
	flake8

tests: test mypy lint

all: build tests
