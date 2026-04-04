set shell := ["cmd.exe", "/C"]

# Show available commands
[group("General")]
default:
    just --list

# =====
# SERVER
# =====

# Run the application
[group("Server")]
up:
    uv run python -m src.main

# =====
# TESTS
# =====

# All tests
[group("Test")]
test:
    uv run pytest -q
alias test-all := test

# Unit tests
[group("Test")]
test-unit:
    uv run pytest tests/unit

# Integration tests
[group("Test")]
test-integration:
    uv run pytest tests/integration
alias test-int := test-integration