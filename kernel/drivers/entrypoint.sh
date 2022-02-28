#! /bin/sh

# Start the pulseaudio server for the microphone
pulseaudio -D --exit-idle-time=-1
# Load the virtual sink and set it as default
pacmd load-module module-virtual-sink sink_name=v1
pacmd set-default-sink v1
# set the monitor of v1 sink to be the default source
pacmd set-default-source v1.monitor

# /alfred/drivers/.venv/bin/python3 -m drivers.example &
# /alfred/drivers/.venv/bin/python3 -m realsense &
# /alfred/drivers/.venv/bin/python3 -m bltouch &
/alfred/drivers/.venv/bin/python3 -m microphone &

tail -f /dev/null

# execute docker CMD
exec "$@"
