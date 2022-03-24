# ALFRED: General Purpose Middleware for Robotic Assistants

![](https://lh3.googleusercontent.com/JEOWY7b3WMAHVkF5KZLIHeB23qiwjvKzhWhWC9J5-x-8ZxOtSWnrIjf0i0tEbXrPixt26_uIJCs-0_4TrWsS=w1920-h592-rw)

Basic automation requires a robot to only repeat a set of movements indefinitely, but with the needs of Industry 4.0, robotic systems need to be more and more complex. Safety, adaptability and connectivity are now required for automation in the industry. Safety comes in the form of smart collision detection, with sensitive robots that know their environments and react to unseen obstacles or operators. Adaptability requires robots to have intelligent decision making systems and powerful sensing abilities. Robots need to communicate with each other to share information, and to be able to be controlled remotely for easier access.

ALFRED brings safety, adaptability and connectivity to any commercial robotic arm. ALFRED is a middleware, enhanced by Artificial Intelligence, focused on modularity, extensibility and abstraction. Inspired by modern Operating Systems, it brings together devices, interfaces and the robotic arm to create a system ready to be deployed in real situations. ALFRED is a way for manufacturers and researchers to develop applications for a robotic arm with minimal knowledge about robotic control. It integrates in its environment with its multiple interaction modalities, such as manual control with hands, voice control, and a web interface.

Check out the demo video [here](https://www.youtube.com/watch?v=6KcHh4nWJFI)! Updated video to come soon.

## Requirements

- Docker ([get docker](https://docs.docker.com/get-docker/))
- docker-compose ([get docker-compose](https://docs.docker.com/compose/install/))
- GNU Make

## Usage

Run

```bash
make up
```

to start the project. Web page is available at http://{host ip}, and backend at http://{host_ip}:8000.

## Demos

- Hand control

## Install steps for NVIDIA

See (here)[https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html] for a more complete guide.

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt update
sudo apt install nvidia-docker2
sudo systemctl restart docker
```

Test install with:

```bash
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

## Development

How to dev on the platform ?

### CPU and GPU compatibility

Make sure to keep CPU and GPU docker-compose and Docker files in sync by comparing them to each other every so often. In VSCode, select the two files, right click and select `Compare Selected` in the drop down menu.

## Audio driver

Some problems may appear when using audio in ALFRED containers. As far as my understanding goes, docker containers should use the host's drivers, but it acts as another client, so when it tries to use a device that is already used by the system, it won't work. To see which devices are in use, try:

```sh
fuser -fv /dev/snd/*
```

If nothing appears, good, but if the audio devices responsible for playback (ex: `/dev/snd/pcmC0D0p`) and/or capture (ex: `/dev/snd/pcmC0D0c`) appear, you will have to restart or disable your audio drivers until they are free for the container to use.

To restart Pipewire:

```bash
systemctl --user restart pipewire.service
```
