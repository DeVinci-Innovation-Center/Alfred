
create-db:
	mkdir -p src/database/redis-data src/database/mongodb-data
	chmod 777 src/database/mongodb-data
	chmod 777 src/database/redis-data

clean-db:
	rm -rf src/database/redis-data/**
	rm -rf src/database/mongodb-data/**

run: create-db
	cd src && docker-compose up --build -d

stop:
	cd src && docker-compose down

up: run

down: stop

build-all-images: build-frontend build-backend build-controller build-listener

build-frontend:
	git clone

build-backend:


build-controller:


build-redis-listener:
