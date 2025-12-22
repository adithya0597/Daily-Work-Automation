# Example: Run quality gate
skillpack quality-gate

# Example: Check only (CI mode)
skillpack quality-gate --check

# This runs:
# 1. ruff format (or --check)
# 2. ruff check (with --fix unless --check)
# 3. mypy skillpack/
# 4. pytest tests/
