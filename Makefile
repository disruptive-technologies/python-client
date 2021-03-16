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

dev:
	${PIP} install --upgrade pip flake8 pytest pytest-mock setuptools wheel mypy

build: dev
	${PYTHON} setup.py sdist bdist_wheel
	${PIP} install -e .

test:
	pytest

mypy:
	mypy disruptive/

lint:
	flake8

tests: test mypy lint

all: build test mypy lint
