# A.L.F.R.E.D. : an AI-augmented polyvalent robotic assistant

## Running the project

Run:

```bash
make up
```

to start the project. Web page is available at http://{host ip}.

## Demos

- Hand control

## Requirements

- docker

- docker-compose

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
