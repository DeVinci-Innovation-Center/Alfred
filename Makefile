include .env

generate-example-dotenv:
	sed 's/=.*/=/' .env > .env.example

create-volumes:
	mkdir -p database/redis-data database/mongodb-data
	chmod 777 database/mongodb-data
	chmod 777 database/redis-data

clean-volumes:
	rm -rf database/redis-data/**
	rm -rf database/mongodb-data/**

run: create-volumes
	docker-compose up --build -d

stop:
	docker-compose down

show-logs:
	docker-compose logs -f

up: run

down: stop

build-all-images:
	cd backend && make build
	cd database/redis-listener && make build
	cd frontend && make build
