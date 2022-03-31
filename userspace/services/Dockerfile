FROM python:3.7


RUN mkdir -p /alfred/services

WORKDIR /alfred/services

RUN python3 -m venv .venv && \
    .venv/bin/python3 -m ensurepip && \
    .venv/bin/python3 -m pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN .venv/bin/pip3 install -r requirements.txt

COPY rasa rasa

COPY entrypoint.sh entrypoint.sh

ENTRYPOINT [ "sh", "entrypoint.sh" ]
