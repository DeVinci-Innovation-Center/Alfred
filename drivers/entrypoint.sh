#! /bin/sh

# python3 -m example &

tail -f /dev/null

# execute docker CMD
exec "$@"
