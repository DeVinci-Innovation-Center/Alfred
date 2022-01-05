FROM python:3.9-slim

RUN apt-get update && apt-get install \
    libusb-1.0-0

RUN python3 -m venv .venv && .venv/bin/python3 -m ensurepip && .venv/bin/python3 -m pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN  .venv/bin/pip3 install -r requirements.txt

COPY drivers /alfred/drivers

WORKDIR /alfred/drivers

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["sh", "/entrypoint.sh"]
