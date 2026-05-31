install: install-prod

install-dev:
	uv sync --all-extras

install-prod:
	uv sync --all-extras --no-dev

dev:
	uv run launcher.py

prod:
	uv run hypercorn --bind 0.0.0.0:13132 --certfile cert.pem --keyfile key.pem launcher:app

lint:
	uv run ruff check --select I --fix .
	uv run ruff format .

clean:
	rm -f logs/*.log

.PHONY: install install-dev install-prod dev prod lint clean
.DEFAULT_GOAL := dev
