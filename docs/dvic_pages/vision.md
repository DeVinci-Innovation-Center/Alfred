# ALFRED : General Purpose Middleware for Personal Robotic Arm Assistants

# Abstract

# Introduction

## Context

## Motivations
* Worker 2.0 & Industry 4.0

Industry 4.0 has recently become the standard for factory automation. Network-controlled, intelligent machines allow for faster production, at lower cost and risk. Robots have become controllable remotely, and as such, the worker in this new type of industry, a "Worker 2.0", needs to adapt to these new methods of production. With ALFRED, we aim to create a new system that makes working with robot arms remotely easier and adds more capabilities to these robot arms.

## State of the Art

* Arm Robotic
  * Mechanics
  * Trajectory planning
    * RRT
    * Trajectory computation
  *

* Cobotic & HCI
  * Multi modalities interactionEnvironment
  *

* Artificial Intelligence
  * computer vision (boxing, image segmentation, 3d pose estimation)
  * Language Processing
  * Context analysis
    * VSLAM
    * Semantic mapping
  * Decision Making

# ALFRED Overview

## Middleware architecture

<!-- TODO: architecture schematic -->

## 1.1 Environment Analysis
### Static Environment Discovery

We use VSLAM* to analyze the environment around the arm. From this algorithmn, we extract a 3D occupancy map*. The robot does an initial scan at boot time, then updates the map in the background during execution.

From the occupancy map we can determine forbidden zones*. Forbidden zones are zones of space where an object was detected, which the arm cannot go through. Around the forbidden zones, we add a padding for path planning. This is necessary since the position of the arm is represented by the center of its end-effector*, and collision can occur in a radius around this position. The padding allows for a margin between the end-effector and the object in space.

### Static Object Recognition

From the camera feed, we run object recognition to detect objects present in the environment. Our model is trained on the COCO dataset*, but we plan to add other objects more relevent to our usage in the future. Inference is done with YOLOv5* for its speed of execution and lightweight nature.

### Semantic Environment Mapping
VSLAM + Object detection, object positions in space

### Dynamic Colision Detection


## Arm Robotic Control
### Trajectory Planning


## Human Robot Control Interfaces
### Interactive Modalities
- Voice control
- Control with gestures
- Web interface

### Decision Loop
- Robot to Human
- Human to Robot

## Applications
=> Autre pages (Cross reality, ) => tabs

## Future works
