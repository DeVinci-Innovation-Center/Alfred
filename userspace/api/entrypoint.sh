#! /bin/sh

cd /alfred/api/src &&
/alfred/api/.venv/bin/python3 -m pytest .. &
cd /alfred/api/src &&
/alfred/api/.venv/bin/uvicorn app:app --reload --host=0.0.0.0
