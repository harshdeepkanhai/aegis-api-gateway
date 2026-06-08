.PHONY: up down test lint typecheck bench fmt
up:        ; docker compose up -d --build
down:      ; docker compose down -v
test:      ; uv run pytest -q
lint:      ; uv run ruff check . && uv run ruff format --check .
fmt:       ; uv run ruff format . && uv run ruff check --fix .
typecheck: ; uv run mypy src
bench:     ; uv run python -m scripts.bench