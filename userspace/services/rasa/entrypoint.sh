#! /bin/sh

rasa run actions &
rasa run &
python3 -m server &

tail -f /dev/null
