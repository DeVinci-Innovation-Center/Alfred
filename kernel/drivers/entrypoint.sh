#! /bin/sh

# /alfred/drivers/.venv/bin/python3 -m drivers.example &
# /alfred/drivers/.venv/bin/python3 -m realsense &
# /alfred/drivers/.venv/bin/python3 -m bltouch &
/alfred/drivers/.venv/bin/python3 -m microphone &

tail -f /dev/null

# execute docker CMD
exec "$@"
