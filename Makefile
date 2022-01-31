expose-x:
	sudo xhost +local:root

run: export ALFRED_HOST_IP=${shell ip -o route get to 8.8.8.8 | sed -n 's/.*src \([0-9.]\+\).*/\1/p'}  # get local IP for websocket address
run: expose-x
	docker-compose up --build -d

stop:
	docker-compose down

show-logs:
	docker-compose logs -f

up: run

down: stop
