#! /bin/bash

function mount_dev()
{
	tmp_dir='/tmp/tmpmount'
	mkdir -p "$tmp_dir"
	mount -t devtmpfs none "$tmp_dir"
	mkdir -p "$tmp_dir/shm"
	mount --move /dev/shm "$tmp_dir/shm"
	mkdir -p "$tmp_dir/mqueue"
	mount --move /dev/mqueue "$tmp_dir/mqueue"
	mkdir -p "$tmp_dir/pts"
	mount --move /dev/pts "$tmp_dir/pts"
	touch "$tmp_dir/console"
	mount --move /dev/console "$tmp_dir/console"
	umount /dev || true
	mount --move "$tmp_dir" /dev

	# Since the devpts is mounted with -o newinstance by Docker, we need to make
	# /dev/ptmx point to its ptmx.
	# ref: https://www.kernel.org/doc/Documentation/filesystems/devpts.txt
	ln -sf /dev/pts/ptmx /dev/ptmx
	mount -t debugfs nodev /sys/kernel/debug
}

function start_udev()
{
    # mount_dev
    if command -v udevd &>/dev/null; then
        unshare --net udevd --daemon &> /dev/null
    else
        unshare --net /lib/systemd/systemd-udevd --daemon &> /dev/null
    fi
    udevadm trigger &> /dev/null
}

function init()
{
	# echo error message, when executable file is passed but doesn't exist.
	if [ -n "$1" ]; then
		if CMD=$(command -v "$1" 2>/dev/null); then
			shift
			exec "$CMD" "$@"
		else
			echo "Command not found: $1"
			exit 1
		fi
	fi
}

start_udev

# /alfred/drivers/.venv/bin/python3 -m drivers.example &
/alfred/drivers/.venv/bin/python3 -m realsense &
# /alfred/drivers/.venv/bin/python3 -m bltouch &
/alfred/drivers/.venv/bin/python3 -m microphone &

tail -f /dev/null

# execute docker CMD
init "$@"
