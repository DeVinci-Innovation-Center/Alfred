# A.L.F.R.E.D. : an AI-augmented polyvalent robotic assistant


![](https://lh3.googleusercontent.com/JEOWY7b3WMAHVkF5KZLIHeB23qiwjvKzhWhWC9J5-x-8ZxOtSWnrIjf0i0tEbXrPixt26_uIJCs-0_4TrWsS=w1920-h592-rw)

A.L.F.R.E.D. is a cobotics platform. It aims to maximize the interaction between man and machine, and to make it as seamless as possible. Its main purpose is to be used in innovation environments, such as FabLabs or research labs.

One of its two components is a uFactory xArm 6, a six Degrees of Freedom (DOF) industrial robotic arm. It allows for complex motion in space to manipulate objetcs in the environment. The other component is the software, which is a full stack application with an added layer of robotics to control the arm.

The goal is to be a centerpiece in innovation spaces, to aid in research by automating repetitive tasks, assist in more complex ones, and protect the Human by replacing it in dangerous activities. Some of its use-cases include soldering, pick-and-place, chemical experiments, or art.

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
