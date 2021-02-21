SHELL=/bin/sh

.PHONY: all help build run serve install install-dev dev-install lint test run-dev dev-run

all: help

build:
	docker build -t wyin-be-feed .

run:
	docker run -p 8080:8080 wyin-be-feed:latest

serve:
	docker run -d -p 8080:8080 wyin-be-feed:latest

install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-dev.txt

dev-install: install-dev

lint:
	pre-commit run --all-files

test:
	pytest --cov=app/ tests/

run-dev:
	uvicorn app.main:app --reload

dev-run: run-dev

help:
	@echo "For available targets type: 'make ' and hit TAB"
	@echo
