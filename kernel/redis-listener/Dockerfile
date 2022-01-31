FROM python:3.9

RUN mkdir -p /alfred/redis_listener

WORKDIR /alfred/redis_listener

RUN python3 -m venv .venv && \
    .venv/bin/python3 -m ensurepip && \
    .venv/bin/python3 -m pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN  .venv/bin/pip3 install -r requirements.txt

COPY src src

CMD ["python3", "src/main.py"]
