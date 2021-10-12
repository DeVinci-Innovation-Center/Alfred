IM_NAME=alfred-backend
IM_TAG=dev

include .env

build:
	docker build \
	-t ${IM_NAME}:${IM_TAG} .

run:
	docker run -it --rm -p 80:8000 ${IM_NAME}:${IM_TAG}

run-dev:
	docker run -it --rm -p 8000:8000 \
	-v ${shell pwd}/src:/home/appuser/app/src \
	${IM_NAME}:${IM_TAG} bash
