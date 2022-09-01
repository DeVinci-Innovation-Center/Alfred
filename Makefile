PACKAGE_NAME=.
_ALFRED_HOST_IP:=${shell ip -o route get to 8.8.8.8 | sed -n 's/.*src \([0-9.]\+\).*/\1/p'} # local IP of the host

all: stop run show-logs

gpu: stop run-gpu show-logs

expose-x:
	sudo xhost +local:root

# ------------ RUNNING W/ CPU ------------

run: export ALFRED_HOST_IP=${_ALFRED_HOST_IP}
run: expose-x
	docker-compose up --build -d

up: run

# ------------ RUNNING W/ GPU ------------

run-gpu: export ALFRED_HOST_IP=${_ALFRED_HOST_IP}
run-gpu: expose-x
	docker-compose -f docker-compose-gpu.yml up --build -d

up-gpu: run-gpu

# ------------ STOPPING ------------

stop:
	- docker-compose down
	- docker-compose -f docker-compose-gpu.yml down

down: stop

# ------------ LOGS ------------

show-logs:
	docker-compose logs -f

# ------------ LINTING AND FORMATTING ------------

clean: clean-mypy clean-pycache

lint: isort black flake8 mypy pylint

isort:
	@echo Running isort
	python -m isort --diff ${PACKAGE_NAME}/

black:
	@echo Running black
	python -m black --check ${PACKAGE_NAME}/

flake8:
	@echo Running flake8
	python -m flake8 ${PACKAGE_NAME}/

mypy:
	@echo Running mypy
	python -m mypy ${PACKAGE_NAME}/

clean-mypy:
	- rm -rf .mypy_cache

pylint:
	@echo Running pylint
	python -m pylint --rcfile=.pylintrc ${PACKAGE_NAME}/

clean-pycache:
	find . -type d -name  "__pycache__" -exec rm -r {} +
