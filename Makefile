# open-frontend:
# 	firefox http://$(shell hostname -I | awk '{print $$1}'):80

# open-backend:
# 	firefox http://$(shell hostname -I | awk '{print $$1}'):8000/docs

expose-x:
	sudo xhost +local:root

create-volumes:
	mkdir -p ./kernel/database-files/redis-data \
		./kernel/database-files/mongodb-data \
		./kernel/database-files/mongodb-data/initdb.d/ \
		./kernel/database-files/mongodb-data/data/db/ \
		./kernel/database-files/mongodb-data/data/log/

clean-volumes:
	rm -rf ./kernel/database-files/redis-data/**
	rm -rf ./kernel/database-files/mongodb-data/**

run: create-volumes expose-x
	docker-compose up --build -d

stop:
	docker-compose down

show-logs:
	docker-compose logs -f

up: run

down: stop
