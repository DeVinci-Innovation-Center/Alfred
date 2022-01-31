#! /bin/sh



# /alfred/drivers/.venv/bin/python3 -m drivers.example &
/alfred/drivers/.venv/bin/python3 -m realsense &

tail -f /dev/null

# execute docker CMD
exec "$@"
