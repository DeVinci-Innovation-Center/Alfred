include .env

create-volumes:
	mkdir -p src/database/redis-data src/database/mongodb-data
	chmod 777 src/database/mongodb-data
	chmod 777 src/database/redis-data

clean-volumes:
	rm -rf src/database/redis-data/**
	rm -rf src/database/mongodb-data/**

run: create-volumes
	cd src && docker-compose up --build -d

stop:
	cd src && docker-compose down

show-logs:
	cd src && docker-compose logs -f

up: run

down: stop

build-all-images: build-frontend build-backend build-controller build-redis-listener

build-frontend:
	cd ${FRONTEND_PATH} && docker build -t ${FRONTEND_IM_NAME}:${FRONTEND_RELEASE_TAG} .

build-backend:
	cd ${BACKEND_PATH} && docker build -t ${BACKEND_IM_NAME}:${BACKEND_RELEASE_TAG} .

build-controller:
	cd ${CONTROLLER_PATH} && docker build -t ${CONTROLLER_IM_NAME}:${CONTROLLER_RELEASE_TAG} .

build-redis-listener:
	cd ${REDIS_LISTENER_PATH} && docker build -t ${REDIS_LISTENER_IM_NAME}:${REDIS_RELEASE_TAG} .
