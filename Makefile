.PHONY: req dev lint

req:
	uv pip compile pyproject.toml -o requirements/base.txt > /dev/null
	uv pip compile --extra dev pyproject.toml -o requirements/dev.txt > /dev/null

dev:
	uv pip sync requirements/dev.txt

lint:
	pre-commit run --all-files
