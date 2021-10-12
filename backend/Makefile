IM_NAME=alfred-backend
IM_TAG=dev

include .env

build:
	docker build \
	-t ${IM_NAME}:${IM_TAG} .

run:
	docker run -it --rm -p 80:8000 ${IM_NAME}:${IM_TAG}

run-dev1:
	docker run -it --rm --privileged \
	-p 8000:8000 \
	-v ${shell pwd}/src:/home/appuser/app/src \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-v /dev/video0:/dev/video0 \
	--env DISPLAY=${DISPLAY} \
	--env QT_X11_NO_MITSHM=1 \
	${IM_NAME}:${IM_TAG} uvicorn src.app:app --reload --host=0.0.0.0

run-dev2:
	docker run -it --rm --privileged \
	-p 8000:8000 \
	-v ${shell pwd}/src:/home/appuser/app/src \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	--env DISPLAY=${DISPLAY} \
	--env QT_X11_NO_MITSHM=1 \
	${IM_NAME}:${IM_TAG} bash
