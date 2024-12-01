.PHONY: dev lint test

dev:
	uv venv
	uv sync
	uv run pre-commit install

lint:
	uv run pre-commit run --all-files

test:
	pytest --cov plox --cov-report term-missing -vv tests
