set shell := ["cmd.exe", "/C"]

# Показать доступные команды
default:
    just --list

# Запуск приложения
up:
    uv run python -m src.main

# Все тесты
test:
    uv run pytest -q

# Юнит-тесты (по маркеру unit)
test-unit:
    uv run pytest -q -m unit

# Интеграционные тесты (по маркеру integration)
test-integration:
    uv run pytest -q -m integration

