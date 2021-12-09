FROM python:3.9-alpine

RUN python3 -m ensurepip && pip3 install redis

COPY drivers /alfred/drivers

WORKDIR /alfred/drivers

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["sh", "/entrypoint.sh"]
