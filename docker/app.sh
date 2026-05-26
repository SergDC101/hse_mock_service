#!/bin/bash

printenv

alembic upgrade head

python -m src.script_db

gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8086