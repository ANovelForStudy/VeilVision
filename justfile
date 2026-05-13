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
# ALEMBIC MIGRATIONS
# =====

# Make migrations
[group("Database")]
revision message:
    uv run alembic revision --autogenerate -m "{{ message }}"

# Apply migrations
[group("Database")]
migrate:
    uv run alembic upgrade head

# Revert migrations
[group("Database")]
reset-db:
    uv run alembic downgrade base

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