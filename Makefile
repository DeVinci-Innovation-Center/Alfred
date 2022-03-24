_ALFRED_HOST_IP:=${shell ip -o route get to 8.8.8.8 | sed -n 's/.*src \([0-9.]\+\).*/\1/p'} # local IP of the host

expose-x:
	sudo xhost +local:root

# ------------ RUNNING W/ CPU ------------

run-update: export ALFRED_HOST_IP=${_ALFRED_HOST_IP}
run-update: expose-x
	UPDATE_LIBALFRED=true docker-compose up --build -d

run: export ALFRED_HOST_IP=${_ALFRED_HOST_IP}
run: expose-x
	docker-compose up --build -d

up: run

up-update: run-update

# ------------ RUNNING W/ GPU ------------

run-gpu: export ALFRED_HOST_IP=${_ALFRED_HOST_IP}
run-gpu: expose-x
	docker-compose -f docker-compose-gpu.yml up --build -d

up-gpu: run-gpu

run-update-gpu: export ALFRED_HOST_IP=${_ALFRED_HOST_IP}
run-update-gpu: expose-x
	UPDATE_LIBALFRED=true docker-compose -f docker-compose-gpu.yml up --build -d

up-update-gpu: run-update-gpu

# ------------ STOPPING ------------

stop:
	docker-compose down
	docker-compose -f docker-compose-gpu.yml down

down: stop

# ------------ LOGS ------------

show-logs:
	docker-compose logs -f
