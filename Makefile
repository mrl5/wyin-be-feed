SHELL=/bin/bash

.PHONY: all help install install-dev dev-install lint test run

all: help

install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-dev.txt

dev-install: install-dev

lint:
	pre-commit run --all-files

test:
	pytest --cov=app/ tests/

run:
	uvicorn app.main:app --reload

help:
	@echo "For available targets type: 'make ' and hit TAB"
	@echo
