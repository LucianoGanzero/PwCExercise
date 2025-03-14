#!/bin/bash
poetry run alembic upgrade head

poetry run seed-db

poetry run uvicorn app:app --host 0.0.0.0 --port 8000 --reload