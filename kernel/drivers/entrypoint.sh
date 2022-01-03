#! /bin/sh

# .venv/bin/python3 -m example &
/.venv/bin/python3 -m realsense &

tail -f /dev/null

# execute docker CMD
exec "$@"
