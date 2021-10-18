FROM python:3.8

RUN apt update && apt install -y -qq --no-install-recommends \
    libglvnd0 libgl1 libglx0 libegl1 libxext6 libx11-6

# create a non-root user
RUN useradd -m --no-log-init --system --uid 1000 appuser -g sudo \
    && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER appuser
ENV PATH=/home/appuser/.local/bin:${PATH}

RUN mkdir /home/appuser/app
WORKDIR /home/appuser/app

# setup backend
RUN python3 -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install --user -r requirements.txt
COPY src /home/appuser/app/src

# CMD ["tail", "-f", "/dev/null"]
CMD ["python3", "src/main.py"]
