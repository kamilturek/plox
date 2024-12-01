.PHONY: dev lint test

dev:
	uv venv
	uv sync --dev
	uv run pre-commit install

lint:
	uv run pre-commit run --all-files

test:
	uv run pytest --cov plox --cov-report term-missing -vv tests
