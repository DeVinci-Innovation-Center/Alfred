#! /bin/sh

.venv/bin/python3 -m pytest &
.venv/bin/uvicorn src.app:app --reload --host=0.0.0.0
