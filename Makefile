# open-frontend:
# 	firefox http://$(shell hostname -I | awk '{print $$1}'):80

# open-backend:
# 	firefox http://$(shell hostname -I | awk '{print $$1}'):8000/docs

expose-x:
	sudo xhost +local:root

create-volumes:
	mkdir -p ./database/redis-data \
		./database/mongodb-data \
		./database/mongodb-data/initdb.d/ \
		./database/mongodb-data/data/db/ \
		./database/mongodb-data/data/log/

	chmod 777 database/mongodb-data
	chmod 777 database/redis-data

clean-volumes:
	rm -rf database/redis-data/**
	rm -rf database/mongodb-data/**

run: create-volumes expose-x
	docker-compose up --build -d

stop:
	docker-compose down

show-logs:
	docker-compose logs -f

up: run

down: stop

# build-all-images: build-backend build-database build-frontend

# build-backend:
# 	cd backend && make build

# build-database:
# 	cd database/redis-listener && make build

# build-frontend:
# 	cd frontend && make build
