include .env

generate-example-dotenv:
	sed 's/=.*/=/' .env > .env.example

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
	cd backend && make build
	cd controller && make build
	cd database/redis-listener && make build
	cd frontend && make build
