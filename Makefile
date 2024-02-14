VENV_DIR = .venv
VENV_BIN = $(VENV_DIR)/bin
VENV_PYTHON   = $(VENV_BIN)/python
NOSETESTS     = $(VENV_BIN)/nosetests

run:
	source $(VENV_DIR)/bin/activate && $(VENV_PYTHON) -m uvicorn src.asgi:app --port 5000 --reload

test:
	@echo "Running the tests"
	$(NOSETESTS)

.PHONY: run test
