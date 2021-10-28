# A.L.F.R.E.D. : an AI-augmented polyvalent robotic assistant

![](https://lh3.googleusercontent.com/JEOWY7b3WMAHVkF5KZLIHeB23qiwjvKzhWhWC9J5-x-8ZxOtSWnrIjf0i0tEbXrPixt26_uIJCs-0_4TrWsS=w1920-h592-rw)

A.L.F.R.E.D. is a cobotics platform. It aims to maximize the interaction between man and machine, and to make it as seamless as possible. Its main purpose is to be used in innovation environments, such as FabLabs or research labs.

One of its two components is a uFactory xArm 6, a six Degrees of Freedom (DOF) industrial robotic arm. It allows for complex motion in space to manipulate objetcs in the environment. The other component is the software, which is a full stack application with an added layer of robotics to control the arm.

The goal is to be a centerpiece in innovation spaces, to aid in research by automating repetitive tasks, assist in more complex ones, and protect the Human by replacing it in dangerous activities. Some of its use-cases include soldering, pick-and-place, chemical experiments, or art.

Check out the demo video [here](https://www.youtube.com/watch?v=6KcHh4nWJFI)! Updated video to come soon.

## Requirements

- Docker

- docker-compose

## Usage

Run

```bash
make up
```
to start the frontend, backend, controller and database processes. Frontend is available at http://<your_local_ip> (ex: http://172.21.72.106), and backend at http://<your_local_ip>:8000 (ex: http://172.21.72.106:8000).

## Demos

Since there is no visual interface yet, the only way to access the demos is to go to the backend's API docs page at http://<your_local_ip>:8000/docs and do a GET request to the demo you want.

Currently available demos are: 

- Hand control at /movement/hand_control
