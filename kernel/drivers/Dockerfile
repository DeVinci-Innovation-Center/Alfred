FROM python:3.9

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    # bltouch
    libusb-1.0-0 \
    # microphone
    libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /alfred/drivers

WORKDIR /alfred/drivers

RUN python3 -m venv .venv && \
    .venv/bin/python3 -m ensurepip && \
    .venv/bin/python3 -m pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN  .venv/bin/pip3 install -r requirements.txt

COPY drivers drivers

COPY entrypoint.sh /entrypoint.sh

WORKDIR /alfred/drivers/drivers

ENTRYPOINT ["sh", "/entrypoint.sh"]
