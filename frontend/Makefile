# IM_NAME=alfred-dashboard
# IM_TAG=dev

include ../.env

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
