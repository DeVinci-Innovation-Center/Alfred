expose-x:
	sudo xhost +local:root

create-volumes:
	mkdir -p ./kernel/database-files/redis-data \
		./kernel/database-files/mongodb-data \
		./kernel/database-files/mongodb-data/initdb.d/ \
		./kernel/database-files/mongodb-data/data/db/ \
		./kernel/database-files/mongodb-data/data/log/

	chmod -R 777 ./kernel/database-files/mongodb-data
	chmod -R 777 ./kernel/database-files/redis-data

clean-volumes:
	rm -rf ./kernel/database-files/redis-data/**
	rm -rf ./kernel/database-files/mongodb-data/**

run: export ALFRED_HOST_IP=${shell ip -o route get to 8.8.8.8 | sed -n 's/.*src \([0-9.]\+\).*/\1/p'}
run: create-volumes expose-x
	docker-compose up --build -d

stop:
	docker-compose down

show-logs:
	docker-compose logs -f

up: run

down: stop
