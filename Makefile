PYTHON?=python3
PIP?=pip3

help:
	@echo Usage:
	@echo - make dev
	@echo - make build
	@echo - make test
	@echo - make lint
	@echo - make all

dev:
	${PIP} install --upgrade pip flake8 pytest pytest-mock setuptools wheel

build: dev
	${PYTHON} setup.py sdist bdist_wheel
	${PIP} install -e .

test:
	pytest

lint:
	flake8

all: build test lint