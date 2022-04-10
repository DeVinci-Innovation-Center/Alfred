# Pose Estimation with ArUco Markers for Robotic Arm
## Table of content
* [ArUco markers detection](#pose-estimation-on-tracked-ArUco-markers-with-a-robotic-arm)
* [Demo](#demo)

## Pose estimation on tracked ArUco markers with a robotic arm
Detecting tools and robot grasping require estimation of 3D object poses. Different techniques for vision-based pose estimation have been proposed. However, not all the advantages of the camera and the
robotic arm have been used. In this project, we propose a new approach for absolute pose estimation with a robotic arm, thus enabling to better understand the environment through computer vision. The method is based on scanning the surroundings and tracking fiducial markers. The absolute positions of the makers have been calculated via geometry by using a calibrated stereo camera. 

More details can be found on the [report](https://github.com/wimausberlin/voice-assistant-system/blob/main/docs/report.pdf).

### Requirements

The following software is required for the complete workflow (from git clone to the running Docker Container). The specified versions are the tested ones. Other versions should also work.

 * Git 2.35.1
 * Docker 20.10.12

## Prerequisites

Before you start to work with this project, Docker has to be installed and all dependencies be provided as described in the following sections.

### Install Docker

Check the official [Docker documentation](https://docs.docker.com/engine/) for information how to install Docker on your operating system. And then install Docker and supporting tools.

## Demo
After installing the prerequisites, check if the RealSense is connected to the running computer. Verify if the arm is on and connected to the same network as the running computer.


Command to run ALFRED firmware:
 ```
 make up [show-logs]
 ```

 ```show-logs``` allows you to better debug (see if the unit tests fail or not, if the arm is connected, if all docker containers run, ...).

 Once all docker containers running, web page is available at http://{host ip}, and backend at http://{host_ip}:8000. Documentation is available by adding `/docs` since the firware works with FastAPI. To launch a demo, go to `/docs/applications/demo` and execute for example `/stream-with-aruco` to only detect ArUco markers with the camera.
