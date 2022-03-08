#! /bin/sh

cd rasa
../.venv/bin/rasa run actions &
../.venv/bin/rasa run &
sleep 120
../.venv/bin/python3 -m client &
tail -f /dev/null
