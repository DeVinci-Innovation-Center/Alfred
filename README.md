# A.L.F.R.E.D. : an AI-augmented polyvalent robotic assistant

## Requirements

- Docker

- docker-compose

## Usage

Run

```bash
make up
```
to start the frontend, backend, controller and database processes. Frontend is available at http://<your_local_ip>, and backend athttp://<your_local_ip>:8000 

## Demos

Since there is no visual interface yet, the only way to access the demos is to go to the backend's API docs page at http://<your_local_ip>:8000/docs and do a GET request to the demo you want.

Currently available demos are: 

- Hand control at /movement/hand_control
