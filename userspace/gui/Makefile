IM_NAME=alfred-frontend
IM_TAG=dev

build:
	docker build -t ${IM_NAME}:${IM_TAG} .

run:
	docker run -it --rm \
	-p 3000:3000 \
	${FRONTEND_IM_NAME}:${FRONTEND_IM_TAG}


run-dev:
	docker run -it --rm \
	-p 3000:3000 \
	-v ${shell pwd}/app/:/app
	${IM_NAME}:${IM_TAG} /bin/sh
