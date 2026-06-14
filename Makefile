.PHONY: install dev test lint format typecheck db-up db-down migrate migration ci-check

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

dev:
	uvicorn invyra_platform.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	ruff check src tests

format:
	ruff format src tests

typecheck:
	mypy src

db-up:
	docker compose up -d postgres test_postgres

db-down:
	docker compose down

migrate:
	alembic upgrade head

migration:
	alembic revision --autogenerate -m "$(name)"

ci-check: lint typecheck test
