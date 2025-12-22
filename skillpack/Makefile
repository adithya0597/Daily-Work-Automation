.PHONY: all install format lint typecheck test quality clean help

PYTHON := python3
PIP := pip

all: quality

## Install the package in development mode
install:
	$(PIP) install -e ".[dev]"

## Format code with ruff
format:
	$(PYTHON) -m ruff format skillpack/ tests/
	$(PYTHON) -m ruff check --fix skillpack/ tests/

## Lint code with ruff
lint:
	$(PYTHON) -m ruff check skillpack/ tests/

## Type check with mypy
typecheck:
	$(PYTHON) -m mypy skillpack/

## Run tests with pytest
test:
	$(PYTHON) -m pytest tests/ -v

## Run full quality gate: format + lint + type-check + tests
quality: format lint typecheck test
	@echo "✅ All quality checks passed!"

## Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

## Show this help
help:
	@echo "Available targets:"
	@grep -E '^## ' Makefile | sed 's/## /  /'
	@echo ""
	@grep -E '^[a-zA-Z_-]+:' Makefile | grep -v '.PHONY' | sed 's/:.*//' | sed 's/^/  make /'
