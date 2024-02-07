DIR = $(shell pwd)
VENV_DIR = .venv

run:
	@echo "Running the application"
	@python -m uvicorn src.asgi:app --port 5000 --reload


.PHONY: run
