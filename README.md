# Bulk Product

Pokémon GO IV analysis and team optimization tool.

## Stack

- **Backend:** Python 3.14+ / FastAPI / SQLAlchemy (async) / PostgreSQL
- **Frontend:** React (TBD)
- **Linting/Formatting:** Ruff
- **Type Checking:** mypy

## Quick Start (Docker)

```bash
docker compose up
```

Backend at `http://localhost:8000`, API docs at `http://localhost:8000/docs`.

## Local Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

uvicorn app.main:app --reload
```

## Database Migrations

```bash
# Generate a migration after changing models
alembic revision --autogenerate -m "describe your change"

# Apply migrations
alembic upgrade head

# Roll back one step
alembic downgrade -1
```

## Dev Commands

```bash
ruff check .          # lint
ruff format .         # format
ruff check --fix .    # lint + auto-fix
mypy app/             # type check
pytest                # test
```
