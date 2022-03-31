#! /bin/sh

cd rasa
../.venv/bin/rasa run actions &
../.venv/bin/rasa run &
../.venv/bin/python3 -m client &

tail -f /dev/null
